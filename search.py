"""
Unified Search: intent detection + DuckDuckGo search in one file.
Caches results to references/cache/last_result_{pid}.json
"""

import sys
import os
import json
import time
import re
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

SKILL_DIR = Path(__file__).parent.parent
CACHE_DIR = SKILL_DIR / "references" / "cache"
OUT_FILE = CACHE_DIR / f"last_result_{os.getpid()}.json"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(Path(__file__).parent))


# ── Imports (separate try blocks so one failure doesn't block all) ──────────

try:
    from cache import Cache, normalize
    _Cache = Cache
except Exception:
    _Cache = None
    normalize = lambda q: re.sub(r'\s+', ' ', q.lower().strip())

try:
    from ddgs import DDGS as _DDGS
except Exception:
    _DDGS = None


# ── Intent Detection (inline, zero cost) ─────────────────────────────────

EN_CODE = {"python", "javascript", "java", "c++", "golang", "rust", "typescript",
           "react", "vue", "angular", "css", "html", "sql", "git", "docker",
           "api", "function", "class", "error", "exception", "debug", "module",
           "import", "export", "async", "promise", "callback", "loop", "array",
           "dict", "list", "string", "int", "float", "bool"}

ZH_CODE = {"代码", "编程", "函数", "方法", "变量", "语法", "报错", "调试",
           "模块", "包", "import", "def", "return", "async", "await",
           "list", "dict", "array", "对象", "实例"}

ZH_NEWS = {"新闻", "今日", "最新", "昨天", "热搜", "发生了什么"}
EN_NEWS = {"news", "latest", "breaking", "trending"}


def detect_intent(query: str) -> str:
    q = query.lower()
    has_zh = bool(re.search(r'[\u4e00-\u9fff]', query))
    if has_zh:
        if any(kw in query for kw in ZH_CODE):
            return "code"
        if any(kw in query for kw in ZH_NEWS):
            return "web_news"
        return "general"
    if any(kw in q for kw in EN_CODE):
        return "code"
    if any(kw in q for kw in EN_NEWS):
        return "web_news"
    return "general"


# ── Domain Utils ──────────────────────────────────────────────────────────

TRUSTED = {
    'stackoverflow.com', 'github.com', 'stackoverflow.org',
    'docs.python.org', 'python.org', 'pypi.org', 'npmjs.com',
    'arxiv.org', 'scholar.google.com', 'wikipedia.org', 'wikimedia.org',
    'medium.com', 'dev.to', 'gist.github.com', 'reddit.com',
    'news.ycombinator.com', 'zhihu.com',
}


def parse_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().lstrip('www.')
    except Exception:
        return ''


def is_trusted(url: str) -> bool:
    return parse_domain(url) in TRUSTED


# ── Result Helpers ────────────────────────────────────────────────────────

def _clean(text: str) -> str:
    """Strip garbled chars from encoding failures, preserve CJK."""
    if not text:
        return ''
    # Remove replacement char and box-drawing noise (but NOT CJK Unified Ideographs)
    text = text.replace('\ufffd', '')
    # Remove only non-CJK control/glyph characters
    text = re.sub(r'[\u2500-\u257F\u2580-\u259F\u2500-\u257F]', ' ', text)
    text = re.sub(r'[\u0000-\u001F\u007F-\u009F]', '', text)  # strip control chars
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:300]


def _make_result(r: dict, source: str) -> dict:
    return {
        'title': _clean(r.get('title', '')),
        'url': r.get('href', '') or r.get('url', ''),
        'snippet': _clean(r.get('body', '') or r.get('description', '')),
        'source': source,
    }


# ── Search Functions ───────────────────────────────────────────────────────

