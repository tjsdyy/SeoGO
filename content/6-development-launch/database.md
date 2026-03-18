---
title: 数据库选型
---

# 数据库选型

> 对于 SEO 站点而言，数据库不仅存储内容和用户数据，还直接影响页面响应速度和 TTFB（首字节时间）。选错数据库可能导致查询缓慢、成本飙升或扩容困难。本节将对比 Supabase、PlanetScale 和 MongoDB Atlas 三种主流云数据库服务，帮助你做出最优选择。

---

## 为什么 SEO 站点需要关注数据库选型

数据库性能直接影响 SEO 表现：

- **TTFB（首字节时间）**：数据库查询是服务端响应时间的主要组成部分，Google 建议 TTFB < 200ms
- **页面生成速度**：SSR/ISR 页面的生成依赖数据库查询效率
- **高并发能力**：当搜索引擎爬虫和用户同时访问时，数据库需要承受并发压力
- **数据一致性**：内容频繁更新的站点需要可靠的数据同步机制

---

## Supabase（推荐）

### 概述

Supabase 是一个基于 PostgreSQL 的开源后端即服务（BaaS）平台，常被称为"开源的 Firebase 替代品"。它提供数据库、认证、存储、实时订阅和 Edge Functions 等一站式服务。

### 核心特性

| 特性 | 说明 |
|------|------|
| **数据库引擎** | PostgreSQL（全球最先进的开源关系型数据库） |
| **实时订阅** | 内置 Realtime，支持数据变更实时推送 |
| **认证系统** | 内置 Auth，支持 OAuth、Magic Link、邮箱密码 |
| **存储服务** | 文件存储，支持图片转换和 CDN |
| **Edge Functions** | 基于 Deno 的 Serverless 函数 |
| **REST & GraphQL API** | 自动为数据库表生成 API |
| **Row Level Security** | PostgreSQL 级别的数据访问控制 |

### 免费套餐

| 资源 | 免费额度 |
|------|----------|
| 数据库空间 | 500 MB |
| 文件存储 | 1 GB |
| 带宽 | 5 GB |
| Edge Functions | 500,000 次调用 |
| 实时连接 | 200 个并发 |
| 项目数 | 2 个活跃项目 |

### Supabase 搭建完整流程

#### 第一步：创建项目

