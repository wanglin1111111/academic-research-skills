"""
S5: Verification - Check result credibility against source URLs.
Usage: python verify.py "<query>" '<results_json>'
Output: Results with confidence labels (high/medium/low)
"""

import json
import sys
import re
import urllib.request
import urllib.error


def fetch_snippet(url: str, timeout: int = 5) -> str:
    """Fetch a short snippet from a URL for verification."""
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; SearchVerifier/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read(8192).decode('utf-8', errors='ignore')
            # Strip HTML tags
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:2000]
    except Exception:
        return ""


def extract_key_terms(text: str) -> set:
    """Extract meaningful terms from text."""
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'can', 'to', 'of', 'in',
        'on', 'at', 'by', 'for', 'with', 'from', 'and', 'or', 'but',
        '的', '了', '是', '在', '有', '和', '与', '或', '但', '也'
    }
    terms = set(re.findall(r'\b\w{3,}\b', text.lower()))
    return terms - stop_words


def compute_confidence(query: str, result: dict, page_text: str) -> str:
    """
    Compute confidence level for a result.
    Returns: 'high', 'medium', or 'low'
    """
    if not page_text:
        return 'low'

    query_terms = extract_key_terms(query)
    snippet_terms = extract_key_terms(result.get('snippet', ''))
    page_terms = extract_key_terms(page_text)

    # Check if snippet terms appear in page
    if snippet_terms:
        snippet_in_page = len(snippet_terms & page_terms) / len(snippet_terms)
    else:
        snippet_in_page = 0.0

    # Check if query terms appear in page
    if query_terms:
        query_in_page = len(query_terms & page_terms) / len(query_terms)
    else:
        query_in_page = 0.0

    if snippet_in_page >= 0.7 and query_in_page >= 0.5:
        return 'high'
    elif snippet_in_page >= 0.4 or query_in_page >= 0.3:
        return 'medium'
    else:
        return 'low'


def verify_results(query: str, results: list) -> list:
    """Verify each result against its source URL."""
    verified = []

    for result in results:
        url = result.get('url', '')
        if not url:
            result['confidence'] = 'low'
            result['confidence_reason'] = 'no_url'
            verified.append(result)
            continue

        # Skip verification for known trusted domains
        trusted_domains = [
            'wikipedia.org', 'github.com', 'stackoverflow.com',
            'arxiv.org', 'docs.python.org', 'developer.mozilla.org',
            'zhihu.com', 'baidu.com', 'qq.com'
        ]
        is_trusted = any(domain in url for domain in trusted_domains)

        if is_trusted:
            result['confidence'] = 'high'
            result['confidence_reason'] = 'trusted_domain'
        else:
            page_text = fetch_snippet(url)
            confidence = compute_confidence(query, result, page_text)
            result['confidence'] = confidence
            result['confidence_reason'] = 'content_match'

        verified.append(result)

    return verified


def add_warnings(results: list) -> dict:
    """Add overall warnings if confidence is generally low."""
    if not results:
        return {"results": results, "warning": "no_results"}

    low_count = sum(1 for r in results if r.get('confidence') == 'low')
    total = len(results)

    warning = None
    if low_count == total:
        warning = "当前搜索结果置信度较低，建议交叉验证"
    elif low_count > total / 2:
        warning = "部分搜索结果未能在来源验证，请注意甄别"

    return {"results": results, "warning": warning}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python verify.py <query> <results_json>"}))
        sys.exit(1)

    query = sys.argv[1]
    try:
        results = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid results JSON: {e}"}))
        sys.exit(1)

    if not results:
        print(json.dumps({"results": [], "warning": None}))
        return

    verified = verify_results(query, results)
    output = add_warnings(verified)
    output["query"] = query
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
