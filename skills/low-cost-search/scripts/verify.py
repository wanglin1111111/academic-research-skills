#!/usr/bin/env python3
"""
verify.py — Verify search results and annotate confidence.
Checks relevance, source credibility, and result quality.
"""

import re
from typing import List, Dict
from datetime import datetime

# ── Confidence thresholds ────────────────────────────────────────────────────

HIGH_CONFIDENCE_THRESHOLD = 0.8
MEDIUM_CONFIDENCE_THRESHOLD = 0.6
LOW_CONFIDENCE_THRESHOLD = 0.4

# ── Source credibility scores ────────────────────────────────────────────────

CREDIBLE_SOURCES = {
    # Official documentation
    "docs.python.org": 1.0,
    "developer.mozilla.org": 1.0,
    "react.dev": 1.0,
    "vuejs.org": 1.0,
    "typescriptlang.org": 1.0,
    "golang.org": 1.0,
    "rust-lang.org": 1.0,
    
    # Academic
    "arxiv.org": 0.95,
    "scholar.google.com": 0.95,
    "dl.acm.org": 0.95,
    "ieeexplore.ieee.org": 0.95,
    
    # Q&A sites
    "stackoverflow.com": 0.85,
    "stackexchange.com": 0.85,
    "quora.com": 0.7,
    
    # Code hosting
    "github.com": 0.8,
    "gitlab.com": 0.8,
    "bitbucket.org": 0.75,
    
    # Tech blogs
    "medium.com": 0.65,
    "dev.to": 0.7,
    "towardsdatascience.com": 0.7,
    
    # News
    "news.ycombinator.com": 0.75,
    "reddit.com": 0.6,
}

# ── Verification functions ───────────────────────────────────────────────────

def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        # Remove protocol
        domain = url.split("://")[-1].split("/")[0]
        # Remove www.
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""

def get_source_credibility(url: str) -> float:
    """Get credibility score for a source."""
    domain = extract_domain(url)
    
    # Exact match
    if domain in CREDIBLE_SOURCES:
        return CREDIBLE_SOURCES[domain]
    
    # Partial match (subdomain)
    for known_domain, score in CREDIBLE_SOURCES.items():
        if domain.endswith(known_domain) or known_domain in domain:
            return score * 0.9  # Slightly lower for subdomains
    
    # Unknown source
    return 0.5

def compute_relevance(query: str, title: str, snippet: str) -> float:
    """Compute relevance score between query and result."""
    query_lower = query.lower()
    title_lower = title.lower()
    snippet_lower = snippet.lower()
    
    # Extract query terms
    query_terms = set(re.findall(r'\w+', query_lower))
    if not query_terms:
        return 0.5
    
    # Check title matches
    title_terms = set(re.findall(r'\w+', title_lower))
    title_overlap = len(query_terms & title_terms) / len(query_terms)
    
    # Check snippet matches
    snippet_terms = set(re.findall(r'\w+', snippet_lower))
    snippet_overlap = len(query_terms & snippet_terms) / len(query_terms)
    
    # Weighted score (title more important)
    relevance = 0.7 * title_overlap + 0.3 * snippet_overlap
    
    # Boost if exact phrase in title
    if query_lower in title_lower:
        relevance = min(1.0, relevance + 0.3)
    
    return relevance

def verify_result(query: str, result: Dict) -> Dict:
    """Verify a single result and add confidence annotation."""
    url = result.get("url", "")
    title = result.get("title", "")
    snippet = result.get("snippet", "")
    
    # Compute scores
    relevance = compute_relevance(query, title, snippet)
    credibility = get_source_credibility(url)
    
    # Combined confidence
    confidence_score = 0.6 * relevance + 0.4 * credibility
    
    # Determine confidence level
    if confidence_score >= HIGH_CONFIDENCE_THRESHOLD:
        confidence = "high"
    elif confidence_score >= MEDIUM_CONFIDENCE_THRESHOLD:
        confidence = "medium"
    elif confidence_score >= LOW_CONFIDENCE_THRESHOLD:
        confidence = "low"
    else:
        confidence = "very_low"
    
    # Add verification info
    verified = result.copy()
    verified["verification"] = {
        "confidence": confidence,
        "confidence_score": round(confidence_score, 3),
        "relevance": round(relevance, 3),
        "credibility": round(credibility, 3),
        "source_domain": extract_domain(url),
        "verified_at": datetime.now().isoformat()
    }
    
    return verified

def verify_results(query: str, results: List[Dict], min_confidence: str = "low") -> List[Dict]:
    """Verify all results and filter by minimum confidence."""
    confidence_order = {"very_low": 0, "low": 1, "medium": 2, "high": 3}
    min_level = confidence_order.get(min_confidence, 1)
    
    verified = []
    for result in results:
        v = verify_result(query, result)
        level = confidence_order.get(v["verification"]["confidence"], 0)
        if level >= min_level:
            verified.append(v)
    
    # Sort by confidence score
    verified.sort(key=lambda x: x["verification"]["confidence_score"], reverse=True)
    
    return verified

# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import sys
    import json
    
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python verify.py <query> '<results_json>' [min_confidence]"
        }))
        sys.exit(1)
    
    query = sys.argv[1]
    
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Missing results JSON"}))
        sys.exit(1)
    
    try:
        results = json.loads(sys.argv[2])
    except Exception as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)
    
    min_confidence = sys.argv[3] if len(sys.argv) > 3 else "low"
    
    verified = verify_results(query, results, min_confidence)
    
    print(json.dumps({
        "query": query,
        "total": len(results),
        "verified": len(verified),
        "min_confidence": min_confidence,
        "results": verified
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
