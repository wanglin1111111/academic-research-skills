---
name: bot-security-governance
version: 1.0.0
author: AI+ Series Workshop
license: MIT
description: |
  AI 机器人安全治理技能，提供公域 AI 智能体的安全设计、权限管理、风险防控等专业服务。
  整合王威扬分享的公域养虾安全经验，帮助开发者构建安全的 AI 机器人系统。
  
  触发场景：
  - AI 机器人安全架构设计
  - 权限精细化配置
  - 安全红线与合规管理
  - 风险监控与应急响应
  
  触发词：机器人安全、权限管理、安全红线、Key 安全、信息隔离、安全治理
keywords:
  - bot-security
  - permission-management
  - security-governance
  - risk-prevention
  - api-key-management
category: security
---

# Bot Security Governance

> AI 机器人安全治理专家 - 提供公域 AI 智能体安全设计与风险防控能力

## 📋 概述

本技能是一个 AI 机器人安全治理工具包，帮助开发者和运营者构建安全的 AI 智能体系统。整合王威扬分享的公域养虾安全经验，覆盖安全架构设计、权限管理、风险防控、应急响应等全流程。

## 🎯 核心能力

### 1. 安全架构设计
- 威胁建模与风险评估
- 安全分层架构
- 最小权限原则
- 纵深防御策略

### 2. 权限精细化管理
- 多维度权限模型
- 角色与策略设计
- 动态权限调整
- 权限审计与追溯

### 3. 安全红线设定
- 内容安全过滤
- 操作白名单/黑名单
- 敏感信息识别
- 合规性检查

### 4. 风险监控与响应
- 异常行为检测
- 实时告警机制
- 应急响应流程
- 安全审计与复盘

## 📊 知识覆盖范围

| 安全维度 | 核心内容 | 关键指标 | 适用场景 |
|---------|---------|---------|---------|
| 身份安全 | 认证、授权、Key 管理 | 泄露事件数 | 全周期 |
| 数据安全 | 加密、脱敏、隔离 | 数据泄露事件 | 全周期 |
| 操作安全 | 命令校验、审计 | 未授权操作数 | 全周期 |
| 内容安全 | 过滤、审核、合规 | 违规内容数 | 全周期 |

## 🚀 使用方法

### 典型应用场景

**场景1：公域 Bot 安全架构设计**
```
用户："如何设计公域养虾的安全架构？"
执行：分析威胁模型，设计分层安全架构，规划防护策略
```

**场景2：权限体系设计**
```
用户："如何精细化配置 Bot 权限？"
执行：设计权限模型，定义角色策略，实现动态控制
```

**场景3：安全红线与过滤**
```
用户："如何设定 Bot 的安全红线？"
执行：识别风险点，设计过滤规则，建立监控机制
```

**场景4：应急响应机制**
```
用户："Key 泄露后如何处理？"
执行：建立应急流程，设计止损方案，完善复盘机制
```

### 推荐问题示例

- AI 机器人有哪些安全风险？
- 如何管理 API Key 安全？
- 如何设计权限管理体系？
- 公域 Bot 如何防止滥用？
- 如何监控 Bot 异常行为？
- 安全事件如何应急处理？

## 📝 输出格式

### 安全架构设计文档

```markdown
# AI 机器人安全架构设计

## 威胁模型分析
### 资产识别
- 核心资产：API Key、用户数据、业务逻辑
- 敏感资产：对话内容、个人信息、财务数据
- 基础设施：服务器、数据库、网络

### 威胁识别
| 威胁类型 | 威胁描述 | 影响 | 概率 | 风险等级 |
|---------|---------|------|------|---------|
| Key 泄露 | API Key 被窃取滥用 | 高 | 中 | 高 |
| 信息泄露 | 敏感信息被获取 | 高 | 中 | 高 |
| 权限越权 | 执行未授权操作 | 中 | 低 | 中 |
| 服务滥用 | 资源被恶意消耗 | 中 | 高 | 中 |
| 内容违规 | 传播违规内容 | 高 | 中 | 高 |

### 攻击路径分析
```
外部攻击者
    ↓
公域 Bot 接口
    ↓
┌─────────────────┐
│  身份认证层      │ ← 第一道防线
└─────────────────┘
    ↓ 通过
┌─────────────────┐
│  权限控制层      │ ← 第二道防线
└─────────────────┘
    ↓ 通过
┌─────────────────┐
│  内容安全层      │ ← 第三道防线
└─────────────────┘
    ↓ 通过
