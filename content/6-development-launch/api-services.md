---
title: API 接口服务
---

# API 接口服务

> 在构建 SEO 站点时，合理利用第三方 API 服务可以大幅提升开发效率。本节介绍三个实用的 API 服务平台——apicore.ai、evolink.ai 和 kie.ai，涵盖它们的功能定位、接入方式和在 Next.js 项目中的集成示例。

---

## 为什么需要 API 接口服务

开发 SEO 站点时，以下需求往往需要借助外部 API 服务：

| 需求场景 | 自行开发成本 | API 服务方案 |
|----------|------------|-------------|
| AI 内容生成与改写 | 高（需训练模型或对接大模型） | kie.ai |
| 外链建设自动化 | 高（需爬虫 + 邮件系统） | evolink.ai |
| 数据抓取与聚合 | 高（反爬虫、IP 池管理） | apicore.ai |
| SEO 数据分析 | 中（需对接多个数据源） | apicore.ai |

使用 API 服务的核心优势：
- **节省开发时间**：无需重复造轮子
- **降低运维成本**：无需维护后端基础设施
- **快速迭代**：功能上线速度从数周缩短到数小时
- **按量付费**：起步成本低，按使用量扩展

---

## apicore.ai

### 平台概述

apicore.ai 是一个综合性的 API 服务平台，提供数据抓取、搜索引擎结果页（SERP）分析、内容提取等功能。对于 SEO 从业者来说，它主要用于获取搜索结果数据和竞争对手分析。

### 核心功能

| 功能模块 | 说明 | 用途 |
|----------|------|------|
| **SERP API** | 获取 Google/Bing 搜索结果 | 关键词排名监控 |
| **网页抓取** | 提取任意网页的结构化数据 | 竞品内容分析 |
| **批量查询** | 支持批量关键词查询 | 大规模关键词研究 |
| **多地域支持** | 模拟不同国家/语言的搜索 | 多语言 SEO 监控 |

### 接入示例

```typescript
// lib/apicore.ts
const APICORE_BASE_URL = 'https://api.apicore.ai/v1';
const APICORE_API_KEY = process.env.APICORE_API_KEY!;

interface SerpResult {
  position: number;
  title: string;
  url: string;
  description: string;
}

// 获取搜索结果
export async function getSerpResults(
  keyword: string,
  country: string = 'us',
  language: string = 'en'
): Promise<SerpResult[]> {
  const response = await fetch(`${APICORE_BASE_URL}/serp`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${APICORE_API_KEY}`,
    },
    body: JSON.stringify({
      keyword,
      country,
      language,
      num_results: 20,
    }),
  });

  if (!response.ok) {
    throw new Error(`SERP API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.results;
}

// 抓取网页内容
export async function scrapeWebpage(url: string) {
  const response = await fetch(`${APICORE_BASE_URL}/scrape`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${APICORE_API_KEY}`,
    },
    body: JSON.stringify({
      url,
      extract: ['title', 'meta_description', 'headings', 'content', 'links'],
    }),
  });

  const data = await response.json();
  return data;
}
```

### 实际应用：关键词排名追踪页面

```typescript
// app/dashboard/rankings/page.tsx
import { getSerpResults } from '@/lib/apicore';
import { supabase } from '@/lib/supabase';

