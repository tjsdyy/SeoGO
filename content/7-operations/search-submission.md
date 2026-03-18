---
title: 提交搜索引擎
---

# 提交搜索引擎

> 网站上线后，第一件事就是让搜索引擎发现并收录你的页面。本节详细讲解 Google Search Console 和 Bing Webmaster Tools 的配置、sitemap 与 robots.txt 的最佳实践，以及如何监控索引状态。

---

## Google Search Console 收录

### GSC 验证与设置

Google Search Console（GSC）是 Google 官方提供的免费站长工具，是 SEO 运营的必备基础设施。

**资源类型选择：**

| 类型 | 说明 | 推荐 |
|------|------|------|
| **网域资源** | 覆盖域名下的所有子域名和协议 | 推荐 |
| **网址前缀** | 只覆盖指定的 URL 前缀 | 简单情况可用 |

**设置流程：**

1. 访问 [search.google.com/search-console](https://search.google.com/search-console)
2. 点击"添加资源"（Add Property）
3. 选择"网域资源"，输入你的域名
4. **验证域名所有权**：
   - GSC 会给你一个 TXT 记录值
   - 到域名注册商（如 Cloudflare）添加 DNS TXT 记录
   - 回到 GSC 点击验证
   - 等待 DNS 生效（通常几分钟到几小时）

### 提交 Sitemap

验证完成后，立即提交 sitemap：

1. 在 GSC 左侧菜单选择"站点地图"（Sitemaps）
2. 输入你的 sitemap URL（通常是 `yourdomain.com/sitemap.xml`）
3. 点击提交
4. 确认状态为"成功"

### 请求索引

发布重要新内容后，可以手动请求索引加速收录：

1. 在 GSC 顶部的 URL 检查工具中输入新页面 URL
2. 等待检查完成
3. 如果显示"URL 不在 Google 中"，点击"请求编入索引"
4. 注意：每天有请求次数限制，仅对重要页面使用

### 索引覆盖率监控

索引覆盖率报告将你的所有页面分为四类：

```
┌─────────────┬──────────────────────────────────────┐
│   有效       │ 已成功编入索引的页面                    │
│   (Valid)    │ → 正常状态，持续监控数量变化            │
├─────────────┼──────────────────────────────────────┤
│   有效但有   │ 已索引但存在潜在问题                    │
│   警告       │ → 需要检查，可能影响排名                │
├─────────────┼──────────────────────────────────────┤
│   错误       │ 无法编入索引的页面                      │
│   (Error)    │ → 需要尽快修复                         │
├─────────────┼──────────────────────────────────────┤
│   已排除     │ Google 知道但选择不索引的页面            │
│   (Excluded) │ → 评估排除是否合理                     │
└─────────────┴──────────────────────────────────────┘
```

**常见索引问题及解决方案：**

| 状态 | 含义 | 解决方案 |
|------|------|---------|
| 已发现 - 尚未编入索引 | Google 知道 URL 但还没爬取 | 等待，或使用"请求编入索引" |
| 已抓取 - 尚未编入索引 | 已爬取但 Google 认为不值得索引 | 提升内容质量和独特性 |
| 已排除 - 被 robots.txt 屏蔽 | robots.txt 阻止了爬取 | 检查并修改 robots.txt |
| 已排除 - 被 noindex 标记排除 | 页面有 noindex 标签 | 移除 noindex（如果需要被索引） |
| 重复页面 - 选择了其他规范网址 | Google 选了另一个 URL 作为规范版本 | 检查 canonical 标签设置 |

### GSC 效果报告

GSC 的效果报告提供四个核心指标：

- **总点击次数**：用户从搜索结果中点击进入你网站的次数
- **总展示次数**：网页在搜索结果中出现的次数
- **平均点击率（CTR）**：点击次数 / 展示次数
- **平均排名**：网页在搜索结果中的平均位置

**高价值分析技巧：**

- **高展示低 CTR**：筛选展示次数高但 CTR < 2% 的查询，优化 Title 和 Description
- **排名临界点**：筛选平均排名 8-20 的关键词，这些只需小幅提升就能进入首页
- **正则表达式筛选**：使用 `^(?!.*brand).*$` 排除品牌词，专注非品牌流量分析

---

## 必应 Webmaster Tools

### 为什么要提交必应

虽然 Google 占据搜索市场的主导地位，但 Bing 仍然值得重视：

- Bing 在欧美市场有约 5-10% 的市场份额
- 微软 Edge 浏览器默认使用 Bing
- Bing 的竞争远小于 Google，更容易获得排名
- Bing Chat（Copilot）正在引入更多用户
- 提交到 Bing 只需要 10 分钟，投入产出比极高

### 设置流程

1. 访问 [bing.com/webmasters](https://www.bing.com/webmasters)
2. 使用 Microsoft 账号登录（或 Google 账号）
3. 添加你的网站
4. **验证方式**（三选一）：
   - **从 GSC 导入**（最快）：如果已有 GSC 验证，可直接导入
   - **DNS 验证**：添加 CNAME 记录到 DNS
   - **Meta 标签**：在首页 `<head>` 中添加 meta 标签
5. 提交 sitemap：输入 sitemap.xml URL

### 必应特有功能

| 功能 | 说明 | 使用建议 |
|------|------|---------|
| URL 提交 API | 可批量提交 URL 加速收录 | 新页面发布时使用 |
| IndexNow | 即时通知搜索引擎内容更新 | 推荐配置 |
| SEO 报告 | 自动生成站点 SEO 问题报告 | 每月查看 |
| 反向链接 | 查看 Bing 索引的外链数据 | 补充 Ahrefs 数据 |

### IndexNow 协议

IndexNow 是由 Bing 和 Yandex 联合推出的即时索引协议。配置后，网站内容更新时可以主动通知搜索引擎，无需等待爬虫发现。

**配置步骤：**

1. 到 [indexnow.org](https://www.indexnow.org/) 获取 API Key
2. 将 Key 文件放在网站根目录：`yourdomain.com/{key}.txt`
3. 内容更新时调用 API：

```bash
# 提交单个 URL
curl "https://api.indexnow.org/IndexNow?url=https://yourdomain.com/new-page&key=YOUR_KEY"

# 批量提交
curl -X POST "https://api.indexnow.org/IndexNow" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "yourdomain.com",
    "key": "YOUR_KEY",
    "urlList": [
      "https://yourdomain.com/page1",
      "https://yourdomain.com/page2"
    ]
  }'
```

---

## robots.txt 配置

### 基础配置

robots.txt 文件放在网站根目录，告诉搜索引擎哪些页面可以爬取，哪些不可以。

```
# robots.txt 基础模板

# 允许所有搜索引擎爬取所有页面
User-agent: *
Allow: /

# 禁止爬取管理后台
Disallow: /admin/
Disallow: /api/
Disallow: /dashboard/

# 禁止爬取搜索结果页（避免大量低质量页面被索引）
Disallow: /search?
Disallow: /*?sort=
Disallow: /*?filter=

# 声明 Sitemap 位置
Sitemap: https://yourdomain.com/sitemap.xml
```

### 常见错误与最佳实践

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 用 `Disallow: /` 屏蔽整站 | 所有页面无法被索引 | 仅屏蔽不需要索引的目录 |
| 屏蔽了 CSS/JS 文件 | Google 无法正确渲染页面 | 不要屏蔽静态资源 |
| 没有声明 Sitemap | 搜索引擎可能找不到 sitemap | 在 robots.txt 末尾声明 |
| 使用 robots.txt 阻止敏感页面 | robots.txt 是公开可见的 | 敏感页面使用 noindex 或登录保护 |

> **重要**：robots.txt 只是"建议"，不是"命令"。Google 可能仍然会索引被 Disallow 的页面（如果有外链指向它）。要完全阻止索引，需要使用 `<meta name="robots" content="noindex">` 标签。

---

## sitemap.xml 配置

### 标准格式

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourdomain.com/</loc>
    <lastmod>2026-03-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://yourdomain.com/blog/seo-guide</loc>
    <lastmod>2026-03-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Sitemap 最佳实践

| 要点 | 说明 |
|------|------|
| 只包含规范 URL | 不要包含重定向页面、noindex 页面或非规范 URL |
| lastmod 真实有效 | 只在内容真正更新时修改 lastmod，不要自动更新 |
| 大型网站使用索引 | 每个 sitemap 最多 50,000 个 URL 或 50MB |
| 动态生成 | 使用 CMS 或框架自动生成 sitemap，避免手动维护 |
| 提交到所有搜索引擎 | 同时提交到 GSC 和 Bing Webmaster Tools |

### Sitemap 索引文件

当网站页面超过 50,000 时，使用 Sitemap 索引文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://yourdomain.com/sitemap-pages.xml</loc>
    <lastmod>2026-03-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://yourdomain.com/sitemap-blog.xml</loc>
    <lastmod>2026-03-14</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://yourdomain.com/sitemap-products.xml</loc>
    <lastmod>2026-03-13</lastmod>
  </sitemap>
</sitemapindex>
```

---

## 索引状态监控

### 日常监控清单

| 检查项 | 工具 | 频率 | 关注点 |
|-------|------|------|-------|
| 索引页面数量趋势 | GSC 覆盖率报告 | 每周 | 数量是否与实际页面数匹配 |
| 索引错误 | GSC 错误报告 | 每周 | 5xx 错误、404 页面需及时修复 |
| 新页面收录速度 | GSC URL 检查 | 每次发布后 | 重要页面 48 小时内应被发现 |
| 爬取统计 | GSC 设置 → 爬取统计 | 每月 | 爬取频率和响应时间是否正常 |
| Bing 索引状态 | Bing Webmaster Tools | 每两周 | Bing 的收录情况 |

### 爬取预算优化

对于大型网站，需要优化爬取预算（Crawl Budget），确保重要页面被优先爬取：

| 优化项 | 具体操作 | 优先级 |
|--------|---------|--------|
| 清理低质量页面 | 合并或删除薄内容页面 | 高 |
| 处理重复内容 | 设置 canonical 标签 | 高 |
| 修复 HTTP 状态错误 | 处理 404、500 等错误 | 高 |
| 优化 URL 参数 | 避免大量参数化 URL | 中 |
| 减少重定向链 | 直接跳转到最终 URL | 中 |

### 索引健康度指标

| 指标 | 目标值 | 计算方式 |
|------|--------|----------|
| 索引率 | >95% | 已索引页面数 / 需要索引的总页面数 |
| 错误页面比例 | <2% | 错误页面数 / 总页面数 |
| 平均收录速度 | <72 小时 | 从发布到首次被爬取的时间 |

---

## 实操清单

- [ ] GSC 已验证域名所有权（推荐网域资源）
- [ ] 已在 GSC 中提交 sitemap.xml
- [ ] Bing Webmaster Tools 已配置（可从 GSC 导入）
- [ ] robots.txt 配置正确，未屏蔽重要页面
- [ ] sitemap.xml 包含所有需要索引的页面
- [ ] 新页面发布后使用 GSC URL 检查请求索引
- [ ] 每周检查 GSC 索引覆盖率报告
- [ ] 已配置 IndexNow 协议（可选但推荐）
- [ ] 已设置爬取错误的邮件通知
