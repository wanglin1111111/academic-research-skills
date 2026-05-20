#!/usr/bin/env python3
"""
search_server.py — Long-running HTTP server for search.
Model loads once, serves multiple requests.
Usage: python search_server.py --port 18765 --warmup
"""

import sys
import os
import json
import argparse
import traceback
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# ── Setup paths ────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CACHE_DIR = SKILL_DIR / "references" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(SCRIPT_DIR))

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

# ── Lazy imports ────────────────────────────────────────────────────────────
_Cache = None
_DDGS = None
_reranker = None

def _init_cache():
    global _Cache
    if _Cache is None:
        try:
            from cache import Cache
            _Cache = Cache
        except Exception as e:
            sys.stderr.write(f"[SERVER] cache import failed: {e}\n")
    return _Cache

def _init_ddgs():
    global _DDGS
    if _DDGS is None:
        try:
            from ddgs import DDGS
            _DDGS = DDGS
        except Exception as e:
            sys.stderr.write(f"[SERVER] ddgs import failed: {e}\n")
    return _DDGS

def _init_reranker():
    global _reranker
    if _reranker is None:
        try:
            from sentence_transformers import CrossEncoder
            _reranker = CrossEncoder('BAAI/bge-reranker-base', max_length=512)
            sys.stderr.write("[SERVER] reranker loaded\n")
        except Exception as e:
            sys.stderr.write(f"[SERVER] reranker load failed: {e}\n")
    return _reranker

# ── Search logic ────────────────────────────────────────────────────────────

EN_CODE = {"python", "javascript", "java", "c++", "golang", "rust", "typescript", "react", "vue", "sql", "git", "docker", "api", "function", "class", "error", "debug"}
ZH_CODE = {"代码", "编程", "函数", "方法", "报错", "调试", "模块", "包", "def", "return", "async", "await", "list", "dict"}

def detect_intent(query: str) -> str:
    import re
    q = query.lower()
    has_zh = bool(re.search(r"[\u4e00-\u9fff]", query))
    if has_zh and any(kw in query for kw in ZH_CODE):
        return "code"
    if not has_zh and any(kw in q for kw in EN_CODE):
        return "code"
    if any(kw in query for kw in ["论文", "paper", "arxiv", "学术", "研究"]):
        return "academic"
    if any(kw in query for kw in ["新闻", "news", "最新", "今日", "昨天"]):
        return "web_news"
    if any(kw in query for kw in ["对比", "测评", "review", "vs", "哪个好"]):
        return "review"
    return "general"

def search_ddg(query: str, intent: str = "general", max_r: int = 5) -> list:
    DDGS = _init_ddgs()
    if not DDGS:
        return []
    results = []
    seen = set()
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_r * 2):
                url = r.get("href") or r.get("url") or ""
                if url in seen:
                    continue
                seen.add(url)
                txt = (r.get("body") or r.get("description") or "")[:300]
                results.append({
                    "title": r.get("title", "")[:200],
                    "url": url,
                    "snippet": txt,
                    "source": "ddg"
                })
                if len(results) >= max_r:
                    break
    except Exception as e:
        sys.stderr.write(f"[SERVER] search error: {e}\n")
    return results

def rerank_results(query: str, results: list) -> list:
    reranker = _init_reranker()
    if not reranker or not results:
        return results
    try:
        pairs = [[query, r["title"] + " " + r["snippet"]] for r in results]
        scores = reranker.predict(pairs)
        scored = list(zip(results, scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [r for r, s in scored if s > 0.6]
    except Exception as e:
        sys.stderr.write(f"[SERVER] rerank error: {e}\n")
        return results

# ── HTTP Handler ────────────────────────────────────────────────────────────

class SearchHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging

    def _send_json(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/health":
            self._send_json({"status": "ok"})
        elif parsed.path == "/search":
            params = urllib.parse.parse_qs(parsed.query)
            query = params.get("query", [""])[0]
            max_r = int(params.get("max_results", ["5"])[0])
            if not query:
                self._send_json({"error": "missing query"}, 400)
            else:
                result = self._do_search(query, max_r)
                self._send_json(result)
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/search":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                data = json.loads(body)
                query = data.get("query", "")
                max_r = int(data.get("max_results", 5))
                if not query:
                    self._send_json({"error": "missing query"}, 400)
                else:
                    result = self._do_search(query, max_r)
                    self._send_json(result)
            except Exception as e:
                self._send_json({"error": str(e)}, 400)
        else:
            self._send_json({"error": "not found"}, 404)

    def _do_search(self, query: str, max_r: int = 5) -> dict:
        from datetime import datetime
        intent = detect_intent(query)
        
        # Check cache
        Cache = _init_cache()
        cache = Cache(str(CACHE_DIR)) if Cache else None
        if cache:
            cached = cache.get(query)
            if cached:
                return {"query": query, "intent": intent, "cache_hit": True, "results": cached.get("results", [])}
        
        # Search
        results = search_ddg(query, intent, max_r)
        
        # Rerank
        results = rerank_results(query, results)
        
        out = {
            "query": query,
            "intent": intent,
            "cache_hit": False,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache results
        if cache and results:
            cache.set(query, out)
        
        return out

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Search Server")
    parser.add_argument("--port", type=int, default=18765, help="Server port")
    parser.add_argument("--warmup", action="store_true", help="Preload models")
    args = parser.parse_args()

    if args.warmup:
        sys.stderr.write("[SERVER] Warming up...\n")
        _init_cache()
        _init_ddgs()
        _init_reranker()
        sys.stderr.write("[SERVER] Warmup complete\n")

    server = HTTPServer(("127.0.0.1", args.port), SearchHandler)
    sys.stderr.write(f"[SERVER] Listening on http://127.0.0.1:{args.port}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\n[SERVER] Shutting down\n")
        server.shutdown()

if __name__ == "__main__":
    main()
