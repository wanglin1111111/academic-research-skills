#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
48灏忔椂鏋侀檺寮€鍙?- 椤圭洰鍒濆鍖栧伐鍏?蹇€熸惌寤?Next.js + SQLite + Railway 椤圭洰
"""

import os
import json
from pathlib import Path

class ExtremeDevInitializer:
    """
    鏋侀檺寮€鍙戦」鐩垵濮嬪寲鍣?    鑷姩鐢熸垚椤圭洰缁撴瀯銆侀厤缃枃浠躲€丄I 鍗忎綔鎸囧崡
    """
    
    def __init__(self, project_name):
        self.project_name = project_name
        self.project_dir = Path(f"./{project_name}")
    
    def create_project_structure(self):
        """鍒涘缓椤圭洰鐩綍缁撴瀯"""
        print(f"\n[1/5] 鍒涘缓椤圭洰缁撴瀯: {self.project_name}")
        
        # 鍒涘缓鐩綍
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
            print(f"  鉁?{dir_path}")
        
        print(f"\n[OK] 椤圭洰缁撴瀯宸插垱寤? {self.project_dir}")
    
    def generate_package_json(self):
        """鐢熸垚 package.json"""
        print(f"\n[2/5] 鐢熸垚 package.json...")
        
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
        
        print(f"  鉁?{file_path}")
    
    def generate_railway_config(self):
        """鐢熸垚 Railway 閮ㄧ讲閰嶇疆"""
        print(f"\n[3/5] 鐢熸垚 Railway 閰嶇疆...")
        
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
        
        print(f"  鉁?{file_path}")
    
    def generate_prisma_schema(self):
        """鐢熸垚 Prisma Schema锛圫QLite锛?""
        print(f"\n[4/5] 鐢熸垚 Prisma Schema...")
        
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
        
        print(f"  鉁?{file_path}")
    
    def generate_ai_collaboration_guide(self):
        """鐢熸垚 AI 鍗忎綔鎸囧崡锛堢粰 AI 鐪嬬殑 spec锛?""
        print(f"\n[5/5] 鐢熸垚 AI 鍗忎綔鎸囧崡...")
        
        guide_content = f"""# AI 鍗忎綔鎸囧崡 - {self.project_name}

鏈枃妗ｄ负 AI 缂栫▼鍔╂墜鎻愪緵鏄庣‘鐨勫紑鍙戣鑼冦€?
## 椤圭洰姒傝堪
{self.project_name} 鏄竴涓珵鍝佺洃鎺х郴缁燂紝鏍稿績鍔熻兘锛?1. 娣诲姞绔炲搧 URL
2. 鑷姩鐖彇绔炲搧淇℃伅
3. 瀵规瘮澶氫釜绔炲搧
4. 鍙鍖栧睍绀?
## 鎶€鏈爤
- 鍓嶇: Next.js 14 + React 18 + Tailwind CSS
- 鍚庣: Next.js API Routes
- 鏁版嵁搴? SQLite (Prisma ORM)
- 閮ㄧ讲: Railway

## 寮€鍙戣鑼?
### API 杈撳叆杈撳嚭杈圭晫

**鎵€鏈?API 蹇呴』閬靛惊缁熶竴鍝嶅簲鏍煎紡**锛?
鎴愬姛鍝嶅簲锛?```json
{{
  "status": "success",
  "data": {{ ... }}
}}
```

澶辫触鍝嶅簲锛?```json
{{
  "status": "error",
  "message": "閿欒鎻忚堪",
  "code": 400 | 401 | 403 | 404 | 500 | 503
}}
```

### 澶辫触澶勭悊瑙勮寖

| 澶辫触鍦烘櫙 | HTTP鐘舵€佺爜 | 閿欒淇℃伅 |
|---------|-----------|---------|
| 鍙傛暟閿欒 | 400 | "鏃犳晥鐨勫弬鏁? [瀛楁鍚峕" |
| 鏈巿鏉?| 401 | "鏈櫥褰曟垨 token 澶辨晥" |
| 鏃犳潈闄?| 403 | "鏃犳潈闄愭墽琛屾鎿嶄綔" |
| 璧勬簮涓嶅瓨鍦?| 404 | "璧勬簮涓嶅瓨鍦? [璧勬簮鍚峕" |
| 鏁版嵁搴撻敊璇?| 503 | "鏁版嵁搴撴殏鏃朵笉鍙敤" |
| 鏈嶅姟鍣ㄩ敊璇?| 500 | "鏈嶅姟鍣ㄥ唴閮ㄩ敊璇? |

