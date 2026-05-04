"""
search_server.py — 常驻 HTTP 服务器，模型只加载一次。
OpenClaw 启动时后台启动一次，所有搜索通过 localhost HTTP 调用。

Usage:
  python search_server.py [--port 18765] [--warmup]
  python search_server.py stop
"""
import sys
import os
import json
import time
import threading
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

SKILL_SCRIPTS = Path(__file__).parent
SKILL_DIR = SKILL_SCRIPTS.parent
sys.path.insert(0, str(SKILL_SCRIPTS))

# ── Lazy model load ─────────────────────────────────────────────────────────

_EM = None
_EM_READY = threading.Event()


def _load_model():
    global _EM
    if _EM is None:
        from sentence_transformers import SentenceTransformer
        _EM = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        _EM_READY.set()


# ── Search logic ────────────────────────────────────────────────────────────

def cosine_sim(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    n1 = sum(x * x for x in a) ** 0.5
    n2 = sum(x * x for x in b) ** 0.5
    return dot / (n1 * n2) if n1 and n2 else 0.0


def search_ddg(query: str, intent: str = "general", max_r: int = 5):
    """Run ddgs search with early return optimization.
    
    优化策略：
    1. 缩短超时：25s → 12s
    2. 首批即返：拿到 min(3, max_r) 条结果立即返回
    3. 降级兜底：超时后返回已获取的部分结果
    """
    from ddgs import DDGS as _DDGS

    def make_result(r, src):
        import re
        txt = (r.get("body") or r.get("description") or "").replace("\ufffd", "")
        txt = re.sub(r"[\u2500-\u257F\u2580-\u259F\u0000-\u001F]", " ", txt)
        txt = re.sub(r"\s+", " ", txt).strip()
        url = r.get("href") or r.get("url") or ""
        title = r.get("title", "").replace("\ufffd", "")
        return {"title": title[:200], "url": url, "snippet": txt[:300], "source": src}

    results = []
    seen = set()
    
    # 首批即返阈值：拿到这个数量就立即返回
    EARLY_RETURN_THRESHOLD = min(3, max_r)
    # 缩短超时：25s → 12s
    TIMEOUT_FAST = 12

    if intent == "code":
        sq = f"site:stackoverflow.com {query}"
        try:
            with _DDGS(timeout=TIMEOUT_FAST) as ddgs:
                for r in ddgs.text(sq, max_results=max_r):
                    u = r.get("href", "")
                    if u and u not in seen:
                        seen.add(u)
                        results.append(make_result(r, "stackoverflow"))
                        # 首批即返：拿到 3 条就返回
                        if len(results) >= EARLY_RETURN_THRESHOLD:
                            return results
        except Exception:
            pass
        # 降级：如果 SO 结果不足，尝试 GitHub（更短超时）
        if len(results) < EARLY_RETURN_THRESHOLD:
            gq = f"site:github.com {query}"
            try:
                with _DDGS(timeout=8) as ddgs:
                    for r in ddgs.text(gq, max_results=3):
                        u = r.get("href", "")
                        if u and u not in seen:
                            seen.add(u)
                            results.append(make_result(r, "github"))
                            if len(results) >= EARLY_RETURN_THRESHOLD:
                                return results
            except Exception:
                pass
    else:
        # 通用搜索：首果即返
        try:
            with _DDGS(timeout=TIMEOUT_FAST) as ddgs:
                for r in ddgs.text(query, max_results=max_r):
                    u = r.get("href", "") or r.get("url", "")
                    if u and u not in seen:
                        seen.add(u)
                        results.append(make_result(r, "duckduckgo"))
                        # 首批即返：拿到 3 条就返回
                        if len(results) >= EARLY_RETURN_THRESHOLD:
                            return results
        except Exception:
            pass
    
    return results


def do_search(query: str, max_r: int = 5):
    """Main search entry point. Checks knowledge base, L2/L3 cache, then searches."""
    _EM_READY.wait(timeout=10)  # wait for model warmup

    CACHE_DIR = SKILL_DIR / "references" / "cache"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    L2_PATH = CACHE_DIR / "l2_semantic.jsonl"
    L3_PATH = CACHE_DIR / "l3_raw.jsonl"

    norm_q = query.lower().strip()

    # ── Knowledge base (L0) ────────────────────────────────────────────────
    try:
        from knowledge_base import query_knowledge
        kb_hit = query_knowledge(query, model=_EM)
        if kb_hit:
            return kb_hit
    except Exception:
        pass

    # ── L3 exact match ────────────────────────────────────────────────────
    l3_hit = None
    if L3_PATH.exists():
        cutoff = time.time() - 7 * 86400
        with open(L3_PATH, encoding="utf-8") as f:
            for line in reversed(f.readlines()):
                try:
                    e = json.loads(line.strip())
                    if e.get("query_norm") == norm_q:
                        ts = e.get("timestamp", "")
                        if "T" in ts:
                            from datetime import datetime
                            try:
                                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                                if (datetime.now(dt.tzinfo) - dt).total_seconds() < 7 * 86400:
                                    l3_hit = e.get("result")
                            except Exception:
                                pass
                        if l3_hit:
                            break
                except Exception:
                    pass

    if l3_hit and l3_hit.get("results"):
        return {
            **{k: v for k, v in l3_hit.items() if not k.startswith("_")},
            "cache_hit": True,
            "cache_tier": "L3_raw",
            "search_ms": 0,
            "_model_loaded": _EM is not None,
        }

    # ── L2 semantic match ────────────────────────────────────────────────
    if _EM and L2_PATH.exists():
        emb = _EM.encode(query).tolist()
        best_score, best_entry = 0.0, None
        with open(L2_PATH, encoding="utf-8") as f:
            for line in f.readlines():
                try:
                    e = json.loads(line.strip())
                    cached_emb = e.get("embedding")
                    if cached_emb:
                        score = cosine_sim(emb, cached_emb)
                        if score > best_score:
                            best_score, best_entry = score, e
                except Exception:
                    pass
        if best_score >= 0.85 and best_entry:
            result = best_entry.get("result", {})
            if result.get("results"):
                result = {k: v for k, v in result.items() if not k.startswith("_")}
                result["cache_hit"] = True
                result["cache_tier"] = "L2_semantic"
                result["_cache_similarity"] = round(best_score, 4)
                result["search_ms"] = 0
                result["_model_loaded"] = True
                return result

    # ── Fresh search ─────────────────────────────────────────────────────
    intent = "code" if any(
        kw in query.lower() for kw in ["python", "javascript", "java", "code", "函数", "代码", "编程", "sql", "api"]
    ) else "general"

    t0 = time.time()
    raw = search_ddg(query, intent, max_r)
    elapsed = round((time.time() - t0) * 1000, 1)

    trusted = {
        "stackoverflow.com", "github.com", "docs.python.org", "python.org",
        "pypi.org", "wikipedia.org", "medium.com", "zhihu.com",
    }
    results = raw[:max_r]

    answer = {
        "query": query,
        "intent": intent,
        "results": results,
        "total_raw": len(raw),
        "total_deduped": len(results),
        "trusted_count": sum(1 for r in results if any(d in r.get("url","") for d in trusted)),
        "search_ms": elapsed,
        "cache_hit": False,
        "cache_tier": None,
        "_model_loaded": _EM is not None,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    # ── Write to L3 ────────────────────────────────────────────────────
    try:
        entry = {
            "query_norm": norm_q,
            "result": answer,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        with open(L3_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

    return answer


# ── HTTP Server ────────────────────────────────────────────────────────────

_SEARCH_BUSY = threading.Lock()


class SearchHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # silence HTTP log

    def do_POST(self):
        if _SEARCH_BUSY.locked():
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b"busy")
            return

        with _SEARCH_BUSY:
            try:
                cl = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(cl) if cl else b"{}"
                req = json.loads(body.decode("utf-8"))

                query = req.get("query", "")
                max_r = int(req.get("max_results", 5))

                if not query:
                    raise ValueError("empty query")

                result = do_search(query, max_r)
                payload = json.dumps(result, ensure_ascii=False).encode("utf-8")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", len(payload))
                self.end_headers()
                self.wfile.write(payload)

            except Exception as e:
                err = json.dumps({"error": str(e)}).encode()
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", len(err))
                self.end_headers()
                self.wfile.write(err)

    def do_GET(self):
        # Health check
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
            return
        self.send_response(404)
        self.end_headers()


class ThreadedHTTPServer(HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def start_server(port: int, warmup: bool):
    threading.Thread(target=_load_model, daemon=True).start()

    if warmup:
        print("Warming up model...", flush=True)
        _load_model()
        print(f"Model ready. Starting HTTP server on port {port}.", flush=True)
    else:
        threading.Thread(target=_load_model, daemon=True).start()
        print(f"Starting HTTP server on port {port} (model loads lazily).", flush=True)

    server = ThreadedHTTPServer(("127.0.0.1", port), SearchHandler)
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=18765)
    parser.add_argument("--warmup", action="store_true", help="load model immediately")
    args = parser.parse_args()

    start_server(args.port, args.warmup)
