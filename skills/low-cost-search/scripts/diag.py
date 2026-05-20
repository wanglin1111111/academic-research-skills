import sys, os, traceback, json script for low-cost-search skill.
Tests imports and cache functionality.
Run: python diag.py
"""
import sys, os, traceback

# ── Add skill scripts to path (relative) ─────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

sys.stderr.write("[DIAG] diag.py started\n"); sys.stderr.flush()

try:
    sys.stderr.write("[DIAG] importing cache\n"); sys.stderr.flush()
    from cache import Cache
    sys.stderr.write("[DIAG] cache ok\n"); sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[DIAG] cache import failed: {e}\n"); sys.stderr.flush()
    traceback.print_exc()
    sys.exit(1)

try:
    sys.stderr.write("[DIAG] importing ddgs\n"); sys.stderr.flush()
    from ddgs import DDGS
    sys.stderr.write("[DIAG] ddgs ok\n"); sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[DIAG] ddgs import failed: {e}\n"); sys.stderr.flush()
    traceback.print_exc()

try:
    sys.stderr.write("[DIAG] creating Cache\n"); sys.stderr.flush()
    cache_dir = SKILL_DIR / "references" / "cache"
    cache = Cache(str(cache_dir))
    sys.stderr.write("[DIAG] Cache created\n"); sys.stderr.flush()

    sys.stderr.write("[DIAG] calling cache.get\n"); sys.stderr.flush()
    result = cache.get("python defaultdict tutorial")
    sys.stderr.write(f"[DIAG] cache.get done: {result is not None}\n"); sys.stderr.flush()

    if result:
        sys.stderr.write("[DIAG] cache hit, done\n"); sys.stderr.flush()
        import json
        print(json.dumps({"cache_hit": True, "tier": result.get("_cache_tier")}))
        sys.exit(0)

    sys.stderr.write("[DIAG] cache miss - all basic tests passed\n"); sys.stderr.flush()
    print(json.dumps({"cache_hit": False, "status": "diag_passed"}))
    sys.exit(0)

except Exception as e:
    sys.stderr.write(f"[DIAG] FATAL: {e}\n"); sys.stderr.flush()
    traceback.print_exc()
    import json
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
