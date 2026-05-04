# 08 low-cost-search技能包（完整版）

## 概述
低成本高精度搜索引擎。三层缓存 + 意图路由 + DuckDuckGo搜索

## 核心特性
- **响应时间**：< 500ms（缓存命中 < 50ms）
- **三层缓存**：L3精确匹配 + L2语义匹配 + L1进程缓存
- **搜索源**：DuckDuckGo 多引擎

## 快速使用
```python
from search_client import search
result = search("武汉有哪些有名旅游景点")
```

## 核心架构
```
User Query
    │
┌───┴───┐
▼       ▼
L3    L2
Raw   Semantic
Hit   Hit
<30ms <500ms
    │
    └── miss → DuckDuckGo Search
```

## 性能数据
| 场景 | 延迟 |
|------|------|
| 完全重复query | 28ms (L3 hit) |
| 语义改写query | 435ms (L2 hit) |
| 首次query | ~40s (网络搜索) |

## 三层缓存
| 层 | 原理 | 延迟 | 命中率 |
|---|---|---|---|
| L3 | Normalized query精确匹配 | <30ms | ~15% |
| L2 | Embedding cosine≥0.85 | <500ms | ~20% |
| L1 | 进程内LRU | <1ms | — |

## 输出JSON
```json
{
  "query": "python defaultdict example",
  "intent": "code",
  "cache_hit": true,
  "cache_tier": "L2_semantic",
  "results": [...],
  "search_ms": 435
}
```

## 依赖
- sentence-transformers≥2.0
- ddgs≥9.0
- Python 3.10+

## 启动方式
```bash
# 自动启动（首次搜索时）
python scripts/search_server.py --warmup --port 18765

# 双击启动
start_server.bat
```
