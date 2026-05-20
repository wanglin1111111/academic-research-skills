"""
S2: Intent Classification + Cost-Aware Routing
Receives output from S1 (embedding.py). Reuses the embedding result.
Never re-embeds. Returns routing decision (which engines to call, how many results).
"""

import json, sys, re
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))

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
    q_lower = query.lower()
    intent = "general"
    for kw in CODE_KW:
        if kw in q_lower:
            intent = "code"; break
    if intent == "general":
        for kw in ACADEMIC_KW:
            if kw in q_lower:
                intent = "academic"; break
    if intent == "general":
        for kw in NEWS_KW:
            if kw in q_lower:
                intent = "web_news"; break
    if intent == "general":
        for kw in REVIEW_KW:
            if kw in q_lower:
                intent = "review"; break
    max_r = {"code": 1, "academic": 2, "web_news": 3, "review": 2}.get(intent, 5)
    return {"intent": intent, "max_results": max_r, "skip_rerank": max_r <= 3}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python classify.py <query>"}))
        sys.exit(1)
    result = classify_rules(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
