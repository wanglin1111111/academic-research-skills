# 低成本高精度搜索技能 (Low-Cost Search)

## 技能概述
通过语义缓存、意图分类、结果重排序、验证确认四层优化，实现低成本高精度的搜索体验。

## 核心架构（S1-S5流水线）

### S1: 语义缓存 (cache.py + embedding.py)
三层缓存架构：
- L1：精确匹配（相同查询）
- L2：语义相似（embedding相似度>0.85）
- L3：关键词覆盖（关键术语重叠>70%）

效果：高频查询0网络调用，缓存命中率40-60%

### S2: 意图分类 (classify.py)
零成本意图识别，路由到最优引擎：
- code → StackOverflow/GitHub（1个结果）
- academic → arxiv/scholar（2个结果）
- web_news → 新闻引擎（3个结果）
- review → 评测引擎（2个结果）
- general → 多引擎（5个结果）

### S3: 搜索引擎 (search.py + search_server.py)
- DuckDuckGo搜索（免费，无需API密钥）
- 常驻HTTP服务器（模型只加载一次）
- 首批即返优化（拿到3个结果立即返回）
- 超时降级（12秒超时，返回部分结果）

### S4: 结果重排序 (rerank.py)
- 使用BAAI/bge-reranker-base交叉编码器
- 简单关键词备选方案（无需模型）
- 过滤低分结果（阈值0.6）

### S5: 验证确认 (verify.py)
- 检查结果与查询的相关性
- 置信度标注（high/medium/low）
- 来源可信度评估

## 安装与使用

### 安装
```bash
# 安装依赖
pip install sentence-transformers duckduckgo-search

# 启动搜索服务器（可选，自动启动）
python search_server.py --warmup
```

### 使用
```python
from search_client import search
result = search("python list comprehension tutorial", max_results=5)
print(result["results"])
```

## 性能优化

### 成本优化
- 缓存命中：0 API调用
- 意图路由：减少60-80%不必要调用
- 首批即返：响应时间减少50%
- 模型复用：常驻服务器避免重复加载

### 精度优化
- 语义缓存：相似查询共享结果
- 意图分类：针对性召回
- 结果重排序：交叉编码器精排
- 验证确认：过滤低质量结果

## 目录结构
```
low-cost-search/
├── SKILL.md
├── scripts/
│   ├── cache.py           # 三层语义缓存
│   ├── embedding.py      # 查询嵌入
│   ├── classify.py       # 意图分类
│   ├── search.py         # 统一搜索入口
│   ├── search_server.py  # 常驻HTTP服务器
│   ├── search_client.py  # HTTP客户端
│   ├── rerank.py         # 结果重排序
│   ├── verify.py         # 结果验证
│   ├── knowledge_base.py # 预置知识库
│   └── diag.py          # 诊断脚本
└── references/
    └── cache/            # 缓存目录
```

## 依赖
- Python 3.8+
- sentence-transformers
- duckduckgo-search
- scikit-learn

## 适用对象
所有需要搜索功能的用户、AI Agent开发者
