"""Unified Search: intent detection + DuckDuckGo search."""
import sys, os, json, time, re
from datetime import datetime
from pathlib import Path

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
SKILL_DIR = Path(__file__).parent.parent
CACHE_DIR = SKILL_DIR / "references" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(Path(__file__).parent))

try:
    from cache import Cache, normalize
    _Cache = Cache
except Exception:
    _Cache = None
    normalize = lambda q: re.sub(r"\s+", " ", q.lower().strip())

try:
    from ddgs import DDGS as _DDGS
except Exception:
    _DDGS = None

EN_CODE = {"python","javascript","java","c++","golang","rust","typescript","react","vue","sql","git","docker","api","function","class","error","debug"}
ZH_CODE = {"代码","编程","函数","方法","报错","调试","模块","包","def","return","async","await","list","dict"}

def detect_intent(query: str) -> str:
    q = query.lower()
    has_zh = bool(re.search(r"[\u4e00-\u9fff]", query))
    if has_zh and any(kw in query for kw in ZH_CODE):
        return "code"
    if not has_zh and any(kw in q for kw in EN_CODE):
        return "code"
    if any(kw in query for kw in ["论文","paper","arxiv","学术","研究"]):
        return "academic"
    if any(kw in query for kw in ["新闻","news","最新","今日","昨天"]):
        return "web_news"
    if any(kw in query for kw in ["对比","测评","review","vs","哪个好"]):
        return "review"
    return "general"

def search_ddg(query: str, intent: str = "general", max_r: int = 5) -> list:
    if not _DDGS:
        return []
    results = []
    seen = set()
    try:
        with _DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_r * 2):
                url = r.get("href") or r.get("url") or ""
                if url in seen:
                    continue
                seen.add(url)
                txt = (r.get("body") or r.get("description") or "")[:300]
                results.append({"title": r.get("title","")[:200], "url": url, "snippet": txt, "source": "ddg"})
                if len(results) >= max_r:
                    break
    except Exception:
        pass
    return results

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python search.py <query> [max_results]"}))
        sys.exit(1)
    query = sys.argv[1]
    max_r = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    intent = detect_intent(query)
    cache = _Cache(str(CACHE_DIR)) if _Cache else None
    if cache:
        cached = cache.get(query)
        if cached:
            print(json.dumps({"query": query, "intent": intent, "cache_hit": True, "results": cached.get("results",[])}))
            return
    results = search_ddg(query, intent, max_r)
    out = {"query": query, "intent": intent, "cache_hit": False, "results": results, "timestamp": datetime.now().isoformat()}
    if cache and results:
        cache.set(query, out)
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
