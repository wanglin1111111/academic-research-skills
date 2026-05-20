# ADK智能体Skill构建技能

## 技能概述
基于Google ADK框架，提供渐进式披露架构设计、Skill构建方法论和Agent评估体系。

## 核心能力

### 1. 渐进式披露架构设计
三层架构，节省90% token消耗：

**架构层次：**
```
L1 元数据层（~100 token）
├── name: 技能名称
├── description: 简短描述（核心决策依据）
└── tags: 分类标签

L2 指令层（~5000 token）
├── 完整指令
├── 参数定义
├── 示例场景
└── 边界条件

L3 资源层（外部文件）
├── references/: 参考文档
├── assets/: 资源文件
└── examples/: 示例库
```

**Token消耗对比：**
| 场景 | 传统方式 | 渐进式披露 | 节省 |
|------|----------|------------|------|
| 简单查询 | 5000 | 100 | 98% |
| 中等复杂 | 5000 | 500 | 90% |
| 复杂任务 | 5000 | 5000 | 0% |

### 2. 内联Skill构建
适用于快速原型、简单规则、稳定需求

**适用条件：**
- 指令不超过10行
- 无需外部资源
- 规则相对稳定
- 快速验证想法

**构建示例：**
```python
# 内联Skill示例：日期格式化
skill = """
名称：format_date
描述：将日期转换为指定格式
指令：
1. 识别输入日期格式
2. 转换为目标格式（默认YYYY-MM-DD）
3. 处理异常情况（返回原输入）

参数：
- date_input: 输入日期
- target_format: 目标格式（可选）

示例：
输入："2024年1月15日" → 输出："2024-01-15"
输入："01/15/2024" → 输出："2024-01-15"
"""
```

### 3. 文件型Skill构建
结构：SKILL.md + references/ + assets/

**目录结构：**
```
my-skill/
├── SKILL.md          # 主指令文件
├── references/
│   ├── api-docs.md   # API文档
│   └── best-practices.md
├── assets/
│   ├── templates/    # 模板文件
│   └── examples/     # 示例数据
└── examples/
    ├── example1.md
    └── example2.md
```

**优势：**
- 版本管理：Git追踪变更
- 可编辑分发：团队协作
- 跨Agent复用：标准化接口

### 4. 外部Skill导入
规范：agentskills.io（40+产品支持）

**导入命令：**
```bash
# 从官方仓库导入
npx skills add google/adk-docs -y -g

# 从GitHub导入
npx skills add github:user/repo/skill-name

# 从本地导入
npx skills add ./local-skill-path
```

**支持平台：**
- OpenAI GPTs
- Anthropic Claude
- Google Gemini
- Microsoft Copilot
- 自定义Agent平台

### 5. Skill工厂（元Skill）
自动生成新的SKILL.md文件，支持动态扩展、自我进化

**工厂代码示例：**
```python
def skill_factory(task_description: str, examples: list) -> str:
    """
    根据任务描述和示例自动生成Skill
    
    参数：
        task_description: 任务描述
        examples: 示例列表
    
    返回：
        SKILL.md内容
    """
    skill_template = f"""
# 自动生成Skill

## 描述
{task_description}

## 指令
基于以下示例学习：
{format_examples(examples)}

## 参数
自动识别参数：{extract_parameters(examples)}
"""
    return skill_template
```

### 6. Skill描述优化
description是Agent决策的核心依据，需精准简洁

**优化原则：**
- **具体**：明确触发条件
- **简洁**：不超过50字符
- **可区分**：避免与其他Skill混淆
- **可测试**：能验证是否匹配

**对比示例：**
```
❌ 差：处理文本
✅ 好：将Markdown转换为HTML

❌ 差：分析数据
✅ 好：分析CSV文件并生成统计报告

❌ 差：帮助用户
✅ 好：回答Python编程问题
```

### 7. Agent评估与测试

**评估维度：**
| 维度 | 指标 | 目标值 |
|------|------|--------|
| 功能测试 | 任务完成率 | >95% |
| 覆盖检查 | 场景覆盖率 | >80% |
| 冗余检查 | 指令重复率 | <10% |
| 资源验证 | 资源可用性 | 100% |

**测试脚本示例：**
```python
def test_skill(skill_path: str, test_cases: list) -> dict:
    """
    测试Skill的覆盖度和冗余度
    
    返回：
        {
            "pass_rate": 0.95,
            "coverage": 0.85,
            "redundancy": 0.08,
            "issues": ["示例1缺少边界情况"]
        }
    """
    results = []
    for case in test_cases:
        result = execute_skill(skill_path, case)
        results.append(result)
    
    return analyze_results(results)
```

