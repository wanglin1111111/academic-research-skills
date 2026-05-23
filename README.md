# Academic Research Skills Collection

> 学术研究技能合集 - 用于AI Agent的专业技能包

## 📋 概述

本仓库包含一系列用于AI Agent的专业技能包，涵盖企业分析、AI行业洞察、创业指导、中医养生、技术部署等领域。所有技能均采用MIT许可证，可自由使用和修改。

## 📦 技能列表

| 技能名称 | 描述 | 类别 | 版本 |
|---------|------|------|------|
| [enterprise-leads-analyzer](./enterprise-leads-analyzer) | 企业线索分析专家 | 商业 | 1.0.0 |
| [ai-industry-insight](./ai-industry-insight) | AI行业洞察专家 | 技术 | 1.0.0 |
| [startup-opc-guide](./startup-opc-guide) | OPC创业指南专家 | 商业 | 1.0.0 |
| [tcm-wellness-consultant](./tcm-wellness-consultant) | 中医养生顾问 | 健康 | 1.0.0 |
| [tech-deployment-guide](./tech-deployment-guide) | 技术部署指南 | 技术 | 1.0.0 |

## 🎯 技能详解

### 1. Enterprise Leads Analyzer（企业线索分析专家）

企业信息分析工具，提供：
- 企业画像分析
- 竞品对标分析
- 投资标的筛选
- 销售线索构建

**适用场景**：投资研究、商业分析、销售拓展

**触发词**：企业分析、竞品调研、投资标的、销售线索、商业模式

### 2. AI Industry Insight（AI行业洞察专家）

AI行业分析工具，提供：
- AI趋势分析
- 产品动态追踪
- 行业报告解读
- 创业方法论

**适用场景**：技术研究者、创业者、投资者

**触发词**：AI趋势、大模型、机器学习、AI创业、AI报告

### 3. Startup OPC Guide（OPC创业指南专家）

一人公司创业指导工具，提供：
- OPC方法论
- 政策解读
- 实战经验
- 避坑指南

**适用场景**：单人创业者、低成本启动

**触发词**：OPC、一人公司、单人创业、从0到1、创业避坑

### 4. TCM Wellness Consultant（中医养生顾问）

中医养生咨询工具，提供：
- 中医知识问答
- 体质辨识与调理
- 食疗养生
- 穴位保健

**适用场景**：养生咨询、体质调理

**触发词**：中医、养生、体质、食疗、穴位

⚠️ **重要提醒**：本技能提供的中医知识仅供参考，不构成医疗诊断和治疗建议。如有身体不适，请及时就医。

### 5. Tech Deployment Guide（技术部署指南）

技术部署指导工具，提供：
- 环境搭建指南
- 工具安装指导
- 配置优化建议
- 问题排查方案

**适用场景**：技术人员、开发者、系统管理员

**触发词**：部署、安装、环境搭建、配置、技术指南

## 🚀 快速开始

### 安装方式

将技能包放置在Agent的技能目录中：

```bash
# 克隆仓库
git clone https://github.com/wanglin1111111/academic-research-skills.git

# 复制技能到Agent技能目录
cp -r academic-research-skills/<skill-name> ~/.qclaw/skills/
```

### 配置数据源

每个技能需要在`config.yaml`中配置数据源：

```yaml
data_source:
  type: knowledge_base  # 或 local_db / third_party_api
  knowledge_base:
    id: "your-kb-id"  # 替换为实际知识库ID
    api_endpoint: "https://api.example.com/search"
```

### 使用示例

技能会在用户提问相关主题时自动触发：

```
用户："帮我分析一下做AI新药开发的企业"
→ 自动触发 enterprise-leads-analyzer

用户："大模型技术的发展趋势是什么？"
→ 自动触发 ai-industry-insight

用户："我想做一人公司，从哪里开始？"
→ 自动触发 startup-opc-guide
```

## 📁 目录结构

```
academic-research-skills/
├── README.md                          # 仓库说明文档
├── LICENSE                            # MIT许可证
├── enterprise-leads-analyzer/         # 企业线索分析技能
│   ├── SKILL.md                       # 技能详细说明
│   ├── scripts/                       # 执行脚本
│   ├── references/                    # 参考资料
│   └── assets/                        # 资源文件
├── ai-industry-insight/               # AI行业洞察技能
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
├── startup-opc-guide/                 # OPC创业指南技能
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
├── tcm-wellness-consultant/           # 中医养生顾问技能
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
└── tech-deployment-guide/             # 技术部署指南技能
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

## 🔧 技能开发规范

每个技能包遵循以下规范：

### SKILL.md 结构

```yaml
---
name: skill-name
version: 1.0.0
author: Anonymous Researcher
license: MIT
description: |
  技能描述
keywords:
  - keyword1
  - keyword2
category: category
---
```

### 必要内容

1. **概述**：技能用途和适用人群
2. **核心能力**：列出主要功能
3. **使用方法**：典型场景和示例
4. **输出格式**：结果展示模板
5. **技术实现**：配置和代码示例
6. **注意事项**：使用限制和风险提示
7. **隐私合规**：数据保护和合规声明

## 🔒 隐私保护原则

所有技能遵循以下隐私保护原则：

1. **不存储敏感数据**：所有查询通过API实时获取，不持久化存储
2. **匿名化处理**：作者信息匿名化，保护个人隐私
3. **免责声明**：明确标注内容仅供参考，不构成专业建议
4. **合规提醒**：提示用户遵守相关法律法规
5. **用途限制**：禁止用于非法活动

## 📜 许可证

MIT License

```
MIT License

Copyright (c) 2026 Anonymous Researcher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## ⚠️ 免责声明

本仓库中的所有技能包仅供学术研究和个人学习使用。技能提供的内容仅供参考，不构成：

- 投资建议
- 法律建议
- 医疗诊断和治疗建议
- 商业决策依据

使用者需自行判断信息的准确性和适用性，并承担相应风险。

## 📊 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-05-23 | 初始版本发布，包含5个技能包 |

## 🤝 贡献指南

欢迎贡献新的技能包或改进现有技能：

1. Fork本仓库
2. 创建新技能或改进现有技能
3. 确保遵循技能开发规范
4. 提交Pull Request

### 贡献要求

- 遵循MIT许可证
- 包含完整的SKILL.md文档
- 不包含敏感信息或个人隐私数据
- 提供适当的免责声明
- 确保内容客观准确

## 📧 联系方式

如有问题或建议，请通过GitHub Issues提交。

---

**最后更新**：2026-05-23

**仓库维护者**：Anonymous Researcher