┌─────────────────┐
│  操作审计层      │ ← 监控层
└─────────────────┘
```

## 分层安全架构
### 1. 身份与认证层
- API Key 加密存储
- 请求签名验证
- 频率限制
- IP 白名单

### 2. 权限控制层
- RBAC 角色模型
- 细粒度权限控制
- 动态权限调整
- 权限审计日志

### 3. 内容安全层
- 敏感词过滤
- 意图识别
- 合规性检查
- 人工审核队列

### 4. 操作审计层
- 全链路日志
- 异常检测
- 实时告警
- 审计追溯

## 安全红线设计
### 绝对禁止项
1. 不得泄露 API Key、Token 等凭证
2. 不得执行危险系统命令（rm、format、shutdown）
3. 不得访问未授权的数据资源
4. 不得传播违法违规内容
5. 不得绕过安全控制机制

### 条件允许项（需审批）
1. 金融分析（需用户明确同意）
2. 文件操作（需确认路径安全）
3. 外部 API 调用（需白名单）
4. 个人信息查询（需授权）

### 监控告警规则
| 规则 | 触发条件 | 响应动作 |
|------|---------|---------|
| Key 泄露检测 | 同一 Key 多 IP 使用 | 立即吊销 + 告警 |
| 异常请求模式 | 高频调用或异常路径 | 限流 + 人工审核 |
| 敏感信息泄露 | 输出包含 Key/密码 | 拦截 + 告警 |
| 权限越权 | 尝试未授权操作 | 拒绝 + 记录 + 告警 |
| 内容违规 | 命中违规关键词 | 拦截 + 人工审核 |
```

### 应急响应预案

```markdown
# 安全事件应急响应预案

## 事件分级
### P0 - 紧急（核心资产泄露）
- API Key 大规模泄露
- 用户数据大规模泄露
- 系统被完全控制

### P1 - 严重（功能滥用）
- 少量 Key 泄露
- 局部数据泄露
- 服务被滥用

### P2 - 一般（违规操作）
- 单次违规操作
- 少量敏感信息泄露
- 配置错误

## 应急流程
### P0 级响应（< 15分钟）
1. **立即止损**（< 5分钟）
   - 吊销所有相关 Key
   - 隔离受影响系统
   - 停止相关服务

2. **影响评估**（5-10分钟）
   - 评估泄露范围
   - 评估业务影响
   - 评估用户影响

3. **通报与沟通**（10-15分钟）
   - 内部通报
   - 用户通知（如需要）
   - 监管报告（如需要）

4. **根因分析**（24小时内）
   - 日志分析
   - 漏洞定位
   - 责任界定

5. **修复与恢复**（48小时内）
   - 漏洞修复
   - 系统加固
   - 服务恢复

### P1 级响应（< 1小时）
1. 立即止损
2. 局部隔离
3. 影响评估
4. 修复漏洞

### P2 级响应（< 4小时）
1. 拦截违规操作
2. 记录与审计
3. 策略优化
4. 事后复盘

## 复盘模板
```markdown
# 安全事件复盘报告

## 事件概述
- 事件时间：
- 事件类型：
- 影响范围：

## 时间线
- [时间] 事件发生
- [时间] 发现异常
- [时间] 启动应急
- [时间] 完成止损
- [时间] 恢复服务

## 根因分析
- 直接原因：
- 根本原因：
- 系统因素：

## 改进措施
- 短期措施（已完成）：
- 中期措施（1个月内）：
- 长期措施（3个月内）：
```

## ⚙️ 技术实现要点

### 安全 Skills 设计

```python
# 安全 Skills 示例
class SecurityCheckSkills:
    def __init__(self):
        self.red_lines = {
            'key_leak': ['api_key', 'token', 'secret', 'password'],
            'dangerous_commands': ['rm -rf', 'format', 'shutdown', 'drop database'],
            'sensitive_topics': ['stock_tips', 'medical_advice', 'legal_advice']
        }
    
    def check_key_leak(self, text):
        """检查 Key 泄露"""
        patterns = [
            r'sk-[a-zA-Z0-9]{48}',  # OpenAI Key
            r'[a-zA-Z0-9]{32}',      # 通用 Key
        ]
        for pattern in patterns:
            if re.search(pattern, text):
                return True, 'Potential key leak detected'
        return False, None
    
    def check_dangerous_command(self, command):
        """检查危险命令"""
        for danger in self.red_lines['dangerous_commands']:
            if danger in command.lower():
                return True, f'Dangerous command detected: {danger}'
        return False, None
    
    def security_scan(self, user_input, context):
        """安全扫描"""
        violations = []
        
        # Key 泄露检测
        leaked, msg = self.check_key_leak(user_input)
        if leaked:
            violations.append(('key_leak', msg))
        
        # 危险命令检测
        dangerous, msg = self.check_dangerous_command(user_input)
        if dangerous:
            violations.append(('dangerous_command', msg))
        
        # 敏感话题检测
        sensitive, msg = self.check_sensitive_topic(user_input, context)
        if sensitive:
            violations.append(('sensitive_topic', msg))
        
        return violations