### 浠ｇ爜绀轰緥妯℃澘

**API Route 妯℃澘** (`src/app/api/example/route.ts`):
```typescript
import {{ NextRequest, NextResponse }} from 'next/server';
import {{ prisma }} from '@/lib/prisma';

export async function GET(request: NextRequest) {{
  try {{
    // 1. 瑙ｆ瀽鍙傛暟
    const {{ searchParams }} = new URL(request.url);
    const id = searchParams.get('id');
    
    // 2. 鍙傛暟楠岃瘉
    if (!id) {{
      return NextResponse.json(
        {{ status: 'error', message: '缂哄皯鍙傛暟: id' }},
        {{ status: 400 }}
      );
    }}
    
    // 3. 鏁版嵁搴撴搷浣?    const data = await prisma.competitor.findUnique({{
      where: {{ id: parseInt(id) }}
    }});
    
    if (!data) {{
      return NextResponse.json(
        {{ status: 'error', message: '绔炲搧涓嶅瓨鍦? }},
        {{ status: 404 }}
      );
    }}
    
    // 4. 杩斿洖鎴愬姛鍝嶅簲
    return NextResponse.json({{
      status: 'success',
      data: data
    }});
    
  }} catch (error) {{
    console.error('API 閿欒:', error);
    
    // 5. 閿欒澶勭悊
    return NextResponse.json(
      {{ status: 'error', message: '鏈嶅姟鍣ㄥ唴閮ㄩ敊璇? }},
      {{ status: 500 }}
    );
  }}
}}
```

### 鏁版嵁搴撴搷浣滆鑼?
**浣跨敤 Prisma Client**锛?```typescript
// src/lib/prisma.ts
import {{ PrismaClient }} from '@prisma/client';

const globalForPrisma = globalThis as unknown as {{
  prisma: PrismaClient | undefined;
}};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

### 鐖櫕浠ｇ爜瑙勮寖

**浣跨敤 Cheerio 瑙ｆ瀽 HTML**锛?```typescript
// src/lib/crawler.ts
import axios from 'axios';
import * as cheerio from 'cheerio';

