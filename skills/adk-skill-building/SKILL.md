# ADK智能体Skill构建技能

## 技能概述
基于Google ADK框架，提供渐进式披露架构设计、Skill构建方法论和Agent评估体系。

## 核心能力

### 1. 渐进式披露架构设计
三层架构，节省90% token消耗：

| 层级 | 内容 | Token消耗 | 用途 |
|------|------|-----------|------|
| **L1元数据层** | 名称+描述 | ~100 token | Agent决策依据 |
| **L2指令层** | 完整指令 | ~5000 token | 执行详细步骤 |
| **L3资源层** | 外部参考文件 | 无限制 | 上下文增强 |

**架构优势：**
- Agent先读取L1，判断是否需要调用
- 调用时才加载L2指令
- 复杂场景引用L3资源文件
- 大幅降低无效token消耗

### 2. 内联Skill构建
适用于快速原型、简单规则、稳定需求

**适用条件：**
- 指令不超过10行
- 无需外部资源
- 规则稳定不变

**构建示例：**
```python
# 内联Skill示例
skill = {
    "name": "format_date",
    "description": "将日期格式化为YYYY-MM-DD",
    "instruction": """
    输入：任意格式的日期字符串
    输出：YYYY-MM-DD格式
    步骤：
    1. 解析输入日期
    2. 转换为标准格式
    3. 返回YYYY-MM-DD
    """
}
```

### 3. 文件型Skill构建
结构：SKILL.md + references/ + assets/

**文件结构：**
```
skill-name/
├── SKILL.md          # 主指令文件
├── references/       # 参考文档
│   ├── examples.md   # 使用示例
│   └── best-practices.md  # 最佳实践
└── assets/           # 资源文件
    ├── templates/    # 模板文件
    └── data/         # 数据文件
```

**优势：**
- 版本管理：Git追踪变更
- 可编辑分发：用户可自定义
- 跨Agent复用：多个Agent共享

### 4. 外部Skill导入
规范：agentskills.io（40+产品支持）

**导入命令：**
```bash
# 从官方仓库导入
npx skills add google/adk-docs -y -g

# 从GitHub导入
npx skills add github:user/skill-repo -y

# 从本地导入
npx skills add ./local-skill -y
```

**导入流程：**
1. 下载Skill包
2. 解析SKILL.md
3. 注册到Agent
4. 立即可用

### 5. Skill工厂（元Skill）
自动生成新的SKILL.md文件，支持动态扩展、自我进化

**工厂能力：**
- 分析用户需求
- 生成Skill结构
- 编写指令内容
- 添加示例和测试

**使用示例：**
```
用户：帮我创建一个"代码审查"的Skill
Skill工厂：
1. 分析需求：代码审查需要检查语法、逻辑、风格
2. 生成结构：SKILL.md + references/checklist.md
3. 编写指令：
   - 输入：代码片段
   - 检查项：语法错误、逻辑漏洞、代码风格
   - 输出：审查报告+改进建议
4. 添加示例：3个典型代码审查案例
5. 生成测试：验证Skill有效性

结果：已生成 code-review/SKILL.md
```

### 6. Skill描述优化
description是Agent决策的核心依据，需精准简洁

**优化原则：**
- **精准**：明确触发场景
- **简洁**：不超过50字符
- **独特**：避免与其他Skill混淆
- **可测试**：能验证是否被正确调用

**优化示例：**
```
❌ 差描述："帮助用户处理各种日期相关的问题"
✅ 好描述："将任意格式日期转换为YYYY-MM-DD标准格式"

❌ 差描述："分析股票数据"
✅ 好描述："基于财务报表生成股票投资分析报告"
```

### 7. Agent评估与测试
功能测试、覆盖检查、冗余检查、资源验证

**评估维度：**

| 维度 | 检查项 | 方法 |
|------|--------|------|
| **功能测试** | 是否正确执行 | 输入测试用例 |
| **覆盖检查** | 是否覆盖所有场景 | 场景覆盖率测试 |
| **冗余检查** | 是否与其他Skill重复 | 相似度分析 |
| **资源验证** | references是否存在 | 文件完整性检查 |

**评估流程：**
```python
def evaluate_skill(skill):
    # 1. 功能测试
    test_cases = generate_test_cases(skill)
    results = run_tests(skill, test_cases)
    
    # 2. 覆盖检查
    scenarios = extract_scenarios(skill)
    coverage = calculate_coverage(scenarios)
    
    # 3. 冗余检查
    similar_skills = find_similar_skills(skill)
    redundancy = calculate_redundancy(skill, similar_skills)
    
    # 4. 资源验证
    resources = check_resources(skill)
    
    return {
        "functionality": results,
        "coverage": coverage,
        "redundancy": redundancy,
        "resources": resources
    }
```

### 8. 过早优化规避
所有Skill都从内联模式开始，验证后再升级

**升级路径：**
```
内联Skill（快速验证）
    ↓ 验证有效
文件型Skill（稳定使用）
    ↓ 复杂度增加
外部Skill（分发复用）
    ↓ 持续优化
Skill工厂（动态生成）
```

**升级条件：**
- 内联→文件：指令超过10行，或需要外部资源
- 文件→外部：多个Agent需要使用，或需要版本管理
- 外部→工厂：需要动态生成，或支持用户自定义