```

### 权限管理系统

```python
# 权限管理系统
class PermissionManager:
    def __init__(self):
        self.roles = {
            'admin': {'permissions': ['*']},
            'moderator': {'permissions': ['read', 'write', 'moderate']},
            'user': {'permissions': ['read', 'write']},
            'guest': {'permissions': ['read']}
        }
        self.user_roles = {}
        self.resource_permissions = {}
    
    def assign_role(self, user_id, role):
        """分配角色"""
        if role not in self.roles:
            raise ValueError(f"Invalid role: {role}")
        self.user_roles[user_id] = role
    
    def check_permission(self, user_id, action, resource):
        """检查权限"""
        role = self.user_roles.get(user_id, 'guest')
        permissions = self.roles[role]['permissions']
        
        if '*' in permissions:
            return True
        
        if action in permissions:
            # 检查资源级权限
            resource_perm = self.resource_permissions.get(resource, {})
            if user_id in resource_perm.get('allowed', []):
                return True
            if user_id in resource_perm.get('denied', []):
                return False
        
        return False
    
    def get_accessible_resources(self, user_id):
        """获取用户可访问的资源"""
        role = self.user_roles.get(user_id, 'guest')
        permissions = self.roles[role]['permissions']
        
        accessible = []
        for resource, perm in self.resource_permissions.items():
            if self.check_permission(user_id, 'read', resource):
                accessible.append(resource)
        
        return accessible
```

## 🧪 场景测试

### 测试场景1：公域 Bot 安全架构设计

**输入：**
- 场景：飞书公开群 Bot，1000 人群
- 风险：Key 泄露、信息泄露、服务滥用
- 需求：完整的安全架构设计
- 约束：用户体验不受影响

**预期输出：**
1. 威胁模型与风险评估
2. 分层安全架构设计
3. 权限体系设计
4. 安全监控方案
5. 应急响应预案

**验证标准：**
- 威胁识别全面准确
- 架构设计层次清晰
- 权限体系覆盖所有场景
- 监控方案可执行
- 应急流程完整

**评分：** 9/10

### 测试场景2：API Key 安全管理

**输入：**
- 现状：使用多个 API Key（OpenAI、Kimi、Claude）
- 问题：Key 存储分散，容易泄露
- 需求：统一安全管理方案
- 目标：零 Key 泄露事件

**预期输出：**
1. Key 生命周期管理方案
2. 加密存储方案
3. 访问控制策略
4. 监控与告警机制
5. 应急轮换流程

**验证标准：**
- 生命周期管理完整
- 加密方案安全可靠
- 访问控制精细
- 监控覆盖所有风险点
- 应急流程快速有效

**评分：** 9/10

### 测试场景3：公域内容安全治理

**输入：**
- 场景：多群公域 Bot
- 风险：用户询问敏感信息、传播违规内容
- 需求：内容安全过滤体系
- 挑战：平衡安全与用户体验

**预期输出：**
1. 内容安全策略设计
2. 敏感信息识别方案
3. 违规内容处理流程
4. 人工审核机制
5. 用户教育与引导

**验证标准：**
- 安全策略覆盖主要风险
- 识别方案准确率高
- 处理流程清晰合理
- 人工审核机制有效
- 用户引导方式得当

**评分：** 8/10

## 📈 商业化路径

### 阶段1：咨询服务（0-6个月）
- 服务：安全架构咨询
- 收费：项目制（5-15万）

### 阶段2：安全产品（6-12个月）
- 产品：Bot 安全 SaaS 平台
- 功能：Key 管理、权限控制、安全监控
- 收费：按 Bot 数量收费

### 阶段3：安全服务（12个月+）
- 服务：安全审计、渗透测试、合规咨询
- 收费：项目制+年费服务

## ⚠️ 注意事项

1. **安全第一**：安全是公域 Bot 的生命线
2. **最小权限**：只授予必要的权限
3. **持续监控**：安全威胁不断演变，需持续监控
4. **用户透明**：明确告知用户数据使用方式
5. **合规优先**：遵守各平台和地区的法规要求

## 🔗 相关资源

- API 安全最佳实践
- OAuth 2.0 授权框架
- 内容安全审核指南
- 安全事件响应手册
