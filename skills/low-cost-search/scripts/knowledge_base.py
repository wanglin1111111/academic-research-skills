#!/usr/bin/env python3
"""
knowledge_base.py — Local knowledge base with vector retrieval.
Provides pre-built knowledge for common queries.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# ── Paths ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
KB_DIR = SKILL_DIR / "references" / "knowledge_base"
KB_DIR.mkdir(parents=True, exist_ok=True)

# ── Pre-built knowledge entries ─────────────────────────────────────────────

PRESET_KNOWLEDGE = [
    {
        "id": "kb-python-list-comprehension",
        "query_pattern": ["python list comprehension", "列表推导式", "python list"],
        "title": "Python List Comprehension Guide",
        "content": "List comprehension provides a concise way to create lists. Syntax: [expression for item in iterable if condition]. Example: squares = [x**2 for x in range(10)]. Benefits: more readable, faster than loops for simple operations.",
        "source": "preset",
        "tags": ["python", "list", "comprehension", "syntax"]
    },
    {
        "id": "kb-python-defaultdict",
        "query_pattern": ["python defaultdict", "defaultdict", "字典默认值"],
        "title": "Python defaultdict Usage",
        "content": "defaultdict from collections module provides default values for missing keys. Example: from collections import defaultdict; d = defaultdict(list); d['key'].append('value'). Common defaults: list, int, set, str.",
        "source": "preset",
        "tags": ["python", "dict", "defaultdict", "collections"]
    },
    {
        "id": "kb-git-commands",
        "query_pattern": ["git commands", "git 命令", "git basics", "git 基础"],
        "title": "Essential Git Commands",
        "content": "Basic commands: git init, git add, git commit -m 'msg', git push, git pull, git status, git log. Branching: git branch, git checkout -b, git merge. Undo: git reset, git revert, git stash.",
        "source": "preset",
        "tags": ["git", "commands", "version control"]
    },
    {
        "id": "kb-docker-basics",
        "query_pattern": ["docker basics", "docker 基础", "docker commands", "docker 命令"],
        "title": "Docker Basic Commands",
        "content": "Key commands: docker run, docker build, docker ps, docker images, docker stop, docker rm, docker exec. Dockerfile: FROM, RUN, COPY, CMD, EXPOSE. Compose: docker-compose up, down.",
        "source": "preset",
        "tags": ["docker", "container", "commands"]
    },
    {
        "id": "kb-python-async",
        "query_pattern": ["python async", "python 异步", "asyncio", "await"],
        "title": "Python Async/Await Guide",
        "content": "async def defines coroutine. await pauses execution until result ready. asyncio.run() executes coroutine. asyncio.gather() runs multiple coroutines concurrently. Use for I/O-bound operations.",
        "source": "preset",
        "tags": ["python", "async", "asyncio", "concurrent"]
    },
]

# ── Knowledge Base class ───────────────────────────────────────────────────

class KnowledgeBase:
    def __init__(self, kb_dir: Path = None):
        self.kb_dir = kb_dir or KB_DIR
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        self.entries = self._load_entries()
    
    def _load_entries(self) -> List[Dict]:
        """Load all knowledge entries."""
        entries = PRESET_KNOWLEDGE.copy()
        
        # Load from files
        for json_file in self.kb_dir.glob("*.json"):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    entries.extend(data)
                elif isinstance(data, dict):
                    entries.append(data)
            except Exception:
                pass
        
        return entries
    
    def _match_pattern(self, query: str, patterns: List[str]) -> float:
        """Check if query matches any pattern."""
        query_lower = query.lower()
        max_score = 0.0
        
        for pattern in patterns:
            pattern_lower = pattern.lower()
            
            # Exact match
            if query_lower == pattern_lower:
                return 1.0
            
            # Contains
            if pattern_lower in query_lower:
                score = len(pattern_lower) / len(query_lower)
                max_score = max(max_score, score)
            
            # Query contains pattern
            if query_lower in pattern_lower:
                score = len(query_lower) / len(pattern_lower) * 0.8
                max_score = max(max_score, score)
        
        return max_score
    
    def search(self, query: str, threshold: float = 0.5) -> List[Dict]:
        """Search knowledge base for matching entries."""
        results = []
        
        for entry in self.entries:
            patterns = entry.get("query_pattern", [])
            score = self._match_pattern(query, patterns)
            
            if score >= threshold:
                results.append({
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "content": entry.get("content"),
                    "source": entry.get("source", "kb"),
                    "tags": entry.get("tags", []),
                    "match_score": round(score, 3)
                })
        
        # Sort by match score
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        return results
    
    def add_entry(self, entry: Dict) -> None:
        """Add new knowledge entry."""
        entry["added_at"] = datetime.now().isoformat()
        self.entries.append(entry)
        
        # Save to file
        entry_file = self.kb_dir / f"{entry.get('id', 'custom')}.json"
        entry_file.write_text(json.dumps(entry, ensure_ascii=False), encoding="utf-8")
    
    def get_entry(self, entry_id: str) -> Optional[Dict]:
        """Get specific entry by ID."""
        for entry in self.entries:
            if entry.get("id") == entry_id:
                return entry
        return None

# ── Vector retrieval (optional, requires sentence-transformers) ─────────────

class VectorKnowledgeBase(KnowledgeBase):
    """Knowledge base with semantic vector retrieval."""
    
    def __init__(self, kb_dir: Path = None):
        super().__init__(kb_dir)
        self.embeddings = None
        self.model = None
    
    def _init_model(self):
        """Initialize embedding model."""
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"[KB] Model init failed: {e}")
    
    def _build_embeddings(self):
        """Build embeddings for all entries."""
        if self.embeddings is None and self.model:
            contents = [e.get("content", "") for e in self.entries]
            self.embeddings = self.model.encode(contents)
    
    def semantic_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Semantic search using embeddings."""
        self._init_model()
        if not self.model:
            return self.search(query)
        
        self._build_embeddings()
        if self.embeddings is None:
            return self.search(query)
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Compute similarities
        from numpy import dot
        from numpy.linalg import norm
        similarities = []
        for i, entry_emb in enumerate(self.embeddings):
            sim = dot(query_embedding[0], entry_emb) / (norm(query_embedding[0]) * norm(entry_emb))
            similarities.append((i, sim))
        
        # Sort and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        results = []
        for i, sim in similarities[:top_k]:
            entry = self.entries[i]
            results.append({
                "id": entry.get("id"),
                "title": entry.get("title"),
                "content": entry.get("content"),
                "source": entry.get("source", "kb"),
                "tags": entry.get("tags", []),
                "semantic_score": round(sim, 3)
            })
        
        return results

# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python knowledge_base.py <query> [threshold]"}))
        sys.exit(1)
    
    query = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    
    kb = KnowledgeBase()
    results = kb.search(query, threshold)
    
    print(json.dumps({
        "query": query,
        "threshold": threshold,
        "found": len(results),
        "results": results
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()