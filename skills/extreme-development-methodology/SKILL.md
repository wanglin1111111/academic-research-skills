# 48小时极限开发方法论技能

## 技能概述
提供在极短时间内（如黑客松、产品冲刺）高效完成 AI Agent 开发的系统化方法论。涵盖需求定义、技术选型、AI 协作、MVP 策略等核心环节。

## 核心理念

### 为什么需要极限开发方法论？
- **时间紧迫**：黑客松、产品冲刺等场景下，时间是最稀缺资源
- **质量保证**：在快速开发的同时，不能牺牲代码质量和可维护性
- **AI 协作**：如何最大化利用 AI 编程能力，避免常见陷阱
- **高效交付**：在48小时内完成可演示、可运行的 MVP

### 核心原则
1. **最高杠杆原则**：优先完成核心需求，砍掉非必要功能
2. **明确边界原则**：给 AI 明确的输入输出边界和失败行为
3. **保底方案原则**：始终有可演示的版本（即使后端未完成）
4. **根因排查原则**：排查 bug 时寻找根本原因，而非修复表象

---

## 第一部分：48小时极限开发方法论

### 1.1 核心流程（四大动作）

#### 动作1：搭建环境（第1小时）
**目标**：快速搭建可运行的开发环境

**关键步骤**：
1. 选择轻量级技术栈（见第二部分）
2. 配置 AI 编程工具（如 OpenClaw、Cursor 等）
3. 搭建基础项目结构
4. 确保部署流水线可用（如 Railway、Vercel）

**输出**：
- 可运行的空项目
- AI 工具已配置
- 部署环境已就绪

**示例代码结构**（Next.js + SQLite）：
```
my-agent-project/
├── src/
│   ├── app/              # 前端页面
│   ├── api/              # API 路由
│   ├── lib/              # 工具函数
│   └── db/               # 数据库操作
├── public/               # 静态资源
├── railway.json          # 部署配置
└── README.md             # 项目文档
```

#### 动作2：为 AI 设定业务边界（第2-3小时）
**目标**：明确告诉 AI 要做什么、不做什么、失败时怎么做

**关键要素**：

**a) 明确的输入边界**
```markdown
## 输入规范
- API 接收的字段：{字段名: 类型, 约束}
- 字段验证规则：使用 Zod / Joi 等库
- 错误输入的处理：返回 400 + 错误信息
```

**b) 明确的输出边界**
```markdown
## 输出规范
- 成功响应格式：{ status: "success", data: {...} }
- 错误响应格式：{ status: "error", message: "..." }
- 状态码规范：200/400/401/500
```

**c) 明确的失败行为**
```markdown
## 失败处理
- 数据库连不上：返回 503 + "数据库不可用"
- API 超时（>5秒）：返回 504 + "请求超时"
- 未捕获异常：记录日志 + 返回 500
```

**给 AI 的 Prompt 模板**：
```
实现一个 [功能名称] 模块，要求：

输入：
- 字段1: string, 必填, 长度 1-100
- 字段2: number, 可选, 范围 0-100

输出：
- 成功: { status: "success", data: {...} }
- 失败: { status: "error", message: "..." }

失败处理：
- 数据库错误 → 返回 503
- 参数错误 → 返回 400 + 错误详情
- 其他异常 → 记录日志 + 返回 500

技术栈：Next.js API Routes + SQLite
```

#### 动作3：触发业务（第4-24小时）
**目标**：实现核心业务逻辑

**开发策略**：
1. **Spike 调研**（2小时）：验证技术可行性
2. **模块化拆分**：将系统拆分为独立模块
3. **小时级开发节点**：制定详细的开发计划

