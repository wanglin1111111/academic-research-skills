# AI Skills Hub

通用 AI + 金融技能集合，涵盖知识管理、企业转型、Agent 构建、量化分析等领域。

## 仓库 renamed

原仓库名 `academic-research-skills` 不能准确反映内容，建议更名为 `ai-skills-hub`。

## 技能包一览

| # | 目录 | 技能名 | 状态 |
|---|------|--------|------|
| 01 | skills/ai-knowledge-management/ | AI知识管理 | ✅ 已修正 |
| 02 | skills/enterprise-ai-transformation/ | 企业AI转型 | ✅ 已修正 |
| 03 | skills/adk-skill-building/ | ADK智能体Skill构建 | ✅ 已修正 |
| 04 | skills/ai-agent-era-software/ | AI Agent时代软件构建 | ✅ 已修正 |
| 05 | skills/quantitative-finance/ | 量化金融分析 | ✅ 已修正 |
| 06 | skills/investment-mistakes-kb/ | 投资失误知识库 | ✅ 已修正 |
| 07 | skills/stock-analysis/ | 股票分析 | ✅ 已修正 |
| 08 | skills/low-cost-search/ | 低成本高精度搜索 | ✅ 已修正 |

## 主要修正内容

### 1. 仓库结构修正
- 原仓库将所有技能放在根目录，现改为 `skills/<name>/SKILL.md` 标准结构
- 原 `.metadata.json` 只描述了一个技能，现完整描述全部8个技能

### 2. 代码硬编码路径修正
以下脚本中的硬编码路径已修复为相对路径：
- `cache.py` — 移除 `C:\Users\22812\.qclaw\skills\low-cost-search\` 硬编码
- `diag.py` — 移除 `C:\Users\22812\.qclaw\skills\low-cost-search\scripts` 硬编码
- `search_client.py` — `PYTHON` 改为 `sys.executable`
- `embedding.py` — `PYTHON` 改为动态检测

### 3. 删除无关文件
- `readme.md`（与 README.md 重复，自动生成）→ 已删除
- `UPLOAD_MANIFEST.txt` → 已删除
- `紫光股份深度分析报告.md` → 与技能包无关，已移除
- `投资早报-2026-04-13.md` → 日期特定内容，已移除
- `feishu_api_error.log` → 错误日志，已移除

## 技术架构（low-cost-search）

```
S1: cache.py      语义缓存（三层：精确/语义/关键词）
S2: classify.py    意图分类（code/academic/news/review/general）
S3: search.py     搜索引擎（DuckDuckGo，常驻服务器）
S4: rerank.py     结果重排序（cross-encoder）
S5: verify.py     结果验证（置信度标注）
```

## 安装使用

### 依赖
```bash
pip install sentence-transformers duckduckgo-search scikit-learn
```

### 快速测试
```bash
python skills/low-cost-search/scripts/diag.py
python skills/low-cost-search/scripts/search.py "python defaultdict tutorial"
```

## 目录结构

```
ai-skills-hub/
├── README.md
├── .metadata.json
├── skills/
│   ├── ai-knowledge-management/SKILL.md
│   ├── enterprise-ai-transformation/SKILL.md
│   ├── adk-skill-building/SKILL.md
│   ├── ai-agent-era-software/SKILL.md
│   ├── quantitative-finance/SKILL.md
│   ├── investment-mistakes-kb/SKILL.md
│   ├── stock-analysis/SKILL.md
│   └── low-cost-search/
│       ├── SKILL.md
│       └── scripts/
│           ├── cache.py
│           ├── classify.py
│           ├── embedding.py
│           ├── rerank.py
│           ├── search.py
│           ├── search_client.py
│           ├── search_server.py
│           ├── verify.py
│           └── knowledge_base.py
└── references/
    └── cache/
```

## 许可证

MIT License

## 贡献

欢迎提交 PR 改进技能包内容或修复问题。
