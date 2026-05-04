"""
S1: Semantic Cache + Query Embedding
Fetches from three-tier cache if available.
Only generates embedding (miss path) — does NOT call search APIs.

Usage:
  python embedding.py "<query>" [--cache-dir <dir>]

Output:
  - cache hit → returns cached result directly (zero cost)
  - cache miss → returns { query, embedding, cacheable: true } for S2/S3
"""

import json
import sys
import os
from datetime import datetime

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cache import Cache, normalize, is_nav_query

PYTHON = "C:\\Program Files\\AutoClaw\\resources\\python\\python.exe"
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'references', 'cache')


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python embedding.py <query>"}))
        sys.exit(1)

    query = sys.argv[1]
    cache_dir = CACHE_DIR

    for i, arg in enumerate(sys.argv[2:]):
        if arg == '--cache-dir' and i + 2 < len(sys.argv):
            cache_dir = sys.argv[sys.argv.index(arg) + 1]

    cache = Cache(cache_dir)

    # ── Try three-tier cache first ──────────────────────────────────────
    cached = cache.get(query)
    if cached:
        out = {
            "query": query,
            "cache_hit": True,
            "result": cached,
            "cache_tier": cached.get('_cache_tier', 'unknown'),
            "cache_similarity": cached.get('_cache_similarity', 1.0),
            "cost_saved": "S1+S2+S3+S4+S5_all_skipped",
            "timestamp": datetime.now().isoformat(),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    # ── Cache miss: generate embedding, mark as needing search ───────────
    from cache import HAS_ST, _EM_MODEL, cosine_sim

    out = {
        "query": query,
        "query_norm": normalize(query),
        "cache_hit": False,
        "is_nav": is_nav_query(query),
        "result": None,  # Will be filled by S3 after search
        "timestamp": datetime.now().isoformat(),
    }

    if HAS_ST and not is_nav_query(query):
        try:
            emb = _EM_MODEL.encode(query, convert_to_numpy=True).tolist()
            out["embedding"] = emb
            out["embedding_model"] = "sentence-transformers/all-MiniLM-L6-v2"
            out["cost_note"] = "embedding_generated_local (zero cost)"
        except Exception as e:
            out["embedding_error"] = str(e)
            out["embedding_model"] = None
    else:
        out["embedding"] = None
        out["embedding_model"] = None

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
