#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
48小时极限开发 - 项目初始化工具
快速搭建 Next.js + SQLite + Railway 项目
"""

import os
import json
from pathlib import Path

class ExtremeDevInitializer:
    """
    极限开发项目初始化器
    自动生成项目结构、配置文件、AI 协作指南
    """
    
    def __init__(self, project_name):
        self.project_name = project_name
        self.project_dir = Path(f"./{project_name}")
    
    def create_project_structure(self):
        """创建项目目录结构"""
        print(f"\n[1/5] 创建项目结构: {self.project_name}")
        
        # 创建目录
        dirs = [
            "src/app",
            "src/api",
            "src/lib",
            "src/db",
            "public",
            "prisma"
        ]
        
        for dir_path in dirs:
            full_path = self.project_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {dir_path}")
        
        print(f"\n[OK] 项目结构已创建: {self.project_dir}")
    
    def generate_package_json(self):
        """生成 package.json"""
        print(f"\n[2/5] 生成 package.json...")
        
        package_json = {
            "name": self.project_name,
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
                "db:generate": "prisma generate",
                "db:push": "prisma db push",
                "db:studio": "prisma studio"
            },
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@prisma/client": "^5.0.0",
                "axios": "^1.6.0",
                "cheerio": "^1.0.0"
            },
            "devDependencies": {
                "prisma": "^5.0.0",
                "@types/node": "^20.0.0",
                "@types/react": "^18.2.0",
                "typescript": "^5.0.0",
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0"
            }
        }
        
        file_path = self.project_dir / "package.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ {file_path}")
    
    def generate_railway_config(self):
        """生成 Railway 部署配置"""
        print(f"\n[3/5] 生成 Railway 配置...")
        
        railway_json = {
            "build": {
                "builder": "NIXPACKS",
                "buildCommand": "npm run build"
            },
            "deploy": {
                "startCommand": "npm start",
                "healthcheckPath": "/api/health",
                "restartPolicyType": "ON_FAILURE"
            }
        }
        
        file_path = self.project_dir / "railway.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(railway_json, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ {file_path}")
    
    def generate_prisma_schema(self):
        """生成 Prisma Schema（SQLite）"""
        print(f"\n[4/5] 生成 Prisma Schema...")
        
        schema_content = f"""// prisma/schema.prisma
generator client {{
  provider = "prisma-client-js"
}}

datasource db {{
  provider = "sqlite"
  url      = "file:./dev.db"
}}

model Competitor {{
  id          Int      @id @default(autoincrement())
  name        String
  url         String   @unique
  price       Float?
  features    String[]
  lastCrawled DateTime @default(now())
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@map("competitors")
}}

model Comparison {{
  id          Int      @id @default(autoincrement())
  competitorId Int
  competitor  Competitor @relation(fields: [competitorId], references: [id])
  priceChange Float?
  newFeatures String[]
  createdAt   DateTime @default(now())
  
  @@map("comparisons")
}}
"""
        
        file_path = self.project_dir / "prisma" / "schema.prisma"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(schema_content)
        
        print(f"  ✓ {file_path}")
    
    def generate_ai_collaboration_guide(self):
        """生成 AI 协作指南（给 AI 看的 spec）"""
        print(f"\n[5/5] 生成 AI 协作指南...")
        
        guide_content = f"""# AI 协作指南 - {self.project_name}

本文档为 AI 编程助手提供明确的开发规范。

## 项目概述
{self.project_name} 是一个竞品监控系统，核心功能：
1. 添加竞品 URL
2. 自动爬取竞品信息
3. 对比多个竞品
4. 可视化展示

## 技术栈
- 前端: Next.js 14 + React 18 + Tailwind CSS
- 后端: Next.js API Routes
- 数据库: SQLite (Prisma ORM)
- 部署: Railway

## 开发规范

### API 输入输出边界

**所有 API 必须遵循统一响应格式**：

成功响应：
```json
{{
  "status": "success",
  "data": {{ ... }}
}}
```

失败响应：
```json
{{
  "status": "error",
  "message": "错误描述",
  "code": 400 | 401 | 403 | 404 | 500 | 503
}}
```

### 失败处理规范

| 失败场景 | HTTP状态码 | 错误信息 |
|---------|-----------|---------|
| 参数错误 | 400 | "无效的参数: [字段名]" |
| 未授权 | 401 | "未登录或 token 失效" |
| 无权限 | 403 | "无权限执行此操作" |
| 资源不存在 | 404 | "资源不存在: [资源名]" |
| 数据库错误 | 503 | "数据库暂时不可用" |
| 服务器错误 | 500 | "服务器内部错误" |

### 代码示例模板

