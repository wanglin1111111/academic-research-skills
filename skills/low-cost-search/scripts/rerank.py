"""S4: Local Reranker - Rerank search results using a cross-encoder."""
import json, sys, os
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

def rerank_with_model(query: str, results: list) -> list:
    try:
        from sentence_transformers import CrossEncoder
    except ImportError:
        return rerank_simple(query, results)
    model = CrossEncoder("BAAI/bge-reranker-base")
    pairs = [(query, f"{r.get('title','')} {r.get('snippet','')}") for r in results]
    scores = model.predict(pairs).tolist()
    for i, r in enumerate(results):
        r["rerank_score"] = round(float(scores[i]), 4)
    filtered = [r for r in results if r.get("rerank_score", 0) >= 0.6]
    return sorted(filtered, key=lambda x: x["rerank_score"], reverse=True) or results[:3]

def rerank_simple(query: str, results: list) -> list:
    import re
    q_terms = set(re.findall(r"\w+", query.lower()))
    for r in results:
        text = f"{r.get('title','')} {r.get('snippet','')}".lower()
        t_terms = set(re.findall(r"\w+", text))
        r["rerank_score"] = round(len(q_terms & t_terms) / max(len(q_terms), 1), 4)
    return sorted(results, key=lambda x: x["rerank_score"], reverse=True)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python rerank.py <query> '<results_json>'}))
        sys.exit(1)
    query = sys.argv[1]
    results = json.loads(sys.argv[2])
    reranked = rerank_simple(query, results)
    print(json.dumps(reranked[:5], ensure_ascii=False, indent=2))