export async function crawlCompetitor(url: string) {{
  try {{
    // 1. 鑾峰彇 HTML锛堣缃秴鏃讹級
    const response = await axios.get(url, {{ timeout: 5000 }});
    const html = response.data;
    
    // 2. 瑙ｆ瀽 HTML
    const $ = cheerio.load(html);
    
    // 3. 鎻愬彇鏁版嵁锛堟牴鎹疄闄呴〉闈㈣皟鏁达級
    const name = $('h1').text().trim();
    const price = parseFloat($('.price').text().replace('$', ''));
    const features = $('.features li').map((i, el) => $(el).text()).get();
    
    // 4. 杩斿洖缁撴瀯鍖栨暟鎹?    return {{
      name,
      price,
      features,
      url,
      lastCrawled: new Date().toISOString()
    }};
    
  }} catch (error: any) {{
    console.error(`鐖彇澶辫触: ${{url}}`, error.message);
    throw new Error(`鐖彇澶辫触: ${{error.message}}`);
  }}
}}
```

### 閿欒澶勭悊鏈€浣冲疄璺?
**璁板綍璇︾粏鏃ュ織**锛?```typescript
// 濂界殑閿欒澶勭悊
try {{
  await someAsyncOperation();
}} catch (error: any) {{
  console.error('鎿嶄綔澶辫触', {{
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

## AI 浠诲姟娓呭崟

### 浼樺厛绾?P0锛堝繀椤诲畬鎴愶級
- [ ] 瀹炵幇娣诲姞绔炲搧 API
- [ ] 瀹炵幇绔炲搧鍒楄〃 API
- [ ] 瀹炵幇鐖彇绔炲搧淇℃伅鍔熻兘
- [ ] 瀹炵幇绔炲搧瀵规瘮鍔熻兘
- [ ] 鍓嶇灞曠ず绔炲搧鍒楄〃
- [ ] 鍓嶇娣诲姞绔炲搧琛ㄥ崟

### 浼樺厛绾?P1锛堥噸瑕佷絾鍙欢鍚庯級
- [ ] 瀹炵幇瀹氭椂鐩戞帶
- [ ] 瀹炵幇閭欢閫氱煡
- [ ] 瀹炵幇鏁版嵁瀵煎嚭

### 浼樺厛绾?P2锛堝彲鐮嶆帀锛?- [ ] 鐢ㄦ埛鐧诲綍/娉ㄥ唽
- [ ] 鏉冮檺绠＄悊
- [ ] 澶氳瑷€鏀寔

## 缁?AI 鐨?Prompt 妯℃澘

### 瀹炵幇 API 鏃讹細
```
瀹炵幇 [API鍚嶇О] API (Next.js API Routes)

杈撳叆鍙傛暟锛?- param1: string, 蹇呭～, 鎻忚堪...
- param2: number, 鍙€? 鎻忚堪...

杈撳嚭鏍煎紡锛?- 鎴愬姛: {{ status: "success", data: {{...}} }}
- 澶辫触: {{ status: "error", message: "...", code: 400 }}

澶辫触澶勭悊锛?- 鍙傛暟閿欒 鈫?400
- 鏁版嵁搴撻敊璇?鈫?503
- 鍏朵粬寮傚父 鈫?500

鎶€鏈姹傦細
- 浣跨敤 Prisma 鎿嶄綔鏁版嵁搴?- 浣跨敤 try-catch 澶勭悊閿欒
- 璁板綍璇︾粏鏃ュ織
```

### Debug 鏃讹細
```
浠ヤ笅浠ｇ爜鍑虹幇闂锛歔闄勪笂浠ｇ爜]

閿欒淇℃伅锛?[闄勪笂瀹屾暣閿欒鏃ュ織]

鎴戝凡灏濊瘯锛?1. [灏濊瘯鐨勬柟娉?]
2. [灏濊瘯鐨勬柟娉?]

璇峰垎鏋愭牴鍥犲苟鎻愪緵淇鏂规銆?```

---

**鏈€鍚庢洿鏂?*: {self.get_current_time()}
**AI 宸ュ叿**: 鏈寚鍗楅€傜敤浜?OpenClaw銆丆ursor銆丆opilot 绛?AI 缂栫▼鍔╂墜
"""
        
        file_path = self.project_dir / "AI_COLLABORATION_GUIDE.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"  鉁?{file_path}")
    
    def get_current_time(self):
        """鑾峰彇褰撳墠鏃堕棿瀛楃涓?""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def run(self):
        """杩愯鍒濆鍖栧櫒"""
        print("=" * 60)
        print(f"48灏忔椂鏋侀檺寮€鍙?- 椤圭洰鍒濆鍖?)
        print("=" * 60)
        print(f"\n椤圭洰鍚? {self.project_name}\n")
        
        # 鍒涘缓椤圭洰缁撴瀯
        self.create_project_structure()
        
        # 鐢熸垚閰嶇疆鏂囦欢
        self.generate_package_json()
        self.generate_railway_config()
        self.generate_prisma_schema()
        self.generate_ai_collaboration_guide()
        
        print("\n" + "=" * 60)
        print("[OK] 椤圭洰鍒濆鍖栧畬鎴愶紒")
        print("=" * 60)
        print(f"\n涓嬩竴姝?")
        print(f"  1. cd {self.project_name}")
        print(f"  2. npm install")
        print(f"  3. npx prisma db push")
        print(f"  4. npm run dev")
        print(f"\nAI 鍗忎綔鎸囧崡: {self.project_dir / 'AI_COLLABORATION_GUIDE.md'}")
        print("=" * 60)

def main():
    """涓诲嚱鏁?""
    import sys
    
    if len(sys.argv) < 2:
        print("鐢ㄦ硶: python init_project.py <椤圭洰鍚?")
        print("绀轰緥: python init_project.py my-competitor-monitor")
        sys.exit(1)
    
    project_name = sys.argv[1]
    initializer = ExtremeDevInitializer(project_name)
    initializer.run()

if __name__ == '__main__':
    main()