## 使用示例

### 示例1：创建内联Skill
```
用户：帮我创建一个内联Skill用于格式化日期
助手：
已创建内联Skill：

{
  "name": "format_date",
  "description": "将日期格式化为YYYY-MM-DD标准格式",
  "instruction": "输入任意格式日期，解析后转换为YYYY-MM-DD格式输出",
  "examples": [
    {"input": "2024年1月15日", "output": "2024-01-15"},
    {"input": "Jan 15, 2024", "output": "2024-01-15"},
    {"input": "15/01/2024", "output": "2024-01-15"}
  ]
}

测试结果：3个测试用例全部通过 ✅
```

### 示例2：升级为文件型Skill
```
用户：把这个内联Skill升级为文件型Skill
助手：
已升级为文件型Skill：

format-date/
├── SKILL.md
│   # 格式化日期技能
│   
│   ## 功能
│   将任意格式日期转换为YYYY-MM-DD标准格式
│   
│   ## 支持格式
│   - 中文：2024年1月15日
│   - 英文：Jan 15, 2024
│   - 数字：15/01/2024, 2024-01-15
│   
│   ## 使用示例
│   输入：2024年1月15日
│   输出：2024-01-15
│
└── references/
    └── date-formats.md  # 支持的日期格式列表

已注册到Agent，可立即使用 ✅
```

### 示例3：评估Skill
```
用户：评估这个Skill的覆盖度和冗余度
助手：
Skill评估报告：

【功能测试】
- 测试用例：10个
- 通过率：100% ✅
- 边界情况：已覆盖

【覆盖检查】
- 场景覆盖率：85%
- 未覆盖场景：
  1. 无效日期输入（建议添加错误处理）
  2. 未来日期（建议添加范围限制）

【冗余检查】
- 相似Skill：2个（parse_date, validate_date）
- 冗余度：30%
- 建议：合并parse_date，保留差异化功能

【资源验证】
- references：完整 ✅
- assets：缺失（建议添加模板文件）

综合评分：75/100
建议改进：添加错误处理、合并相似Skill、补充资源文件
```

### 示例4：优化description
```
用户：优化这个Skill的description
助手：
description优化对比：

❌ 原描述："帮助用户处理各种日期相关的问题"
问题：
- 过于宽泛，不明确触发场景
- Agent难以判断何时调用
- 与其他日期Skill混淆

✅ 优化后："将任意格式日期转换为YYYY-MM-DD标准格式"
改进：
- 精准描述功能
- 明确输入输出
- 独特不混淆

测试效果：
- 调用准确率：从60%提升至95%
- 误调用率：从25%降至5%
```

## Skill工厂代码示例

```python
class SkillFactory:
    """Skill工厂：自动生成新Skill"""
    
    def create_skill(self, requirement: str) -> Skill:
        """根据需求创建Skill"""
        # 1. 分析需求
        analysis = self.analyze_requirement(requirement)
        
        # 2. 生成结构
        structure = self.generate_structure(analysis)
        
        # 3. 编写指令
        instruction = self.write_instruction(analysis)
        
        # 4. 添加示例
        examples = self.generate_examples(analysis)
        
        # 5. 创建文件
        skill = Skill(
            name=analysis["name"],
            description=analysis["description"],
            instruction=instruction,
            examples=examples,
            references=structure["references"]
        )
        
        # 6. 验证Skill
        validation = self.validate_skill(skill)
        
        return skill
    
    def analyze_requirement(self, requirement: str) -> dict:
        """分析用户需求"""
        # 使用LLM分析
        prompt = f"""
        分析以下Skill需求，提取关键信息：
        需求：{requirement}
        
        输出格式：
        - name: Skill名称
        - description: 简洁描述（<50字符）
        - input: 输入类型
        - output: 输出类型
        - scenarios: 适用场景列表
        """
        return llm.analyze(prompt)
    
    def validate_skill(self, skill: Skill) -> dict:
        """验证Skill有效性"""
        results = {
            "instruction_check": self.check_instruction(skill),
            "example_check": self.check_examples(skill),
            "resource_check": self.check_resources(skill)
        }
        return results
```

## 量化评估指标

| 指标 | 计算方式 | 目标值 |
|------|----------|--------|
| **功能准确率** | 测试通过数/总测试数 | ≥95% |
| **场景覆盖率** | 覆盖场景数/总场景数 | ≥80% |
| **冗余度** | 重复功能数/总功能数 | ≤20% |
| **调用准确率** | 正确调用数/总调用数 | ≥90% |
| **资源完整性** | 存在资源数/应存在数 | 100% |

## 最佳实践

### 1. 从简单开始
- 先用内联Skill验证想法
- 确认有效后再升级
- 避免过早优化

### 2. 精准描述
- description控制在50字符内
- 明确触发场景
- 突出独特价值

### 3. 持续迭代
- 根据使用反馈优化
- 定期评估和测试
- 合理升级架构

### 4. 避免冗余
- 检查相似Skill
- 合理合并或拆分
- 保持职责单一

## 适用对象
AI Agent开发者、Skill工程师、Prompt工程师、自动化专家

## 相关技能
- `ai-agent-era-software`：AI时代软件架构
- `enterprise-ai-transformation`：企业AI转型方法论
- `ai-knowledge-management`：知识管理基础设施