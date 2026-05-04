"""
install_hook.py - Post-install script for low-cost-search skill.

This script runs automatically after skill installation to:
1. Initialize the knowledge base
2. Start the search server in background

User doesn't need to manually run anything!
"""
import subprocess
import sys
import time
import socket
from pathlib import Path

PYTHON = sys.executable
SKILL_DIR = Path(__file__).parent.parent
SERVER_SCRIPT = SKILL_DIR / "scripts" / "search_server.py"
KB_SCRIPT = SKILL_DIR / "scripts" / "knowledge_base.py"
PORT = 18765


def _server_running() -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect(("127.0.0.1", PORT))
        sock.close()
        return True
    except:
        return False


def main():
    print("\n[low-cost-search] Post-install setup...")

    # 1. Initialize knowledge base
    try:
        sys.path.insert(0, str(SKILL_DIR / "scripts"))
        from knowledge_base import init_knowledge_base
        init_knowledge_base()
        print("[OK] Knowledge base initialized")
    except Exception as e:
        print(f"[WARN] Knowledge base init failed: {e}")

    # 2. Start server if not running
    if _server_running():
        print("[OK] Server already running on port 18765")
        return

    print("[INFO] Starting search server (warmup ~10s)...")
    try:
        proc = subprocess.Popen(
            [PYTHON, str(SERVER_SCRIPT), "--warmup", "--port", str(PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
        # Wait for server to start
        for i in range(30):
            time.sleep(0.5)
            if _server_running():
                print(f"[OK] Server started on port {PORT} (PID: {proc.pid})")
                print("\n✅ Ready to use! Just call search() - no manual startup needed.")
                return
        print("[WARN] Server start timeout, will start on first search")
    except Exception as e:
        print(f"[WARN] Server start failed: {e}")


if __name__ == "__main__":
    main()
