# AI知识管理技能

## 技能概述
涵盖AI工具应用、知识管理、信息处理、学术研究等领域。帮助用户实现多源文档整合、可溯源检索、跨文档关联分析和多模态内容生成。

## 核心能力

### 1. 多源异构文档整合
将PDF、网页、Markdown、图片、视频等统一导入知识库

**参数：**
- sources: 数据源列表（pdf/url/markdown/image/video）
- output_format: 输出格式（markdown/json/structured）

### 2. 可溯源知识检索
AI回答提供明确引用来源，支持一键跳转原文

**参数：**
- query: 检索查询
- detail_level: 详细程度（summary/detail/full）
- source_filter: 来源过滤（可选）

### 3. 跨文档关联分析
识别不同来源间的观点联系、矛盾冲突和潜在共识

**参数：**
- documents: 待分析文档列表
- analysis_type: 分析类型（connections/conflicts/consensus）

### 4. 多模态内容生成
自动生成PPT、播客、信息图、思维导图等

**参数：**
- content: 源内容
- output_type: 输出类型（ppt/podcast/infographic/mindmap）

## 使用示例
```
整合这些PDF和网页到知识库
检索关于AI伦理的内容，需要引用来源
分析这几篇论文之间的观点冲突
基于这些笔记生成思维导图
```

## 关键洞察
1. 突破单一文档限制
2. 透明化引用机制
3. 并行记忆优势
4. 从被动到主动

## 适用对象
学术研究者、知识工作者、终身学习者