export default async function RankingsPage() {
  // 从数据库获取需要追踪的关键词
  const { data: keywords } = await supabase
    .from('keyword_rankings')
    .select('keyword')
    .order('keyword');

  // 批量查询排名
  const rankings = await Promise.all(
    (keywords || []).map(async ({ keyword }) => {
      const results = await getSerpResults(keyword);
      const ourSite = results.find((r) =>
        r.url.includes('yourdomain.com')
      );
      return {
        keyword,
        position: ourSite?.position || null,
        url: ourSite?.url || null,
        topResult: results[0],
      };
    })
  );

  return (
    <div>
      <h1>关键词排名追踪</h1>
      <table>
        <thead>
          <tr>
            <th>关键词</th>
            <th>当前排名</th>
            <th>排名 URL</th>
            <th>第一名</th>
          </tr>
        </thead>
        <tbody>
          {rankings.map((r) => (
            <tr key={r.keyword}>
              <td>{r.keyword}</td>
              <td>{r.position || '未上榜'}</td>
              <td>{r.url || '-'}</td>
              <td>{r.topResult.title}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## evolink.ai

### 平台概述

evolink.ai 是一个专注于外链建设（Link Building）的 API 服务平台。它帮助 SEO 从业者自动化外链获取的流程——从发现潜在外链机会到发送合作邮件。

### 核心功能

| 功能模块 | 说明 | 用途 |
|----------|------|------|
| **外链机会发现** | 分析竞品外链，发现潜在合作站点 | 找到可获取的外链来源 |
| **联系人查找** | 获取目标网站管理员的联系方式 | Guest Post 合作 |
| **邮件模板生成** | AI 生成个性化的外链请求邮件 | 提高合作回复率 |
| **外链监控** | 监控已获取外链的存活状态 | 确保外链持续有效 |
| **锚文本分析** | 分析外链的锚文本分布 | 优化锚文本策略 |

### 接入示例

```typescript
// lib/evolink.ts
const EVOLINK_BASE_URL = 'https://api.evolink.ai/v1';
const EVOLINK_API_KEY = process.env.EVOLINK_API_KEY!;

// 分析竞品外链
export async function analyzeCompetitorBacklinks(domain: string) {
  const response = await fetch(`${EVOLINK_BASE_URL}/backlinks/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${EVOLINK_API_KEY}`,
    },
    body: JSON.stringify({
      domain,
      limit: 100,
      sort_by: 'domain_authority',
    }),
  });

  const data = await response.json();
  return data.backlinks;
}

// 发现外链机会
export async function findLinkOpportunities(
  niche: string,
  targetUrl: string
) {
  const response = await fetch(`${EVOLINK_BASE_URL}/opportunities`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${EVOLINK_API_KEY}`,
    },
    body: JSON.stringify({
      niche,
      target_url: targetUrl,
      opportunity_types: ['guest_post', 'resource_page', 'broken_link'],
      min_domain_authority: 30,
    }),
  });

  const data = await response.json();
  return data.opportunities;
}

// 生成外链请求邮件
export async function generateOutreachEmail(params: {
  targetSite: string;
  contactName: string;
  yourSite: string;
  articleTitle: string;
}) {
  const response = await fetch(`${EVOLINK_BASE_URL}/outreach/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${EVOLINK_API_KEY}`,
    },
    body: JSON.stringify({
      target_site: params.targetSite,
      contact_name: params.contactName,
      your_site: params.yourSite,
      article_title: params.articleTitle,
      tone: 'professional',
      language: 'en',
    }),
  });

  const data = await response.json();
  return data.email;
}
```

### 实际应用：外链管理面板

```typescript
// app/api/backlinks/route.ts
import { analyzeCompetitorBacklinks, findLinkOpportunities } from '@/lib/evolink';
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { action, ...params } = await request.json();

  switch (action) {
    case 'analyze_competitor': {
      const backlinks = await analyzeCompetitorBacklinks(params.domain);
      return NextResponse.json({ backlinks });
    }

    case 'find_opportunities': {
      const opportunities = await findLinkOpportunities(
        params.niche,
        params.targetUrl
      );
      return NextResponse.json({ opportunities });
    }

    default:
      return NextResponse.json({ error: 'Invalid action' }, { status: 400 });
  }
}
```

---

## kie.ai

### 平台概述

kie.ai 是一个 AI 能力聚合的 API 平台，提供文本生成、内容改写、翻译、摘要等 AI 功能。对于 SEO 站点，它主要用于批量内容生成和多语言内容制作。

### 核心功能

| 功能模块 | 说明 | SEO 用途 |
|----------|------|----------|
| **内容生成** | AI 生成高质量文章 | 批量生产 SEO 文章 |
| **内容改写** | 智能改写已有内容 | 避免重复内容惩罚 |
| **多语言翻译** | 高质量 AI 翻译 | 多语言 SEO 站点 |
| **摘要提取** | 自动生成内容摘要 | Meta Description 生成 |
| **关键词优化** | 基于关键词优化内容 | 提升内容相关性 |
| **标题生成** | 生成吸引点击的标题 | 提升 CTR |

### 接入示例

```typescript
// lib/kie.ts
const KIE_BASE_URL = 'https://api.kie.ai/v1';
const KIE_API_KEY = process.env.KIE_API_KEY!;

