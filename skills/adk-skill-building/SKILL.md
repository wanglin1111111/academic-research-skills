# ADK智能体Skill构建技能

## 技能概述
基于Google ADK框架，提供渐进式披露架构设计、Skill构建方法论和Agent评估体系。

## 核心能力

### 1. 渐进式披露架构设计
三层架构，节省90% token消耗：
- L1元数据层：名称+描述（~100 token）
- L2指令层：完整指令（~5000 token）
- L3资源层：外部参考文件

### 2. 内联Skill构建
适用于快速原型、简单规则、稳定需求
条件：指令不超过10行

### 3. 文件型Skill构建
结构：SKILL.md + references/ + assets/
优势：版本管理、可编辑分发、跨Agent复用

### 4. 外部Skill导入
规范：agentskills.io（40+产品支持）
命令：npx skills add google/adk-docs -y -g

### 5. Skill工厂（元Skill）
自动生成新的SKILL.md文件，支持动态扩展、自我进化

### 6. Skill描述优化
description是Agent决策的核心依据，需精准简洁

### 7. Agent评估与测试
功能测试、覆盖检查、冗余检查、资源验证

### 8. 过早优化规避
所有Skill都从内联模式开始，验证后再升级

## 使用示例
```
帮我创建一个内联Skill用于格式化日期
把这个内联Skill升级为文件型Skill
评估这个Skill的覆盖度和冗余度
优化这个Skill的description
```

## 适用对象
AI Agent开发者、Skill工程师
