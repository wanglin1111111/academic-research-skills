"""
S4: Local Reranker - Rerank search results using a cross-encoder.
Usage: python rerank.py "<query>" '<results_json>'
results_json: JSON array of {"title": "...", "url": "...", "snippet": "..."}
Output: Reranked JSON array with scores
"""

import json
import sys
import os
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


def rerank_with_model(query: str, results: list) -> list:
    """Rerank using BAAI/bge-reranker-base cross-encoder."""
    try:
        from sentence_transformers import CrossEncoder
    except ImportError:
        raise RuntimeError("sentence-transformers not installed. Run: pip install sentence-transformers")

    model = CrossEncoder('BAAI/bge-reranker-base')

    pairs = [(query, f"{r.get('title', '')} {r.get('snippet', '')}") for r in results]
    scores = model.predict(pairs).tolist()

    for i, result in enumerate(results):
        result['rerank_score'] = round(float(scores[i]), 4)

    # Filter low-score results
    filtered = [r for r in results if r['rerank_score'] >= 0.6]

    # If all filtered out, keep top 3 regardless
    if not filtered:
        filtered = sorted(results, key=lambda x: x['rerank_score'], reverse=True)[:3]

    return sorted(filtered, key=lambda x: x['rerank_score'], reverse=True)


def rerank_simple(query: str, results: list) -> list:
    """
    Simple keyword-based reranking fallback (no model required).
    Scores based on query term overlap with title + snippet.
    """
    import re
    query_terms = set(re.findall(r'\w+', query.lower()))

    for result in results:
        text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
        text_terms = set(re.findall(r'\w+', text))
        overlap = len(query_terms & text_terms)
        result['rerank_score'] = round(overlap / max(len(query_terms), 1), 4)

    return sorted(results, key=lambda x: x['rerank_score'], reverse=True)


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python rerank.py <query> <results_json>"}))
        sys.exit(1)

    query = sys.argv[1]
    try:
        results = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid results JSON: {e}"}))
        sys.exit(1)

    if not results:
        print(json.dumps([]))
        return

    try:
        reranked = rerank_with_model(query, results)
        method = "cross_encoder"
    except Exception:
        reranked = rerank_simple(query, results)
        method = "keyword_overlap"

    output = {
        "query": query,
        "method": method,
        "results": reranked
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
