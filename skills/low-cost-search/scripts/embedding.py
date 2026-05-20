"""
S1: Semantic Cache + Query Embedding
Fetches from three-tier cache if available.
Only generates embedding (miss path) -- does NOT call search APIs.
"""

import json, sys, os
from datetime import datetime
from pathlib import Path

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
sys.path.insert(0, str(Path(__file__).parent))

from cache import Cache, normalize, is_nav_query

CACHE_DIR = Path(__file__).parent.parent / "references" / "cache"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python embedding.py <query>"}))
        sys.exit(1)

    query = sys.argv[1]
    cache_dir = CACHE_DIR
    for i, arg in enumerate(sys.argv[2:]):
        if arg == "--cache-dir" and i + 2 < len(sys.argv):
            cache_dir = sys.argv[sys.argv.index(arg) + 1]

    cache = Cache(str(cache_dir))

    cached = cache.get(query)
    if cached:
        out = {
            "query": query,
            "cache_hit": True,
            "result": cached,
            "cache_tier": cached.get("_cache_tier", "unknown"),
            "cache_similarity": cached.get("_cache_similarity", 1.0),
            "cost_saved": "S1+S2+S3+S4+S5_all_skipped",
            "timestamp": datetime.now().isoformat(),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    from cache import HAS_ST, _get_model, cosine_sim

    out = {
        "query": query,
        "query_norm": normalize(query),
        "cache_hit": False,
        "is_nav": is_nav_query(query),
        "embedding_status": "pending_S2",
        "timestamp": datetime.now().isoformat()
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
