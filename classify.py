"""
S2: Intent Classification + Cost-Aware Routing
Receives output from S1 (embedding.py). Reuses the embedding result.
Never re-embeds. Returns routing decision (which engines to call, how many results).

Routing rules:
  intent=code        → call_code_engine(1)        # StackOverflow/GitHub only
  intent=academic    → call_academic_engine(2)    # arxiv/scholar, skip S4
  intent=web_news   → call_news_engine(3)        # time-sensitive, no semantic dedup
  intent=review     → call_review_engine(2)       # skip S4, verify directly
  intent=general    → call_multi_engine(5)       # full pipeline

Flags:
  skip_rerank:  bool  # if total_results <= 3, no rerank needed
  skip_verify:  bool  # trusted domains only, no HTTP fetch
  max_api_calls: int   # how many engine calls to make (hard cap)
"""

import json
import sys
import re
from pathlib import Path

# ── Intent keywords ────────────────────────────────────────────────────────

CODE_KW = {
    'code', 'function', 'class', 'api', 'error', 'bug', 'debug',
    'import', 'module', 'package', 'npm', 'pip', 'github',
    'javascript', 'python', 'java', 'typescript', 'react', 'vue',
    'sql', 'database', 'shell', 'bash', 'cmd', 'linux',
    '编译', '代码', '函数', '接口', '报错', '调试', '脚本',
    'leetcode', 'algorithm', 'regex', 'json', 'xml', 'yaml',
}

ACADEMIC_KW = {
    'paper', 'research', 'study', 'arxiv', 'journal', 'academic',
    '论文', '研究', '学术', '文献', '博士', '硕士', '论文发表',
    'doi', 'citation', 'peer review', 'dissertation',
}

NEWS_KW = {
    'today', 'latest', 'recent', 'news', 'breaking',
    '昨天', '今天', '明天', '最新', '新闻', '近日', '刚刚',
    '2024', '2025', '2026',
}

REVIEW_KW = {
    'review', 'compare', 'vs', 'versus', 'better', 'best',
    '测评', '评测', '对比', '比较', '哪个好', '怎么样',
    '值得买', '推荐', '体验', '使用感受', '横评',
}


def classify_rules(query: str) -> dict:
    """Rule-based intent classifier — zero cost, deterministic."""
    q_lower = query.lower()

    intent = 'general'
    for kw in CODE_KW:
        if kw in q_lower:
            intent = 'code'
            break
    if intent == 'general':
        for kw in ACADEMIC_KW:
            if kw in q_lower:
                intent = 'academic'
                break
    if intent == 'general':
        for kw in NEWS_KW:
            if kw in q_lower:
                intent = 'web_news'
                break
    if intent == 'general':
        for kw in REVIEW_KW:
            if kw in q_lower:
                intent = 'review'
                break

    # Refine search terms (remove filler)
    fillers = [
        'how to', 'what is', 'how do', 'how can', '帮我', '我想知道',
        '请问', '问一下', '怎么', '如何', 'what the',
    ]
    terms = query
    for f in fillers:
        terms = re.sub(rf'\b{re.escape(f)}\b', '', terms, flags=re.IGNORECASE)
    terms = re.sub(r'\s+', ' ', terms).strip()

    time_sensitive = any(kw in q_lower for kw in NEWS_KW)

    return {
        "intent": intent,
        "search_terms": terms or query,
        "time_sensitive": time_sensitive,
        "method": "rule",
    }


def route(intent: str, n_results: int = 0) -> dict:
    """
    Cost-aware routing: decide which engines to call, how many,
    and which downstream steps to skip.
    """
    # Engine configs: (engine_name, max_calls, skip_rerank, skip_verify)
    configs = {
        'code': {
            'engines': ['stackoverflow', 'github'],
            'max_calls': 1,
            'skip_rerank': n_results <= 5,
            'skip_verify': False,   # code snippets: verify before showing
            'dedup_window': 3,      # deduplicate top-3 only
        },
        'academic': {
            'engines': ['arxiv', 'scholar'],
            'max_calls': 2,
            'skip_rerank': True,    # academic results are already ranked by relevance
            'skip_verify': True,    # arxiv/scholar domains are trusted
            'dedup_window': 5,
        },
        'web_news': {
            'engines': ['bing_news', 'google_news'],
            'max_calls': 2,
            'skip_rerank': True,    # recency > relevance for news
            'skip_verify': True,
            'dedup_window': 5,
        },
        'review': {
            'engines': ['zhihu', 'baidu'],
            'max_calls': 2,
            'skip_rerank': True,
            'skip_verify': False,
            'dedup_window': 5,
        },
        'general': {
            'engines': ['bing', 'duckduckgo', 'google', 'baidu'],
            'max_calls': 3,
            'skip_rerank': n_results <= 5,
            'skip_verify': False,
            'dedup_window': 8,
        },
    }

    cfg = configs.get(intent, configs['general'])

    # Estimate cost: each engine call ≈ 0.001 USD
    estimated_api_calls = cfg['max_calls']
    estimated_cost = round(estimated_api_calls * 0.001, 4)

    return {
        "intent": intent,
        "engines": cfg['engines'],
        "max_calls": cfg['max_calls'],
        "skip_rerank": cfg['skip_rerank'],
        "skip_verify": cfg['skip_verify'],
        "dedup_window": cfg['dedup_window'],
        "estimated_cost_usd": estimated_cost,
        "routing_method": "rule_cost_aware",
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python classify.py <query> [s1_json]"}))
        sys.exit(1)

    query = sys.argv[1]

    # Accept S1 result as second arg (re-use its embedding if already computed)
    s1 = {}
    if len(sys.argv) > 2:
        try:
            s1 = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass

    # Re-use normalized query from S1
    query_norm = s1.get('query_norm', '')
    is_nav = s1.get('is_nav', False)
    cache_hit = s1.get('cache_hit', False)

    # If cache hit, we already have the answer — just classify for logging
    result = classify_rules(query)
    result['query'] = query
    result['query_norm'] = query_norm
    result['is_nav'] = is_nav
    result['cache_hit'] = cache_hit

    if not cache_hit:
        routing = route(result['intent'])
        result['routing'] = routing
    else:
        result['routing'] = {
            "intent": result['intent'],
            "action": "cache_hit_skip_all",
            "estimated_cost_usd": 0.0,
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
