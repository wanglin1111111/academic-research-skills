"""
search_client.py — HTTP client for search_server.py + fallback subprocess.

Usage:
  from search_client import search
  result = search("python list comprehension tutorial", max_results=5)
  # result: dict with results[], intent, cache_hit, search_ms, etc.
"""
import subprocess
import json
import time
import socket
import urllib.request
import urllib.error
from pathlib import Path

PYTHON = r"C:\Program Files\AutoClaw\resources\python\python.exe"
SEARCH_SERVER = Path(__file__).parent / "search_server.py"
SEARCH_PY = Path(__file__).parent / "search.py"
CACHE_DIR = Path(__file__).parent.parent / "references" / "cache"
SERVER_PORT = 18765
_SERVER_PID = None  # track background server process


def _server_running() -> bool:
    """Check if server is already listening on port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect(("127.0.0.1", SERVER_PORT))
        sock.close()
        return True
    except (socket.timeout, socket.error, ConnectionRefusedError):
        return False


def _health_check() -> bool:
    """Returns True if server is responding to /health."""
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{SERVER_PORT}/health",
            headers={"User-Agent": "search-client/1.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.read() == b"ok"
    except Exception:
        return False


def _start_server(warmup: bool = True) -> int:
    """Start search_server.py as background process. Returns PID."""
    args = [PYTHON, str(SEARCH_SERVER), "--port", str(SERVER_PORT)]
    if warmup:
        args.append("--warmup")
    # Start without waiting - let it warm up in background
    proc = subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    )
    return proc.pid


def _http_search(query: str, max_results: int = 5) -> dict:
    """Call running search_server via HTTP POST."""
    payload = json.dumps({"query": query, "max_results": max_results}).encode("utf-8")
    req = urllib.request.Request(
        f"http://127.0.0.1:{SERVER_PORT}/search",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "search-client/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _read_latest_result() -> dict | None:
    """Read the most recent last_result_*.json from cache dir."""
    files = sorted(CACHE_DIR.glob("last_result_*.json"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if files:
        try:
            return json.loads(files[0].read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def _subprocess_search(query: str, max_results: int = 5, intent: str = None) -> dict:
    """Fallback: run search.py as subprocess. Returns parsed result."""
    args = [PYTHON, str(SEARCH_PY), query, "--max", str(max_results)]
    if intent:
        args += ["--intent", intent]
    try:
        # Clean old result files
        for f in CACHE_DIR.glob("last_result_*.json"):
            try:
                f.unlink()
            except Exception:
                pass
        r = subprocess.run(
            args,
            capture_output=True,
            timeout=90,
            cwd=str(SEARCH_PY.parent),
        )
        # Read result from cache file
        result = _read_latest_result()
        if result:
            return result
        # Fallback: parse stderr
        if r.returncode == 0 and r.stderr:
            lines = [l for l in r.stderr.decode("utf-8", errors="replace").split("\n")
                     if "[ERROR]" in l or "[SEARCH]" in l]
            return {"query": query, "error": "no_result_file", "stderr_lines": lines[:5]}
        return {"query": query, "error": f"exit_code={r.returncode}"}
    except subprocess.TimeoutExpired:
        return {"query": query, "error": "timeout", "intent": intent}
    except Exception as e:
        return {"query": query, "error": str(e)}


def search(query: str, max_results: int = 5, warmup: bool = False, auto_start: bool = True) -> dict:
    """
    Main entry point. Tries HTTP server first, falls back to subprocess.

    Args:
        query: search query string
        max_results: max number of results
        warmup: if True, start the server with --warmup flag (slower first call)
        auto_start: if True, automatically start server if not running (default: True)

    Returns:
        dict with keys: query, intent, results, cache_hit, cache_tier,
                        search_ms, cost_usd, cache_stats, error
    """
    # 1. Try HTTP server
    if _server_running():
        try:
            return _http_search(query, max_results)
        except Exception:
            pass  # fall through to auto-start

    # 2. Auto-start server if enabled and not running
    if auto_start and not _server_running():
        _start_server(warmup=True)
        # Wait for server to be ready (max 20 seconds)
        for _ in range(40):
            time.sleep(0.5)
            if _health_check():
                break
        # Try HTTP again
        if _server_running():
            try:
                return _http_search(query, max_results)
            except Exception:
                pass

    # 3. Fallback to subprocess
    return _subprocess_search(query, max_results)