def search_so(query: str, max_r: int) -> list[dict]:
    if _DDGS is None:
        return []
    results = []
    sq = f"site:stackoverflow.com {query}"
    try:
        with _DDGS(timeout=20) as ddgs:
            for r in ddgs.text(sq, max_results=max_r):
                results.append(_make_result(r, 'stackoverflow'))
    except Exception:
        pass
    if len(results) < max_r:
        try:
            with _DDGS(timeout=15) as ddgs:
                for r in ddgs.text(f"site:github.com {query}", max_results=3):
                    results.append(_make_result(r, 'github'))
        except Exception:
            pass
    return results


def search_general(query: str, max_r: int) -> list[dict]:
    if _DDGS is None:
        return []
    results = []
    seen = set()
    try:
        with _DDGS(timeout=20) as ddgs:
            for r in ddgs.text(query, max_results=max_r):
                url = r.get('href', '') or r.get('url', '')
                if url and url not in seen:
                    seen.add(url)
                    results.append(_make_result(r, 'duckduckgo'))
    except Exception:
        pass
    return results


INTENT_SEARCHERS = {
    'code': search_so,
    'general': search_general,
    'web_news': search_general,
}


# ── Deduplication ─────────────────────────────────────────────────────────

def dedup(results: list[dict], window: int = 8, max_per_domain: int = 2) -> list[dict]:
    seen = {}
    out = []
    for r in results[:window]:
        d = parse_domain(r['url'])
        if not d:
            continue
        if d not in seen:
            seen[d] = len(out)
            out.append(r)
        elif seen[d] < max_per_domain:
            out.append(r)
            seen[d] = len(out)
    return out


# ── Output ────────────────────────────────────────────────────────────────

def write(data: dict):
    OUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────

_CACHED = None


def _get_cache():
    global _CACHED
    if _CACHED is None and _Cache is not None:
        _CACHED = _Cache(str(CACHE_DIR))
    return _CACHED


def main():
    if len(sys.argv) < 2:
        write({"error": "Usage: python search.py <query> [--intent general] [--max 5]"})
        sys.exit(0)

    query = sys.argv[1]
    intent = 'general'
    max_r = 5

    for i in range(1, len(sys.argv)):
        a = sys.argv[i]
        if a == '--intent' and i + 1 < len(sys.argv):
            intent = sys.argv[i + 1]
        elif a == '--max' and i + 1 < len(sys.argv):
            max_r = int(sys.argv[i + 1])

    try:
        cache = _get_cache()

        # L2 / L3 cache check
        stats = None
        if cache:
            cached = cache.get(query)
            if cached:
                stats = cache.stats()
                hit_results = cached.get('results')
                if hit_results is None:
                    hit_results = [cached]
                write({
                    "query": query,
                    "intent": cached.get('intent', intent),
                    "cache_hit": True,
                    "cache_tier": cached.get('_cache_tier', 'L2'),
                    "results": hit_results if isinstance(hit_results, list) else [hit_results],
                    "cost_usd": 0.0,
                    "elapsed_ms": 0,
                    "cache_stats": stats,
                    "timestamp": datetime.now().isoformat(),
                })
                sys.exit(0)

        # Search
        detected = detect_intent(query)
        searcher = INTENT_SEARCHERS.get(detected, search_general)

        start = time.time()
        raw = searcher(query, max_r)
        elapsed = round((time.time() - start) * 1000, 1)

        results = dedup(raw)

        answer = {
            "query": query,
            "query_norm": normalize(query),
            "intent": detected,
            "results": results,
            "total_raw": len(raw),
            "total_deduped": len(results),
            "trusted_count": sum(1 for r in results if is_trusted(r['url'])),
            "search_ms": elapsed,
            "timestamp": datetime.now().isoformat(),
        }

        if cache:
            cache.set(query, answer)

        answer["cache_stats"] = cache.stats() if cache else None
        answer["cost_usd"] = 0.003  # rough estimate for one ddgs call
        write(answer)
        sys.exit(0)

    except Exception as e:
        import traceback
        write({"error": str(e), "trace": traceback.format_exc()})
        sys.exit(1)


if __name__ == '__main__':
    main()