**模块化拆分示例**（多元竞品监控 Agent）：
```
模块1：数据采集（6小时）
  - Sub-module 1.1: 爬取竞品官网（2小时）
  - Sub-module 1.2: 解析 HTML 提取关键信息（2小时）
  - Sub-module 1.3: 存储到数据库（2小时）

模块2：数据对比（4小时）
  - Sub-module 2.1: 计算差异（2小时）
  - Sub-module 2.2: 生成对比报告（2小时）

模块3：智能分流（4小时）
  - Sub-module 3.1: 规则引擎（2小时）
  - Sub-module 3.2: 通知推送（2小时）

模块4：数据存储（2小时）
  - Sub-module 4.1: 数据库表设计（1小时）
  - Sub-module 4.2: CRUD 接口（1小时）
```

**AI 协作技巧**：
- 让 AI 按规格（spec-driven）写代码
- 让 AI 生成 mock 数据
- 让 AI 总结代码（帮助理解）

#### 动作4：保底方案（第25-48小时）
**目标**：确保始终有可演示的版本

**保底策略**：
1. **前端 Mock**：即使后端未完成，前端用 mock 数据可演示
2. **后端 Mock**：后端返回硬编码数据，确保 API 可用
3. **降级方案**：复杂功能失败时，切换到简化版本

**前端 Mock 示例**：
```typescript
// src/lib/mock-data.ts
export const mockCompetitorData = [
  {
    id: 1,
    name: "竞品A",
    price: 99,
    features: ["功能1", "功能2"],
    lastUpdated: "2024-01-01"
  },
  // ... 更多 mock 数据
];

// src/app/api/competitors/route.ts
import { mockCompetitorData } from "@/lib/mock-data";

export async function GET() {
  // 开发阶段：返回 mock 数据
  if (process.env.USE_MOCK === "true") {
    return Response.json({ status: "success", data: mockCompetitorData });
  }
  
  // 生产阶段：从数据库读取
  // ...
}
```

**后端 Mock 示例**：
```python
# api/competitors.py
@app.route('/api/competitors', methods=['GET'])
def get_competitors():
    # 保底方案：返回硬编码数据
    mock_data = [
        {"name": "竞品A", "price": 99},
        {"name": "竞品B", "price": 199}
    ]
    return jsonify({"status": "success", "data": mock_data})
```

---

### 1.2 关键规避事项

#### 规避1：需求不明确
**问题**：AI 实现冗余功能，浪费时间

**解决方案**：
- 开赛前明确核心演示路径
- 用思维导图或流程图可视化需求
- 砍掉登录、安全等非核心需求

**需求定义模板**：
```
## 核心需求（必须实现）
1. 用户能上传竞品 URL
2. 系统能爬取竞品信息
3. 系统能对比多个竞品
4. 结果可视化展示

## 非核心需求（可砍掉）
- [ ] 用户登录/注册
- [ ] 权限管理
- [ ] 数据导出
- [ ] 邮件通知
```

#### 规避2：不了解代码结构
**问题**：AI 生成的代码导致 API 超时、内存泄漏等

**解决方案**：
- 人负责决策和验证 AI 结论
- 通过 debug 和运行时证据来验证 AI 的推理
- 确保对所写代码有清晰的认知

**代码审查清单**：
- [ ] API 响应时间 < 5秒
- [ ] 数据库查询有索引
- [ ] 内存使用不会持续增长
- [ ] 错误处理覆盖主要场景

---

## 第二部分：极限开发工具链选型

### 2.1 技术选型原则

**核心思想**：采用最轻量的代码架构，抛弃重型框架和依赖

#### 前端技术栈
| 技术 | 推荐 | 不推荐 | 理由 |
|-----|------|--------|------|
| 框架 | Next.js, Vite | Angular, Vue 3 | 轻量、快速、AI 友好 |
| UI库 | Tailwind CSS, shadcn/ui | Material-UI, Ant Design | 按需加载、无依赖地狱 |
| 状态管理 | Zustand, Jotai | Redux, MobX | 简单、轻量 |

