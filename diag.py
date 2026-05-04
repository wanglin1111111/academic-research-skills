import sys, os, traceback
sys.stderr.write("[DIAG] diag.py started\n"); sys.stderr.flush()
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
sys.path.insert(0, r"C:\Users\22812\.qclaw\skills\low-cost-search\scripts")

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
    sys.exit(1)

try:
    sys.stderr.write("[DIAG] creating Cache\n"); sys.stderr.flush()
    cache = Cache(r"C:\Users\22812\.qclaw\skills\low-cost-search\references\cache")
    sys.stderr.write("[DIAG] Cache created\n"); sys.stderr.flush()

    sys.stderr.write("[DIAG] calling cache.get\n"); sys.stderr.flush()
    result = cache.get("python defaultdict tutorial")
    sys.stderr.write(f"[DIAG] cache.get done: {result is not None}\n"); sys.stderr.flush()

    if result:
        sys.stderr.write("[DIAG] cache hit, done\n"); sys.stderr.flush()
        import json
        print(json.dumps({"cache_hit": True, "tier": result.get('_cache_tier')}))
        sys.exit(0)

    sys.stderr.write("[DIAG] calling ddgs\n"); sys.stderr.flush()
    with DDGS() as ddgs:
        results = list(ddgs.text("site:stackoverflow.com python defaultdict", max_results=3))
        sys.stderr.write(f"[DIAG] ddgs got {len(results)} results\n"); sys.stderr.flush()
        import json
        print(json.dumps({"cache_hit": False, "raw_results": results}))
        sys.exit(0)

except Exception as e:
    sys.stderr.write(f"[DIAG] FATAL: {e}\n"); sys.stderr.flush()
    traceback.print_exc()
    sys.exit(1)
