"""
Unified Cache Layer - Three-tier cache for maximum hit rate + minimum API cost.
Tiers:
  L1 (Memory):  In-process LRU dict, TTL 1h, max 200 entries
  L2 (Semantic): Embedding similarity >= 0.85, 30-day TTL, max 5000 entries
  L3 (Raw):      Normalized query hash key, 7-day TTL, max 20000 entries

All tiers are write-through. L1 hit = zero cost. L2 hit = skip S3. L3 = skip S4 rerank.

Usage:
  from cache import Cache
  cache = Cache(cache_dir)
  result = cache.get(query)         # returns cached SearchResult or None
  cache.set(query, search_result)   # store after successful search
"""

import json
import os
import time
import hashlib
import re
import math
from datetime import datetime, timedelta, timezone
from collections import OrderedDict
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

try:
    from sentence_transformers import SentenceTransformer
    HAS_ST = True
    _ST_LOADED = False
    _EM_MODEL = None

    def _get_model():
        global _EM_MODEL, _ST_LOADED
        if not _ST_LOADED:
            _EM_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            _ST_LOADED = True
        return _EM_MODEL
except Exception:
    HAS_ST = False
    _get_model = None


# ── Normalization ──────────────────────────────────────────────────────────

NAV_BLACKLIST = {
    # Queries that are commands, not searches — never cache their results
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
    """Canonical form for cache key: lower, strip, collapse spaces."""
    q = query.lower().strip()
    q = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', q)
    q = re.sub(r'\s+', ' ', q).strip()
    return q


def is_nav_query(query: str) -> bool:
    """True if query looks like a command/navigation, not a search."""
    q = query.strip().lower()
    if q in NAV_BLACKLIST:
        return True
    if any(q.startswith(p.lower()) for p in NAV_PREFIXES):
        return True
    return False


def query_hash(q: str) -> str:
    """Stable 8-char hex ID for a normalized query."""
    return hashlib.md5(q.encode('utf-8')).hexdigest()[:8]


def cosine_sim(a: list, b: list) -> float:
    """Pure-Python cosine similarity, no numpy required."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ── L1: In-memory LRU ─────────────────────────────────────────────────────

class L1Cache:
    """Process-local LRU. TTL 1h, max 200 entries."""

    def __init__(self, maxsize: int = 200, ttl_seconds: int = 3600):
        self._store: OrderedDict[str, dict] = OrderedDict()
        self.maxsize = maxsize
        self.ttl = ttl_seconds
        self._hits = 0
        self._misses = 0

    def get(self, norm_q: str) -> Optional[dict]:
        key = query_hash(norm_q)
        entry = self._store.get(key)
        if entry is None:
            self._misses += 1
            return None
        if time.time() - entry['_l1_ts'] > self.ttl:
            del self._store[key]
            self._misses += 1
            return None
        # Move to end (most-recently-used)
        self._store.move_to_end(key)
        self._hits += 1
        return entry['result']

    def set(self, norm_q: str, result: dict):
        key = query_hash(norm_q)
        if key in self._store:
            self._store.move_to_end(key)
        else:
            if len(self._store) >= self.maxsize:
                self._store.popitem(last=False)
        self._store[key] = {
            '_l1_ts': time.time(),
            'result': result,
        }

    def stats(self) -> dict:
        total = self._hits + self._misses
        return {
            'l1_hits': self._hits,
            'l1_misses': self._misses,
            'l1_hit_rate': round(self._hits / total, 3) if total else 0.0,
            'l1_size': len(self._store),
        }


# ── L2: Semantic Cache (Embedding similarity) ─────────────────────────────

class L2Cache:
    """
    Disk-backed semantic cache.
    Stores query embedding + result. On lookup: embed → top-K cosine → return best ≥ threshold.
    Threshold lowered to 0.85 to catch rephrased queries.
    """

    def __init__(
        self,
        cache_path: str,
        threshold: float = 0.85,
        max_entries: int = 5000,
        ttl_days: int = 30,
    ):
        self.path = Path(cache_path)
        self.threshold = threshold
        self.max_entries = max_entries
        self.ttl_days = ttl_days
        self._hits = 0
        self._misses = 0
        self._load_index()

    def _load_index(self):
        """Load existing entries into memory."""
        self._entries: list[dict] = []
        if not self.path.exists():
            return
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        self._entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except Exception:
            self._entries = []

    def _save_all(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            for e in self._entries:
                f.write(json.dumps(e, ensure_ascii=False) + '\n')

    def _prune(self):
        """Remove entries older than TTL and cap at max_entries."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.ttl_days)
        cutoff_str = cutoff.isoformat()
        before = len(self._entries)
        self._entries = [
            e for e in self._entries
            if e.get('timestamp', '') > cutoff_str
        ]
        # Keep most recent within max_entries
        self._entries = self._entries[-self.max_entries:]
        if len(self._entries) < before:
            self._save_all()

    def get(self, query: str) -> Optional[dict]:
        if not HAS_ST or not self._entries:
            self._misses += 1
            return None

        try:
            emb = _get_model().encode(query, convert_to_numpy=True).tolist()
        except Exception:
            self._misses += 1
            return None

        best_score = 0.0
        best_entry = None

        for entry in self._entries:
            cached_emb = entry.get('embedding')
            if not cached_emb:
                continue
            score = cosine_sim(emb, cached_emb)
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_score >= self.threshold and best_entry:
            self._hits += 1
            result = best_entry.get('result')
            if result:
                result['_cache_tier'] = 'L2_semantic'
                result['_cache_similarity'] = round(best_score, 4)
            return result

        self._misses += 1
        return None

    def set(self, query: str, result: dict):
        if not HAS_ST or is_nav_query(query):
            return

        try:
            emb = _get_model().encode(query, convert_to_numpy=True).tolist()
        except Exception:
            return

        norm_q = normalize(query)

        # Skip if duplicate (same normalized query already in L2)
        for existing in self._entries:
            if normalize(existing.get('query', '')) == norm_q:
                return  # Don't overwrite fresh result with older one

        entry = {
            'query': query,
            'query_norm': norm_q,
            'embedding': emb,
            'result': result,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }

        self._entries.append(entry)

        # Prune every 50 writes to avoid constant re-writes
        if len(self._entries) % 50 == 0:
            self._prune()
        else:
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def stats(self) -> dict:
        total = self._hits + self._misses
        return {
            'l2_hits': self._hits,
            'l2_misses': self._misses,
            'l2_hit_rate': round(self._hits / total, 3) if total else 0.0,
            'l2_entries': len(self._entries),
        }


# ── L3: Raw (normalized key → result) ────────────────────────────────────

class L3Cache:
    """
    Disk-backed exact-match cache keyed by normalized query.
    TTL 7 days, max 20k entries. Low memory footprint.
    """

    def __init__(
        self,
        cache_path: str,
        max_entries: int = 20000,
        ttl_days: int = 7,
    ):
        self.path = Path(cache_path)
        self.max_entries = max_entries
        self.ttl_days = ttl_days
        self._hits = 0
        self._misses = 0
        self._load_index()

    def _load_index(self):
        self._index: dict[str, dict] = {}
        if not self.path.exists():
            return
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        key = entry.get('query_norm', '')
                        if key:
                            self._index[key] = entry
                    except json.JSONDecodeError:
                        continue
        except Exception:
            self._index = {}

    def _is_fresh(self, entry: dict) -> bool:
        ts = entry.get('timestamp', '')
        if not ts:
            return False
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            age = datetime.now(timezone.utc) - dt
            return age < timedelta(days=self.ttl_days)
        except Exception:
            return False

    def get(self, query: str) -> Optional[dict]:
        norm_q = normalize(query)
        entry = self._index.get(norm_q)
        if entry is None:
            self._misses += 1
            return None
        if not self._is_fresh(entry):
            del self._index[norm_q]
            self._misses += 1
            return None
        self._hits += 1
        result = entry.get('result', {})
        result['_cache_tier'] = 'L3_raw'
        return result

    def set(self, query: str, result: dict):
        if is_nav_query(query):
            return
        norm_q = normalize(query)
        entry = {
            'query_norm': norm_q,
            'result': result,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }
        self._index[norm_q] = entry

        # Periodic prune
        if len(self._index) % 100 == 0:
            self._prune_and_save()
        else:
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def _prune_and_save(self):
        fresh = {k: v for k, v in self._index.items() if self._is_fresh(v)}
        # Keep most recent up to max_entries
        sorted_entries = sorted(
            fresh.items(),
            key=lambda x: x[1].get('timestamp', ''),
            reverse=True
        )
        self._index = dict(sorted_entries[:self.max_entries])
        with open(self.path, 'w', encoding='utf-8') as f:
            for entry in self._index.values():
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def stats(self) -> dict:
        total = self._hits + self._misses
        return {
            'l3_hits': self._hits,
            'l3_misses': self._misses,
            'l3_hit_rate': round(self._hits / total, 3) if total else 0.0,
            'l3_entries': len(self._index),
        }


# ── Unified Cache ─────────────────────────────────────────────────────────

class Cache:
    """
    Three-tier unified cache. Tries L1 → L2 → L3 in order.
    L1: in-process LRU
    L2: semantic similarity
    L3: exact normalized match
    """

    def __init__(self, cache_dir: str):
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)

        self.l1 = L1Cache()
        self.l2 = L2Cache(str(cache_dir / 'l2_semantic.jsonl'))
        self.l3 = L3Cache(str(cache_dir / 'l3_raw.jsonl'))

    def get(self, query: str) -> Optional[dict]:
        norm_q = normalize(query)
        # L1
        r = self.l1.get(norm_q)
        if r:
            r['_cache_tier'] = 'L1_memory'
            return r
        # L2
        r = self.l2.get(query)
        if r:
            return r
        # L3
        r = self.l3.get(query)
        if r:
            return r
        return None

    def set(self, query: str, result: dict):
        norm_q = normalize(query)
        # Write to all tiers
        self.l1.set(norm_q, result)
        self.l2.set(query, result)
        self.l3.set(query, result)

    def stats(self) -> dict:
        return {
            **self.l1.stats(),
            **self.l2.stats(),
            **self.l3.stats(),
        }


# ── CLI entry point ───────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print("Usage: python cache.py get|set <query> [result_json]")
        sys.exit(1)

    op = sys.argv[1]
    query = sys.argv[2]

    skill_dir = Path(__file__).parent.parent
    cache_dir = skill_dir / 'references' / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache = Cache(str(cache_dir))

    if op == 'get':
        result = cache.get(query)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"hit": False, "query": query}))
    elif op == 'set':
        result = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        cache.set(query, result)
        print(json.dumps({"stored": True, "query": query}))
    elif op == 'stats':
        print(json.dumps(cache.stats(), indent=2))


if __name__ == '__main__':
    main()
