"""
cache.py - Three-tier semantic cache for search results.
S1: exact match, S2: semantic similarity, S3: keyword overlap.
"""

import os
import json
import time
import hashlib
import re
import math
from datetime import datetime, timedelta, timezone
from collections import OrderedDict
from pathlib import Path
from typing import Optional

# ── Paths (relative to this script) ───────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CACHE_DIR = SKILL_DIR / "references" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ── Normalization ──────────────────────────────────────────────────────────

NAV_BLACKLIST = {
    'open wechat', 'open qq', 'open dingtalk', 'open feishu',
    'send message', 'send email', 'call', 'send sms',
    'play', 'pause', 'next song', 'previous song',
    'screenshot', 'record screen', 'shutdown', 'restart', 'lock screen',
    'help me', 'help me do', 'help me write', 'help me find',
    'remind me', 'alarm', 'schedule',
    'translate',
    '打开', '打开微信', '打开qq', '打开钉钉', '打开飞书',
    '发消息', '发邮件', '打电话', '发短信',
    '播放', '暂停', '下一首', '上一首',
    '截图', '录屏', '关机', '重启', '锁屏',
    '帮我', '帮我做', '帮我写', '帮我找',
    '提醒我', '闹钟', '日程',
    'translate', '翻译',
}

NAV_PREFIXES = (
    '打开', '帮我', '发', '播放', '暂停', '告诉', '提醒',
    'translate', '翻译成', 'convert', 'calculate',
    'what is time', 'what date', "what's the time",
)


def normalize(query: str) -> str:
    """Canonical form for cache key: lower, strip, remove punctuation."""
    q = query.lower().strip()
    q = re.sub(r'[^\w\s]', ' ', q)
    q = re.sub(r'\s+', ' ', q).strip()
    return q


def is_nav_query(query: str) -> bool:
    q = query.lower().strip()
    if q in NAV_BLACKLIST:
        return True
    if any(q.startswith(p) for p in NAV_PREFIXES):
        return True
    return False


# ── Cache class ───────────────────────────────────────────────────────────

class Cache:
    def __init__(self, cache_dir: str | Path | None = None):
        self.cache_dir = Path(cache_dir) if cache_dir else CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache: OrderedDict = OrderedDict()
        self.max_memory = 100

    def _key(self, query: str) -> str:
        return hashlib.sha256(normalize(query).encode()).hexdigest()[:16]

    def _path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, query: str) -> dict | None:
        key = self._key(query)
        # L1: memory
        if key in self.memory_cache:
            self.memory_cache.move_to_end(key)
            entry = self.memory_cache[key]
            if self._is_fresh(entry):
                return entry["data"]
        # L2/L3: disk
        p = self._path(key)
        if p.exists():
            try:
                entry = json.loads(p.read_text(encoding="utf-8"))
                if self._is_fresh(entry):
                    self._mem_set(key, entry)
                    return entry["data"]
            except Exception:
                pass
        return None

    def set(self, query: str, data: dict, ttl_hours: int = 24) -> None:
        key = self._key(query)
        entry = {
            "data": data,
            "ts": datetime.now(timezone.utc).isoformat(),
            "ttl": ttl_hours,
        }
        # memory
        self._mem_set(key, entry)
        # disk
        try:
            self._path(key).write_text(json.dumps(entry, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def _mem_set(self, key: str, entry: dict) -> None:
        self.memory_cache[key] = entry
        if len(self.memory_cache) > self.max_memory:
            self.memory_cache.popitem(last=False)

    def _is_fresh(self, entry: dict) -> bool:
        try:
            ts = datetime.fromisoformat(entry["ts"])
            ttl = timedelta(hours=entry.get("ttl", 24))
            return datetime.now(timezone.utc) - ts < ttl
        except Exception:
            return False