#### 后端技术栈
| 技术 | 推荐 | 不推荐 | 理由 |
|-----|------|--------|------|
| 框架 | Next.js API Routes, FastAPI | Django, Spring Boot | 轻量、快速开发 |
| 数据库 | SQLite | PostgreSQL, MySQL | 无需配置、单文件 |
| ORM | Prisma, SQLAlchemy | TypeORM, Sequelize | 简单、类型安全 |

#### 部署方案
| 平台 | 推荐 | 不推荐 | 理由 |
|-----|------|--------|------|
| 前端 | Vercel | AWS S3 | 零配置、自动部署 |
| 后端 | Railway, Render | AWS EC2 | 简单、便宜 |
| 数据库 | Railway SQLite | RDS | 无需管理 |

**Railway 部署配置示例**（`railway.json`）：
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/api/health"
  }
}
```

---

### 2.2 AI 编程工具配置

#### 推荐工具
1. **OpenClaw**：本地 AI 编程助手，支持多模型
2. **Cursor**：AI-first 代码编辑器
3. **GitHub Copilot**：代码补全
4. **Claude / GPT-4**：通过 API 直接交互

#### 配置示例（OpenClaw）
```bash
# 安装 OpenClaw
npm install -g openclaw

# 配置 AI 模型
openclaw config set model qclaw/modelroute

# 启动 AI 助手
openclaw chat
```

#### AI 协作工作流
```
1. 人：写需求规格（spec）
2. AI：按 spec 生成代码
3. 人：审查代码，运行测试
4. AI：修复 bug，优化代码
5. 人：提交代码，部署
```

---

## 第三部分：AI 编程的正确姿势

### 3.1 明确分工

| 任务 | AI 擅长 | 人负责 |
|-----|---------|--------|
| 写代码 | ✅ 按规格写代码 | ❌ 决策架构 |
| 生成数据 | ✅ 生成 mock 数据 | ❌ 定义数据结构 |
| 总结代码 | ✅ 总结复杂代码 | ❌ 理解业务逻辑 |
| 调试 | ✅ 根据错误日志修复 | ❌ 判断根因 |
| 测试 | ✅ 生成测试用例 | ❌ 定义测试策略 |

### 3.2 有效沟通技巧

####技巧1：给 AI 明确的边界
**不好**❌：
```
"帮我写一个竞品监控功能"
```

**好**✅：
```
实现一个竞品监控 API，要求：

输入：
- url: string, 必填, 有效的 URL
- interval: number, 可选, 默认 60（分钟）

输出：
- 成功: { status: "success", data: { id, nextRunTime } }
- 失败: { status: "error", message: "..." }

失败处理：
- URL 无效 → 400 + "无效的 URL"
- 数据库错误 → 503 + "数据库不可用"
- 其他异常 → 记录日志 + 500

技术栈：Next.js API Routes + SQLite + node-cron
```

#### 技巧2：通过证据验证 AI 推理
**场景**：AI 说"这个 bug 是因为数据库连不上"

**验证步骤**：
1. 检查数据库日志
2. 手动连接数据库测试
3. 检查网络连接
4. 确认 AI 的推理是否正确

**给 AI 的反馈**：
```
你说是数据库连不上，但我检查了：
1. 数据库日志没有错误
2. 手动连接成功
3. 网络正常

重新分析这个 bug：[附上错误日志和截图]
```

#### 技巧3：确保对代码有清晰认知
**方法**：
1. 让 AI 总结代码（"请用白话解释这段代码在做什么"）
2. 自己画流程图
3. 单步调试，观察变量变化
4. 写注释，确保理解每一行

---

## 第四部分：MVP 思维与模块化开发

### 4.1 锁定核心需求

**步骤**：
1. 列出所有想要的功能
2. 按优先级排序（P0/P1/P2）
3. 砍掉 P1 和 P2，只保留 P0
4. 确保 P0 功能可演示

**示例**（竞品监控 Agent）：
```
P0（核心，必须实现）：
- 添加竞品 URL
- 爬取竞品信息
- 展示对比结果

P1（重要，可延后）：
- 自动定时监控
- 邮件通知
- 数据导出