// AI 内容生成
export async function generateArticle(params: {
  topic: string;
  keywords: string[];
  language: string;
  wordCount: number;
}) {
  const response = await fetch(`${KIE_BASE_URL}/content/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${KIE_API_KEY}`,
    },
    body: JSON.stringify({
      topic: params.topic,
      keywords: params.keywords,
      language: params.language,
      word_count: params.wordCount,
      format: 'markdown',
      seo_optimized: true,
      include_headings: true,
      include_meta: true,  // 自动生成 Title 和 Description
    }),
  });

  const data = await response.json();
  return {
    title: data.title,
    content: data.content,
    metaTitle: data.meta_title,
    metaDescription: data.meta_description,
    suggestedKeywords: data.suggested_keywords,
  };
}

// 内容改写（去重）
export async function rewriteContent(
  content: string,
  style: 'professional' | 'casual' | 'academic' = 'professional'
) {
  const response = await fetch(`${KIE_BASE_URL}/content/rewrite`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${KIE_API_KEY}`,
    },
    body: JSON.stringify({
      content,
      style,
      preserve_meaning: true,
      uniqueness_target: 90,  // 目标唯一性 90%
    }),
  });

  const data = await response.json();
  return data.rewritten_content;
}

// 多语言翻译
export async function translateContent(
  content: string,
  targetLanguage: string
) {
  const response = await fetch(`${KIE_BASE_URL}/translate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${KIE_API_KEY}`,
    },
    body: JSON.stringify({
      content,
      target_language: targetLanguage,
      preserve_html: true,     // 保留 HTML 标签
      preserve_keywords: true,  // 保留关键词不翻译
      seo_friendly: true,       // SEO 友好翻译
    }),
  });

  const data = await response.json();
  return data.translated_content;
}

// 自动生成 Meta Description
export async function generateMetaDescription(
  content: string,
  keyword: string
) {
  const response = await fetch(`${KIE_BASE_URL}/content/summarize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${KIE_API_KEY}`,
    },
    body: JSON.stringify({
      content,
      max_length: 160,       // Meta Description 最佳长度
      include_keyword: keyword,
      type: 'meta_description',
    }),
  });

  const data = await response.json();
  return data.summary;
}
```

### 实际应用：批量内容生成工作流

```typescript
// scripts/batch-generate.ts
// 批量生成 SEO 文章并存入数据库
import { generateArticle, generateMetaDescription } from '@/lib/kie';
import { supabaseAdmin } from '@/lib/supabase';

interface ContentPlan {
  topic: string;
  keywords: string[];
  category: string;
}

async function batchGenerateArticles(plans: ContentPlan[]) {
  for (const plan of plans) {
    console.log(`正在生成: ${plan.topic}`);

    // 1. 生成文章
    const article = await generateArticle({
      topic: plan.topic,
      keywords: plan.keywords,
      language: 'en',
      wordCount: 1500,
    });

    // 2. 生成 slug
    const slug = plan.topic
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');

    // 3. 存入数据库
    const { error } = await supabaseAdmin.from('articles').insert({
      title: article.title,
      slug,
      content: article.content,
      meta_title: article.metaTitle,
      meta_description: article.metaDescription,
      status: 'draft',  // 先存为草稿，人工审核后发布
    });

    if (error) {
      console.error(`存储失败: ${plan.topic}`, error);
    } else {
      console.log(`完成: ${plan.topic}`);
    }

    // 4. 添加延迟避免触发速率限制
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }
}

// 使用示例
batchGenerateArticles([
  {
    topic: 'Best Free SEO Tools for Beginners in 2025',
    keywords: ['free seo tools', 'seo tools for beginners', 'best seo tools'],
    category: 'SEO Tools',
  },
  {
    topic: 'How to Do Keyword Research Step by Step',
    keywords: ['keyword research', 'keyword research guide', 'find keywords'],
    category: 'Keyword Research',
  },
]);
```

---

## API 服务选择指南

### 按需求场景选择

```
你需要什么？
│
├── 监控关键词排名和搜索结果？
│   └── apicore.ai（SERP API）
│
├── 自动化外链建设？
│   └── evolink.ai（外链发现 + 邮件生成）
│
├── 批量生成或改写 SEO 内容？
│   └── kie.ai（AI 内容生成）
│
├── 多语言站点内容翻译？
│   └── kie.ai（AI 翻译）
│
└── 竞品网站数据抓取？
    └── apicore.ai（网页抓取）
```

### 成本考量

| 服务 | 定价模式 | 起步成本 | 适用规模 |
|------|----------|----------|----------|
| apicore.ai | 按请求量 | 有免费额度 | 中小规模 |
| evolink.ai | 按功能订阅 | 按月订阅 | 有外链需求时 |
| kie.ai | 按 Token/字数 | 有免费额度 | 有内容生产需求时 |

---

## API 集成最佳实践

### 1. 安全管理 API 密钥

```typescript
// .env.local（不要提交到 Git）
APICORE_API_KEY=your_apicore_key
EVOLINK_API_KEY=your_evolink_key
KIE_API_KEY=your_kie_key
```

```gitignore
# .gitignore
.env.local
.env.*.local
```

### 2. 错误处理与重试机制

```typescript
// lib/api-utils.ts
export async function fetchWithRetry(
  url: string,
  options: RequestInit,
  maxRetries: number = 3
): Promise<Response> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(url, options);

      // 429 Too Many Requests - 等待后重试
      if (response.status === 429) {
        const retryAfter = parseInt(
          response.headers.get('Retry-After') || '5'
        );
        await new Promise((r) => setTimeout(r, retryAfter * 1000));
        continue;
      }

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      return response;
    } catch (error) {
      lastError = error as Error;
      // 指数退避
      await new Promise((r) =>
        setTimeout(r, Math.pow(2, attempt) * 1000)
      );
    }
  }

  throw lastError || new Error('Max retries exceeded');
}
```

### 3. 缓存 API 响应

```typescript
// lib/cache.ts
const cache = new Map<string, { data: unknown; timestamp: number }>();
const CACHE_TTL = 60 * 60 * 1000; // 1 小时

export async function cachedFetch<T>(
  key: string,
  fetcher: () => Promise<T>
): Promise<T> {
  const cached = cache.get(key);

  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data as T;
  }

  const data = await fetcher();
  cache.set(key, { data, timestamp: Date.now() });
  return data;
}

// 使用示例
const results = await cachedFetch(
  `serp:${keyword}:${country}`,
  () => getSerpResults(keyword, country)
);
```

### 4. 速率限制管理

```typescript
// lib/rate-limiter.ts
class RateLimiter {
  private queue: Array<() => void> = [];
  private running = 0;

  constructor(
    private maxConcurrent: number = 5,
    private intervalMs: number = 1000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    await this.waitForSlot();
    this.running++;

    try {
      return await fn();
    } finally {
      this.running--;
      await new Promise((r) => setTimeout(r, this.intervalMs));
      this.processQueue();
    }
  }

  private waitForSlot(): Promise<void> {
    if (this.running < this.maxConcurrent) {
      return Promise.resolve();
    }
    return new Promise((resolve) => {
      this.queue.push(resolve);
    });
  }

  private processQueue() {
    if (this.queue.length > 0 && this.running < this.maxConcurrent) {
      const next = this.queue.shift();
      next?.();
    }
  }
}

// 使用：限制 API 并发为 3，每次请求间隔 500ms
const limiter = new RateLimiter(3, 500);
const result = await limiter.execute(() => getSerpResults('keyword'));
```

---

## 注意事项

1. **内容质量审核**：AI 生成的内容必须经过人工审核后再发布，避免低质量内容影响 SEO
2. **遵守服务条款**：各 API 服务有各自的使用限制和条款，务必遵守
3. **数据安全**：不要将敏感数据通过第三方 API 传输
4. **成本监控**：设置 API 用量告警，避免意外超额
5. **降级方案**：当 API 服务不可用时，确保网站核心功能不受影响
