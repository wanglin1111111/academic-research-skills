#!/usr/bin/env python3
"""
embedding.py — Query semantic embedding for semantic similarity.
Uses sentence-transformers for embedding generation.
"""

import os
import sys
import json
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple

# ── Setup ───────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CACHE_DIR = SKILL_DIR / "references" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

# ── Model initialization ─────────────────────────────────────────────────────

_model = None
_model_name = 'all-MiniLM-L6-v2'  # Fast, lightweight model

def get_model():
    """Lazy load embedding model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(_model_name)
            sys.stderr.write(f"[EMBEDDING] Model loaded: {_model_name}\n")
        except Exception as e:
            sys.stderr.write(f"[EMBEDDING] Model load failed: {e}\n")
            raise
    return _model

def encode(texts: List[str], normalize: bool = True) -> np.ndarray:
    """
    Encode texts to embeddings.
    
    Args:
        texts: List of texts to encode
        normalize: Whether to normalize embeddings (for cosine similarity)
    
    Returns:
        numpy array of embeddings, shape (len(texts), embedding_dim)
    """
    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    
    if normalize:
        # L2 normalize for cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / (norms + 1e-8)
    
    return embeddings

def encode_single(text: str, normalize: bool = True) -> np.ndarray:
    """Encode a single text to embedding."""
    return encode([text], normalize)[0]

def similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Compute cosine similarity between two embeddings.
    Assumes embeddings are already normalized.
    """
    return float(np.dot(embedding1, embedding2))

def similarity_batch(query_embedding: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
    """
    Compute similarities between query and multiple documents.
    
    Args:
        query_embedding: Single query embedding, shape (dim,)
        doc_embeddings: Document embeddings, shape (n_docs, dim)
    
    Returns:
        Similarity scores, shape (n_docs,)
    """
    return np.dot(doc_embeddings, query_embedding)

def find_similar(query: str, candidates: List[str], top_k: int = 5, threshold: float = 0.0) -> List[Tuple[int, float]]:
    """
    Find most similar candidates to query.
    
    Args:
        query: Query text
        candidates: List of candidate texts
        top_k: Number of top results to return
        threshold: Minimum similarity threshold
    
    Returns:
        List of (index, similarity) tuples
    """
    if not candidates:
        return []
    
    # Encode
    query_emb = encode_single(query)
    candidate_embs = encode(candidates)
    
    # Compute similarities
    similarities = similarity_batch(query_emb, candidate_embs)
    
    # Get top-k above threshold
    indexed = [(i, sim) for i, sim in enumerate(similarities) if sim >= threshold]
    indexed.sort(key=lambda x: x[1], reverse=True)
    
    return indexed[:top_k]

def semantic_deduplicate(texts: List[str], threshold: float = 0.9) -> List[int]:
    """
    Find duplicate texts based on semantic similarity.
    
    Args:
        texts: List of texts
        threshold: Similarity threshold for duplicates
    
    Returns:
        List of indices to remove (keep first occurrence)
    """
    if len(texts) < 2:
        return []
    
    embeddings = encode(texts)
    to_remove = set()
    
    for i in range(len(texts)):
        if i in to_remove:
            continue
        for j in range(i + 1, len(texts)):
            if j in to_remove:
                continue
            sim = similarity(embeddings[i], embeddings[j])
            if sim >= threshold:
                to_remove.add(j)
    
    return sorted(to_remove)

# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Embedding utilities")
    parser.add_argument("texts", nargs="+", help="Texts to encode")
    parser.add_argument("--similarity", action="store_true", help="Compute pairwise similarities")
    parser.add_argument("--top-k", type=int, default=5, help="Top-k similar")
    
    args = parser.parse_args()
    
    if args.similarity and len(args.texts) >= 2:
        # Compute similarity between first text and others
        query = args.texts[0]
        candidates = args.texts[1:]
        results = find_similar(query, candidates, top_k=args.top_k)
        
        output = {
            "query": query,
            "similarities": [
                {"index": i, "text": candidates[i], "score": round(s, 4)}
                for i, s in results
            ]
        }
    else:
        # Just encode
        embeddings = encode(args.texts)
        output = {
            "texts": args.texts,
            "embedding_dim": embeddings.shape[1],
            "embeddings": embeddings.tolist()
        }
    
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