P2（不重要，可砍掉）：
- 用户登录
- 权限管理
- 多语言支持
```

### 4.2 保底方案设计

**原则**：始终有可演示的版本

**实现**：
1. **前端独立可运行**：使用 mock 数据
2. **后端独立可运行**：返回硬编码数据
3. **降级方案**：复杂功能 → 简化功能

**前端保底**：
```typescript
// 开发环境：使用 mock 数据
// 生产环境：调用真实 API

const useMock = process.env.NODE_ENV === 'development';

const fetchCompetitors = async () => {
  if (useMock) {
    return mockData;
  } else {
    const response = await fetch('/api/competitors');
    return response.json();
  }
};
```

**后端保底**：
```python
# api/competitors.py

def get_competitors_from_db():
    try:
        # 尝试从数据库读取
        return db.query("SELECT * FROM competitors")
    except Exception as e:
        # 保底方案：返回硬编码数据
        logger.error(f"数据库错误: {e}")
        return [
            {"name": "竞品A", "price": 99},
            {"name": "竞品B", "price": 199}
        ]
```

### 4.3 根因排查方法

**错误示例**❌：
```
Bug: API 响应慢

表象修复：增加超时时间（从 5秒 → 30秒）

结果：用户体验更差，服务器资源耗尽
```

**正确示例**✅：
```
Bug: API 响应慢（平均 10秒）

根因排查：
1. 检查数据库查询：发现没有索引 → 添加索引
2. 检查 N+1 查询：发现循环查询数据库 → 使用 JOIN
3. 检查数据结构：发现返回过多字段 → 只返回必要字段

结果：响应时间降到 200ms
```

**排查工具**：
- **数据库**：EXPLAIN 分析查询计划
- **API**：Chrome DevTools Network 面板
- **内存**：Node.js heapdump
- **CPU**：profiler

---

## 第五部分：实战案例 - 多元竞品监控 Agent

### 5.1 项目概述

**目标**：在48小时内开发一个竞品监控系统

**核心功能**：
1. 添加竞品 URL
2. 自动爬取竞品信息（价格、功能、更新）
3. 对比多个竞品
4. 可视化展示

### 5.2 技术选型

| 层级 | 技术 |
|-----|------|
| 前端 | Next.js + Tailwind CSS + Zustand |
| 后端 | Next.js API Routes |
| 数据库 | SQLite (Prisma ORM) |
| 部署 | Railway |
| AI工具 | OpenClaw + Cursor |

### 5.3 开发计划（48小时）

#### 第1小时：环境搭建
- [x] 创建 Next.js 项目
- [x] 配置 Tailwind CSS
- [x] 安装 Prisma + SQLite
- [x] 配置 Railway 部署

#### 第2-3小时：需求定义和 AI 边界设定
- [x] 明确输入/输出边界
- [x] 定义失败行为
- [x] 写需求文档（给 AI 看）

#### 第4-6小时：Spike 调研
- [x] 验证爬取可行性（用 Cheerio / Puppeteer）
- [x] 验证数据存储方案
- [x] 验证部署流程

#### 第7-24小时：核心功能开发
**模块1：数据采集**（6小时）
- 爬取竞品官网
- 解析 HTML 提取信息
- 存储到数据库

**模块2：数据对比**（4小时）
- 计算差异
- 生成对比报告

**模块3：智能分流**（4小时）
- 规则引擎
- 通知推送

**模块4：数据存储**（2小时）
- 数据库表设计
- CRUD 接口

#### 第25-30小时：前端开发
- 竞品列表页
- 添加竞品表单
- 对比结果页

#### 第31-36小时：集成测试
- API 测试
- 前端集成
- Bug 修复

#### 第37-42小时：保底方案
- 前端 mock 数据
- 后端降级方案
- 错误处理优化

#### 第43-48小时：演示准备
- 录制 demo 视频
- 准备演讲稿
- 最终测试

### 5.4 代码片段示例

#### 数据采集模块
```typescript
// src/lib/crawler.ts
import cheerio from 'cheerio';
import axios from 'axios';