### 8. 过早优化规避
所有Skill都从内联模式开始，验证后再升级

**升级路径：**
```
内联Skill（验证想法）
    ↓ 验证有效
文件型Skill（稳定使用）
    ↓ 复杂度增加
外部Skill（团队共享）
    ↓ 广泛使用
发布到agentskills.io（社区贡献）
```

## 使用示例

### 示例1：创建内联Skill
```
用户：帮我创建一个内联Skill用于格式化日期
助手：
已创建内联Skill：

名称：format_date
描述：将各种日期格式转换为标准YYYY-MM-DD
指令：
1. 识别输入格式（支持：中文、美式、欧式）
2. 解析为datetime对象
3. 输出为YYYY-MM-DD格式
4. 异常情况返回原输入

测试：
- "2024年1月15日" → "2024-01-15" ✓
- "01/15/2024" → "2024-01-15" ✓
- "15-01-2024" → "2024-01-15" ✓
```

### 示例2：升级为文件型Skill
```
用户：把这个内联Skill升级为文件型Skill
助手：
已创建文件型Skill：

目录结构：
format-date/
├── SKILL.md
├── references/
│   └── date-formats.md
└── examples/
    ├── example1.md
    └── example2.md

SKILL.md内容：
# 日期格式化Skill

## 描述
将各种日期格式转换为标准格式

## 指令
[完整指令...]

## 参数
- date_input: 输入日期
- target_format: 目标格式（默认YYYY-MM-DD）

## 示例
[10个示例...]
```

### 示例3：评估Skill
```
用户：评估这个Skill的覆盖度和冗余度
助手：
Skill评估报告：

【功能测试】
- 测试用例：50个
- 通过：47个
- 通过率：94%

【覆盖检查】
- 场景覆盖：42个（84%）
- 未覆盖场景：
  1. 跨年日期处理
  2. 时区转换

【冗余检查】
- 指令行数：120行
- 冗余内容：10行（8%）
- 建议：合并重复的错误处理逻辑

【资源验证】
- references/：3个文件 ✓
- examples/：10个文件 ✓
- 模板文件：2个 ✓

【改进建议】
1. 添加跨年日期测试用例
2. 简化错误处理逻辑
3. 补充时区转换文档
```

### 示例4：优化描述
```
用户：优化这个Skill的description
助手：
优化对比：

❌ 原描述：
"这个Skill帮助用户处理各种文本相关的任务，包括但不限于格式转换、内容提取、文本分析等"

✅ 优化后：
"文本处理：格式转换、内容提取、文本分析"

优化理由：
1. 删除冗余词汇（"帮助用户"、"包括但不限于"）
2. 使用具体动词（"转换"、"提取"、"分析"）
3. 控制在50字符以内
4. 保持可区分性
```

## 实际案例

### 案例1：客服机器人Skill
**背景**：电商客服自动化
**Skill设计**：
- L1：描述"回答订单查询、退换货问题"
- L2：完整指令+常见问题库
- L3：产品目录+政策文档
**效果**：自动处理70%常见问题

### 案例2：数据分析Skill
**背景**：财务报表自动化
**Skill设计**：
- 内联：简单计算
- 文件型：复杂分析+模板
- 外部：团队共享
**效果**：报表生成时间从2小时降至5分钟

### 案例3：代码生成Skill
**背景**：API接口开发
**Skill设计**：
- 工厂模式：根据需求生成Skill
- 自我进化：从反馈中学习
**效果**：代码生成准确率85%

## 最佳实践

### 1. 命名规范
- 使用动词+名词：`format_date`、`analyze_data`
- 避免缩写：`format_date` > `fmt_dt`
- 保持一致性：同类Skill统一前缀

### 2. 描述优化
- 控制在50字符以内
- 使用具体动词
- 避免模糊词汇
- 保持可区分性

### 3. 指令设计
- 分步骤清晰
- 包含边界条件
- 提供失败处理
- 添加示例

### 4. 测试覆盖
- 覆盖正常场景
- 测试边界情况
- 验证异常处理
- 定期回归测试

## 适用对象
AI Agent开发者、Skill工程师、自动化专家

## 相关技能
- `ai-agent-era-software`：AI时代软件架构
- `ai-knowledge-management`：知识管理基础设施
- `low-cost-search`：低成本高精度搜索