import sys, ost.py — HTTP client for search_server.py + fallback subprocess.
Usage:
  from search_client import search
  result = search("python list comprehension tutorial", max_results=5)
"""

import subprocess
import json
import time
import socket
import urllib.request
import urllib.error
from pathlib import Path

# Use current Python interpreter (not hardcoded)
PYTHON = sys.executable if __import__("sys").executable else "python3"
SEARCH_SERVER = Path(__file__).parent / "search_server.py"
SEARCH_PY = Path(__file__).parent / "search.py"
CACHE_DIR = Path(__file__).parent.parent / "references" / "cache"
SERVER_PORT = 18765
_SERVER_PID = None

def _server_running() -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect(("127.0.0.1", SERVER_PORT))
        sock.close()
        return True
    except (socket.timeout, socket.error, ConnectionRefusedError):
        return False

def _health_check() -> bool:
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
    args = [PYTHON, str(SEARCH_SERVER), "--port", str(SERVER_PORT)]
    if warmup:
        args.append("--warmup")
    proc = subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    )
    return proc.pid

def _http_search(query: str, max_results: int = 5) -> dict:
    try:
        payload = json.dumps({"query": query, "max_results": max_results}).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{SERVER_PORT}/search",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e), "results": []}

def search(query: str, max_results: int = 5, timeout: int = 30) -> dict:
    """Main search entry point."""
    if not _server_running():
        _start_server(warmup=True)
        for _ in range(timeout * 2):
            time.sleep(0.5)
            if _health_check():
                break
    return _http_search(query, max_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_client.py <query> [max_results]")
        sys.exit(1)
    q = sys.argv[1]
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    result = search(q, m)
    print(json.dumps(result, ensure_ascii=False, indent=2))
