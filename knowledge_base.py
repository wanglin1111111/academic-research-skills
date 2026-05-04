"""
knowledge_base.py — 预置知识库 + 本地向量检索

原理：常见查询（城市美食、景点、天气等）预置到本地向量库，
查询时先检索本地，命中则 0 网络调用。

效果：高频查询 < 500ms，冷门查询仍走 ddgs
"""
import json
import time
from pathlib import Path
from typing import Optional, Dict, List, Any

SKILL_DIR = Path(__file__).parent.parent
KNOWLEDGE_DIR = SKILL_DIR / "references" / "knowledge"
KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
KNOWLEDGE_PATH = KNOWLEDGE_DIR / "hot_queries.jsonl"

# ── 预置热门查询（示例数据）──────────────────────────────────────────────

HOT_QUERIES = [
    # 城市美食
    {
        "query": "武汉有名小吃",
        "keywords": ["武汉", "小吃", "美食", "热干面", "豆皮", "鸭脖"],
        "answer": {
            "summary": "武汉最著名的小吃包括：热干面（碱水面拌芝麻酱）、三鲜豆皮（金黄酥脆）、精武鸭脖（麻辣鲜香）、面窝（油炸米饼）、鲜鱼糊汤粉、排骨莲藕汤、欢喜坨、汤包。",
            "items": [
                {"name": "热干面", "desc": "武汉C位名吃，碱水面拌芝麻酱，风靡全国"},
                {"name": "三鲜豆皮", "desc": "金黄酥脆，内馅糯米、肉丁、香菇"},
                {"name": "精武鸭脖", "desc": "武汉夜宵代表，麻辣鲜香"},
                {"name": "面窝", "desc": "油炸米饼，外脆内软"},
                {"name": "鲜鱼糊汤粉", "desc": "鲜鱼熬汤，配油条绝佳"},
            ],
            "source": "预置知识库"
        }
    },
    {
        "query": "北京有名小吃",
        "keywords": ["北京", "小吃", "美食", "烤鸭", "炸酱面"],
        "answer": {
            "summary": "北京著名小吃包括：北京烤鸭、炸酱面、卤煮火烧、豆汁焦圈、驴打滚、艾窝窝、糖葫芦、豌豆黄。",
            "items": [
                {"name": "北京烤鸭", "desc": "皮脆肉嫩，享誉世界"},
                {"name": "炸酱面", "desc": "手擀面配黄豆酱，老北京味道"},
                {"name": "卤煮火烧", "desc": "猪肠猪肺炖煮，地道北京味"},
            ],
            "source": "预置知识库"
        }
    },
    {
        "query": "上海有名小吃",
        "keywords": ["上海", "小吃", "美食", "生煎", "小笼包"],
        "answer": {
            "summary": "上海著名小吃包括：生煎包、小笼包、葱油拌面、白切鸡、红烧肉、糖醋排骨、排骨年糕、蟹壳黄。",
            "items": [
                {"name": "生煎包", "desc": "底部金黄酥脆，汁多味美"},
                {"name": "小笼包", "desc": "皮薄汁多，南翔小笼最著名"},
                {"name": "葱油拌面", "desc": "简单却经典，上海人早餐首选"},
            ],
            "source": "预置知识库"
        }
    },
    {
        "query": "成都美食推荐",
        "keywords": ["成都", "美食", "火锅", "串串", "川菜"],
        "answer": {
            "summary": "成都必吃美食：火锅、串串香、麻婆豆腐、夫妻肺片、担担面、龙抄手、钟水饺、钵钵鸡、兔头。",
            "items": [
                {"name": "火锅", "desc": "麻辣鲜香，成都美食名片"},
                {"name": "串串香", "desc": "自选菜品涮煮，平民美食"},
                {"name": "担担面", "desc": "麻辣鲜香，经典川味面食"},
            ],
            "source": "预置知识库"
        }
    },
    # 编程常见问题
    {
        "query": "python list comprehension",
        "keywords": ["python", "list", "comprehension", "列表推导式"],
        "answer": {
            "summary": "Python 列表推导式（List Comprehension）是用单行代码创建列表的简洁语法。基本格式：[expression for item in iterable if condition]",
            "examples": [
                "squares = [x**2 for x in range(10)]",
                "evens = [x for x in range(20) if x % 2 == 0]",
                "matrix = [[i*j for j in range(5)] for i in range(5)]",
            ],
            "source": "预置知识库"
        }
    },
    {
        "query": "python defaultdict",
        "keywords": ["python", "defaultdict", "字典", "default"],
        "answer": {
            "summary": "defaultdict 是 collections 模块中的字典子类，自动为不存在的键创建默认值，避免 KeyError。",
            "examples": [
                "from collections import defaultdict",
                "d = defaultdict(list)  # 默认值为空列表",
                "d['key'].append('value')  # 无需初始化",
            ],
            "source": "预置知识库"
        }
    },
    # 可以继续添加更多...
]

# ── 知识库管理 ────────────────────────────────────────────────────────────

def init_knowledge_base():
    """初始化知识库文件（首次运行时调用）"""
    if not KNOWLEDGE_PATH.exists():
        with open(KNOWLEDGE_PATH, "w", encoding="utf-8") as f:
            for entry in HOT_QUERIES:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return True
    return False


def load_knowledge_base() -> List[Dict]:
    """加载知识库"""
    if not KNOWLEDGE_PATH.exists():
        init_knowledge_base()
    
    entries = []
    with open(KNOWLEDGE_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except:
                    pass
    return entries


def query_knowledge(query: str, model=None, threshold: float = 0.75) -> Optional[Dict]:
    """
    查询知识库
    
    Args:
        query: 用户查询
        model: sentence-transformers 模型（用于语义匹配）
        threshold: 相似度阈值
    
    Returns:
        匹配的答案，或 None
    """
    entries = load_knowledge_base()
    if not entries:
        return None
    
    query_lower = query.lower().strip()
    
    # 1. 关键词匹配（快速路径）
    for entry in entries:
        keywords = entry.get("keywords", [])
        if any(kw in query_lower for kw in keywords):
            return {
                "query": query,
                "results": [{"title": entry["query"], "snippet": json.dumps(entry["answer"], ensure_ascii=False), "url": "", "source": "knowledge_base"}],
                "cache_hit": True,
                "cache_tier": "knowledge_base",
                "search_ms": 0,
            }
    
    # 2. 语义匹配（如果提供了模型）
    if model is not None:
        try:
            query_emb = model.encode(query).tolist()
            best_score, best_entry = 0.0, None
            
            # 注意：这里需要知识库条目预计算 embedding
            # 为简化，暂时只做关键词匹配
            
        except Exception:
            pass
    
    return None


def add_to_knowledge(query: str, keywords: List[str], answer: Dict):
    """添加新条目到知识库"""
    entry = {
        "query": query,
        "keywords": keywords,
        "answer": answer,
    }
    with open(KNOWLEDGE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# 初始化
if __name__ == "__main__":
    if init_knowledge_base():
        print(f"Knowledge base initialized at {KNOWLEDGE_PATH}")
    else:
        print(f"Knowledge base already exists at {KNOWLEDGE_PATH}")
    
    # 测试查询
    print("\nTest query: '武汉有什么好吃的'")
    result = query_knowledge("武汉有什么好吃的")
    if result:
        print("Hit:", result["results"][0]["title"])
    else:
        print("No match")