1. 访问 [supabase.com](https://supabase.com)，使用 GitHub 账号登录
2. 点击 "New Project"
3. 选择组织，填写项目名称
4. 设置数据库密码（务必记住）
5. 选择服务器区域（美西 `us-west-1` 或新加坡 `ap-southeast-1`）
6. 点击 "Create new project"，等待约 2 分钟初始化

#### 第二步：设计数据库表

以 SEO 内容站为例，创建核心表结构：

```sql
-- 文章表
CREATE TABLE articles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  content TEXT,
  excerpt TEXT,
  meta_title TEXT,          -- SEO 标题
  meta_description TEXT,    -- SEO 描述
  featured_image TEXT,
  category_id UUID REFERENCES categories(id),
  author_id UUID REFERENCES auth.users(id),
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 分类表
CREATE TABLE categories (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  parent_id UUID REFERENCES categories(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 关键词追踪表
CREATE TABLE keyword_rankings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  keyword TEXT NOT NULL,
  position INTEGER,
  url TEXT,
  search_volume INTEGER,
  checked_at TIMESTAMPTZ DEFAULT NOW()
);

-- 为 slug 字段创建索引（加速查询）
CREATE INDEX idx_articles_slug ON articles(slug);
CREATE INDEX idx_articles_status ON articles(status);
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);

-- 自动更新 updated_at 字段
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_updated_at
  BEFORE UPDATE ON articles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

#### 第三步：配置 Row Level Security（RLS）

```sql
-- 启用 RLS
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;

-- 公开读取已发布文章
CREATE POLICY "Published articles are viewable by everyone"
  ON articles FOR SELECT
  USING (status = 'published');

-- 作者可以管理自己的文章
CREATE POLICY "Authors can manage their own articles"
  ON articles FOR ALL
  USING (auth.uid() = author_id);
```

#### 第四步：在 Next.js 项目中集成

```bash
# 安装 Supabase 客户端
npm install @supabase/supabase-js
```

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// 服务端专用客户端（拥有更高权限）
export const supabaseAdmin = createClient(
  supabaseUrl,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);
```

```typescript
// app/blog/[slug]/page.tsx - 获取文章数据
import { supabase } from '@/lib/supabase';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';

interface Props {
  params: { slug: string };
}

// 生成 SEO Metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { data: article } = await supabase
    .from('articles')
    .select('title, meta_title, meta_description, featured_image')
    .eq('slug', params.slug)
    .eq('status', 'published')
    .single();

  if (!article) return {};

  return {
    title: article.meta_title || article.title,
    description: article.meta_description,
    openGraph: {
      title: article.meta_title || article.title,
      description: article.meta_description,
      images: article.featured_image ? [{ url: article.featured_image }] : [],
    },
  };
}

// 静态生成所有文章路径
export async function generateStaticParams() {
  const { data: articles } = await supabase
    .from('articles')
    .select('slug')
    .eq('status', 'published');

  return (articles || []).map((article) => ({
    slug: article.slug,
  }));
}

export default async function ArticlePage({ params }: Props) {
  const { data: article } = await supabase
    .from('articles')
    .select('*, categories(name, slug)')
    .eq('slug', params.slug)
    .eq('status', 'published')
    .single();

  if (!article) notFound();

  return (
    <article>
      <h1>{article.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: article.content }} />
    </article>
  );
}
```

---

## PlanetScale

### 概述

PlanetScale 是基于 Vitess（YouTube 数据库技术）的 MySQL 兼容 Serverless 数据库。它的核心特色是数据库分支（Database Branching）和无锁 Schema 变更（Non-blocking Schema Changes）。

> **注意**：PlanetScale 于 2024 年取消了免费套餐，目前最低方案为 $39/月（Scaler 计划）。如果预算有限，建议优先考虑 Supabase。

### 核心特性

| 特性 | 说明 |
|------|------|
| **数据库引擎** | MySQL 8.0 兼容（基于 Vitess） |
| **数据库分支** | 类似 Git 分支，可在独立分支上测试 Schema 变更 |
| **无锁变更** | Schema 变更不会锁表，零停机迁移 |
| **自动扩容** | Serverless 架构，自动根据负载扩展 |
| **全球复制** | 支持多区域只读副本 |
| **连接方式** | HTTP（Serverless 友好）或 TCP |

### PlanetScale 适用场景

- 已有 MySQL 技术栈的团队
- 需要频繁变更数据库结构的项目
- 大规模读取场景（内容站、工具站）
- 需要全球多区域部署的应用

### 在 Next.js 中使用 PlanetScale

```bash
# 安装 PlanetScale Serverless 驱动
npm install @planetscale/database
```

```typescript
// lib/planetscale.ts
import { connect } from '@planetscale/database';

const config = {
  host: process.env.DATABASE_HOST,
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD,
};

export const conn = connect(config);

// 查询文章
export async function getArticleBySlug(slug: string) {
  const results = await conn.execute(
    'SELECT * FROM articles WHERE slug = ? AND status = ?',
    [slug, 'published']
  );
  return results.rows[0];
}

// 获取文章列表（带分页）
export async function getArticles(page: number = 1, limit: number = 20) {
  const offset = (page - 1) * limit;
  const results = await conn.execute(
    'SELECT * FROM articles WHERE status = ? ORDER BY published_at DESC LIMIT ? OFFSET ?',
    ['published', limit, offset]
  );
  return results.rows;
}
```

---

## MongoDB Atlas

### 概述

MongoDB Atlas 是 MongoDB 官方提供的全托管云数据库服务。作为文档型（NoSQL）数据库，MongoDB 适合处理灵活多变的数据结构。

### 核心特性

| 特性 | 说明 |
|------|------|
| **数据模型** | 文档型（JSON/BSON），无固定 Schema |
| **查询语言** | MongoDB Query Language (MQL) |
| **全文搜索** | 内置 Atlas Search（基于 Lucene） |
| **免费套餐** | M0 免费版：512 MB 存储、共享 RAM |
| **聚合管道** | 强大的数据聚合和分析能力 |
| **Change Streams** | 实时数据变更监听 |

### 免费套餐详情

| 资源 | 免费额度 |
|------|----------|
| 存储空间 | 512 MB |
| 共享 RAM | 是（共享集群） |
| 连接数 | 500 |
| 数据传输 | 10 GB/周 |
| 备份 | 无自动备份 |
| Atlas Search | 包含 |

### MongoDB Atlas 搭建流程

1. 访问 [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)，注册账号
2. 创建免费集群（M0），选择云服务商和区域
3. 设置数据库用户和密码
4. 配置 Network Access（添加 IP 白名单或允许所有 `0.0.0.0/0`）
5. 获取连接字符串

### 在 Next.js 中使用 MongoDB

```bash
npm install mongodb
```

```typescript
// lib/mongodb.ts
import { MongoClient, Db } from 'mongodb';

const uri = process.env.MONGODB_URI!;
const options = {};

let client: MongoClient;
let clientPromise: Promise<MongoClient>;

// 开发环境复用连接
if (process.env.NODE_ENV === 'development') {
  let globalWithMongo = global as typeof globalThis & {
    _mongoClientPromise?: Promise<MongoClient>;
  };
  if (!globalWithMongo._mongoClientPromise) {
    client = new MongoClient(uri, options);
    globalWithMongo._mongoClientPromise = client.connect();
  }
  clientPromise = globalWithMongo._mongoClientPromise;
} else {
  client = new MongoClient(uri, options);
  clientPromise = client.connect();
}

export default clientPromise;

// 获取数据库实例
export async function getDb(): Promise<Db> {
  const client = await clientPromise;
  return client.db('seo-site');
}
```

```typescript
// app/api/articles/route.ts
import { getDb } from '@/lib/mongodb';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const db = await getDb();
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') || '1');
  const limit = 20;

  const articles = await db
    .collection('articles')
    .find({ status: 'published' })
    .sort({ publishedAt: -1 })
    .skip((page - 1) * limit)
    .limit(limit)
    .toArray();

  return NextResponse.json(articles);
}
```

### MongoDB 适用场景

- 内容结构不固定的站点（不同类别的文章有不同字段）
- 需要全文搜索功能（Atlas Search 内置支持）
- 已有 MongoDB 经验的团队
- 原型开发阶段，Schema 频繁变动

---

## 三大数据库完整对比

| 维度 | Supabase | PlanetScale | MongoDB Atlas |
|------|----------|-------------|---------------|
| **数据库类型** | PostgreSQL（关系型） | MySQL（关系型） | MongoDB（文档型） |
| **免费套餐** | 500 MB 存储 | 无（最低 $39/月） | 512 MB 存储 |
| **连接方式** | REST API / 客户端 SDK | HTTP / TCP | 驱动连接 / REST API |
| **实时功能** | 内置 Realtime | 不支持 | Change Streams |
| **认证系统** | 内置 Auth | 不含 | 不含（需 Atlas App Services） |
| **文件存储** | 内置 Storage | 不含 | GridFS |
| **全文搜索** | PostgreSQL Full Text | 需外部服务 | Atlas Search（内置） |
| **扩展性** | 手动升级 | 自动 Serverless | 自动（M10+） |
| **学习曲线** | 低（有 Dashboard UI） | 中（MySQL + Vitess 概念） | 中（NoSQL 思维） |
| **适合 SEO 站** | 非常适合（一站式） | 适合（纯数据库） | 适合（灵活 Schema） |
| **ORM 支持** | Prisma、Drizzle、TypeORM | Prisma、Drizzle | Mongoose、Prisma |
| **SEO 相关优势** | 快速 API + Auth + Storage | 极低延迟查询 | 灵活文档 + 全文搜索 |

---

## SEO 站点数据库选型建议

### 内容站 / 博客站

```
推荐：Supabase
原因：
- 免费版足够起步
- 内置 Auth 可快速实现管理后台登录
- REST API 自动生成，无需手写接口
- PostgreSQL 全文搜索可做站内搜索
```

### 工具站 / SaaS

```
推荐：Supabase 或 PlanetScale
原因：
- 需要事务支持和数据一致性 → 关系型数据库
- 用户数据和计费信息需要严格的表结构
- Supabase 内置 Auth 减少开发量
- PlanetScale 的 Serverless 特性适合突发流量
```

### 聚合站 / 大规模内容

```
推荐：MongoDB Atlas
原因：
- 不同来源的数据结构可能不同 → 文档型更灵活
- Atlas Search 提供强大的全文搜索能力
- 水平扩展能力强，适合海量数据
```

---

## 使用 ORM 简化数据库操作

推荐使用 **Prisma** 或 **Drizzle ORM** 来管理数据库操作：

### Prisma 示例

```bash
npm install prisma @prisma/client
npx prisma init
```

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"  // 或 "mysql" (PlanetScale)
  url      = env("DATABASE_URL")
}