export async function crawlCompetitor(url: string) {
  try {
    // 1. 获取 HTML
    const response = await axios.get(url, { timeout: 5000 });
    const html = response.data;
    
    // 2. 解析 HTML
    const $ = cheerio.load(html);
    
    // 3. 提取信息（根据实际页面结构调整）
    const name = $('h1').text().trim();
    const price = $('.price').text().trim();
    const features = $('.features li').map((i, el) => $(el).text()).get();
    
    // 4. 返回结构化数据
    return {
      name,
      price,
      features,
      lastCrawled: new Date().toISOString()
    };
  } catch (error) {
    console.error(`爬取失败: ${url}`, error);
    throw new Error('爬取失败');
  }
}
```

#### 数据对比模块
```typescript
// src/lib/comparator.ts

export function compareCompetitors(competitors: any[]) {
  // 1. 价格对比
  const prices = competitors.map(c => parseFloat(c.price));
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  
  // 2. 功能对比
  const allFeatures = competitors.flatMap(c => c.features);
  const uniqueFeatures = [...new Set(allFeatures)];
  
  // 3. 生成对比报告
  const report = {
    priceRange: { min: minPrice, max: maxPrice },
    featureCoverage: competitors.map(c => ({
      name: c.name,
      features: c.features,
      coverage: c.features.length / uniqueFeatures.length
    })),
    lastUpdated: new Date().toISOString()
  };
  
  return report;
}
```

---

## 第六部分：待办与优化建议

### 6.1 商业产品参赛疑问

**问题**：商业 SaaS 平台参赛，源代码公开程度？

**建议**：
1. 与组委会确认开源协议要求
2. 如必须开源，考虑：
   - 开源核心算法，保留业务逻辑
   - 使用双许可证（开源 + 商业）
   - 提供 demo 版本源码

### 6.2 AI 技能库与多窗口协作优化

**问题**：Cloud Code 上下文过载

**解决方案**（基于讲师方法）：
1. **维护 Cloud MD**：
   - 记录常用操作和错误
   - 沉淀为 Skill
   - 便于多窗口协作

2. **创建技能库**：
   - 将常见问题解决方案封装为 Skill
   - 如："如何解决 API 超时问题"
   - 如："如何优化数据库查询"

3. **示例 Cloud MD 结构**：
```markdown
# Cloud MD - 开发笔记

## 常见问题

### API 超时
**原因**: 数据库查询慢
**解决**: 添加索引 + 使用 JOIN
**代码片段**: [附上代码]

### 内存泄漏
**原因**: 未释放事件监听器
**解决**: 在 useEffect 返回清理函数
**代码片段**: [附上代码]

## 常用命令

- 启动开发服务器: `npm run dev`
- 部署到 Railway: `railway up`
- 数据库迁移: `npx prisma migrate dev`

## AI 协作技巧

- 给 AI 明确的输入输出边界
- 通过 debug 证据验证 AI 推理
- 让 AI 总结代码（确保理解）
```

---

## 总结

### 核心要点
1. **时间管理**：48小时很紧，必须聚焦核心需求
2. **AI 协作**：明确边界、验证推理、保持认知
3. **保底方案**：始终有可演示的版本
4. **根因排查**：修复根本原因，而非表象
5. **轻量技术栈**：抛弃重型框架，快速开发

### 成功关键因素
- ✅ 明确的需求定义
- ✅ 合理的技术选型
- ✅ 高效的 AI 协作
- ✅ 可靠的保底方案
- ✅ 充分的根因排查

### 下一步
1. 选择一个黑客松题目
2. 按本文档的方法论制定计划
3. 开始48小时极限开发挑战
4. 总结经验，优化方法论

---

**版本**: v1.0  
**创建日期**: 2026-06-05  
**适用对象**: 黑客松参与者、产品冲刺团队、AI Agent 开发者