**API Route 模板** (`src/app/api/example/route.ts`):
```typescript
import {{ NextRequest, NextResponse }} from 'next/server';
import {{ prisma }} from '@/lib/prisma';

export async function GET(request: NextRequest) {{
  try {{
    // 1. 解析参数
    const {{ searchParams }} = new URL(request.url);
    const id = searchParams.get('id');
    
    // 2. 参数验证
    if (!id) {{
      return NextResponse.json(
        {{ status: 'error', message: '缺少参数: id' }},
        {{ status: 400 }}
      );
    }}
    
    // 3. 数据库操作
    const data = await prisma.competitor.findUnique({{
      where: {{ id: parseInt(id) }}
    }});
    
    if (!data) {{
      return NextResponse.json(
        {{ status: 'error', message: '竞品不存在' }},
        {{ status: 404 }}
      );
    }}
    
    // 4. 返回成功响应
    return NextResponse.json({{
      status: 'success',
      data: data
    }});
    
  }} catch (error) {{
    console.error('API 错误:', error);
    
    // 5. 错误处理
    return NextResponse.json(
      {{ status: 'error', message: '服务器内部错误' }},
      {{ status: 500 }}
    );
  }}
}}
```

### 数据库操作规范

**使用 Prisma Client**：
```typescript
// src/lib/prisma.ts
import {{ PrismaClient }} from '@prisma/client';

const globalForPrisma = globalThis as unknown as {{
  prisma: PrismaClient | undefined;
}};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

### 爬虫代码规范

**使用 Cheerio 解析 HTML**：
```typescript
// src/lib/crawler.ts
import axios from 'axios';
import * as cheerio from 'cheerio';

export async function crawlCompetitor(url: string) {{
  try {{
    // 1. 获取 HTML（设置超时）
    const response = await axios.get(url, {{ timeout: 5000 }});
    const html = response.data;
    
    // 2. 解析 HTML
    const $ = cheerio.load(html);
    
    // 3. 提取数据（根据实际页面调整）
    const name = $('h1').text().trim();
    const price = parseFloat($('.price').text().replace('$', ''));
    const features = $('.features li').map((i, el) => $(el).text()).get();
    
    // 4. 返回结构化数据
    return {{
      name,
      price,
      features,
      url,
      lastCrawled: new Date().toISOString()
    }};
    
  }} catch (error: any) {{
    console.error(`爬取失败: ${{url}}`, error.message);
    throw new Error(`爬取失败: ${{error.message}}`);
  }}
}}
```

### 错误处理最佳实践

**记录详细日志**：
```typescript
// 好的错误处理
try {{
  await someAsyncOperation();
}} catch (error: any) {{
  console.error('操作失败', {{
    message: error.message,
    stack: error.stack,
    context: {{
      userId: user.id,
      action: 'create_competitor'
    }}
  }});
  throw error;
}}
```

## AI 任务清单

### 优先级 P0（必须完成）
- [ ] 实现添加竞品 API
- [ ] 实现竞品列表 API
- [ ] 实现爬取竞品信息功能
- [ ] 实现竞品对比功能
- [ ] 前端展示竞品列表
- [ ] 前端添加竞品表单

### 优先级 P1（重要但可延后）
- [ ] 实现定时监控
- [ ] 实现邮件通知
- [ ] 实现数据导出

### 优先级 P2（可砍掉）
- [ ] 用户登录/注册
- [ ] 权限管理
- [ ] 多语言支持

## 给 AI 的 Prompt 模板

### 实现 API 时：
```
实现 [API名称] API (Next.js API Routes)

输入参数：
- param1: string, 必填, 描述...
- param2: number, 可选, 描述...

输出格式：
- 成功: {{ status: "success", data: {{...}} }}
- 失败: {{ status: "error", message: "...", code: 400 }}

失败处理：
- 参数错误 → 400
- 数据库错误 → 503
- 其他异常 → 500

技术要求：
- 使用 Prisma 操作数据库
- 使用 try-catch 处理错误
- 记录详细日志
```

### Debug 时：
```
以下代码出现问题：[附上代码]

错误信息：
[附上完整错误日志]

我已尝试：
1. [尝试的方法1]
2. [尝试的方法2]

请分析根因并提供修复方案。
```

---

**最后更新**: {self.get_current_time()}
**AI 工具**: 本指南适用于 OpenClaw、Cursor、Copilot 等 AI 编程助手
"""
        
        file_path = self.project_dir / "AI_COLLABORATION_GUIDE.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"  ✓ {file_path}")
    
    def get_current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def run(self):
        """运行初始化器"""
        print("=" * 60)
        print(f"48小时极限开发 - 项目初始化")
        print("=" * 60)
        print(f"\n项目名: {self.project_name}\n")
        
        # 创建项目结构
        self.create_project_structure()
        
        # 生成配置文件
        self.generate_package_json()
        self.generate_railway_config()
        self.generate_prisma_schema()
        self.generate_ai_collaboration_guide()
        
        print("\n" + "=" * 60)
        print("[OK] 项目初始化完成！")
        print("=" * 60)
        print(f"\n下一步:")
        print(f"  1. cd {self.project_name}")
        print(f"  2. npm install")
        print(f"  3. npx prisma db push")
        print(f"  4. npm run dev")
        print(f"\nAI 协作指南: {self.project_dir / 'AI_COLLABORATION_GUIDE.md'}")
        print("=" * 60)

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python init_project.py <项目名>")
        print("示例: python init_project.py my-competitor-monitor")
        sys.exit(1)
    
    project_name = sys.argv[1]
    initializer = ExtremeDevInitializer(project_name)
    initializer.run()

if __name__ == '__main__':
    main()