model Article {
  id              String    @id @default(uuid())
  title           String
  slug            String    @unique
  content         String?
  metaTitle       String?   @map("meta_title")
  metaDescription String?   @map("meta_description")
  status          String    @default("draft")
  publishedAt     DateTime? @map("published_at")
  createdAt       DateTime  @default(now()) @map("created_at")
  updatedAt       DateTime  @updatedAt @map("updated_at")
  author          User      @relation(fields: [authorId], references: [id])
  authorId        String    @map("author_id")
  category        Category? @relation(fields: [categoryId], references: [id])
  categoryId      String?   @map("category_id")

  @@index([slug])
  @@index([status, publishedAt(sort: Desc)])
  @@map("articles")
}
```

```typescript
// 使用 Prisma 查询
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// 获取已发布文章
const articles = await prisma.article.findMany({
  where: { status: 'published' },
  orderBy: { publishedAt: 'desc' },
  include: { category: true },
  take: 20,
});
```

---

## 数据库性能优化要点

### 对 SEO 影响最大的优化

1. **为 slug 字段添加索引**：文章详情页查询最频繁
2. **使用连接池**：避免频繁创建数据库连接
3. **善用缓存**：ISR + 数据库查询缓存双重保障
4. **只查询需要的字段**：避免 `SELECT *`，减少数据传输
5. **选择离目标用户最近的数据库区域**：降低网络延迟

```typescript
// 优化示例：只查询 SEO 相关字段
const { data } = await supabase
  .from('articles')
  .select('slug, title, meta_title, meta_description, published_at')
  .eq('status', 'published')
  .order('published_at', { ascending: false })
  .limit(50);
```
