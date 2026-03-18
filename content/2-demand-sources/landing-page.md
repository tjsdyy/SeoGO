---
title: 网站落地页找词
---

# 网站落地页找词

> 竞争对手的落地页（Landing Page）是经过反复测试和优化的——页面上出现的每一个关键词都经过了精心选择。通过分析竞品落地页，你可以快速获取已被验证有效的关键词，避免从零摸索。本节将介绍免费和付费两种竞品落地页找词方法。

---

## 一、为什么从落地页找词

### 1.1 落地页关键词的特殊价值

落地页与普通博客不同，它直接承接转化目标（注册、购买、咨询）。落地页上的关键词具有以下特点：

| 特点 | 说明 |
|------|------|
| 高转化意图 | 落地页目标是转化，关键词必须匹配用户购买意图 |
| 经过 A/B 测试 | 成熟产品的落地页标题经过多轮测试优化 |
| 产品-关键词匹配 | 落地页关键词与产品定位高度一致 |
| SEO + 付费双验证 | 好的落地页同时承接 SEO 和广告流量 |

### 1.2 哪些落地页值得分析

- **竞品产品首页**：核心产品定位关键词
- **竞品功能页（Feature Pages）**：功能相关的中腰关键词
- **竞品对比页（vs Pages）**：对比型关键词
- **竞品行业解决方案页**：行业细分关键词
- **竞品博客高流量页面**：内容型长尾关键词

---

## 二、免费方法：手动提取竞品落地页关键词

### 2.1 页面源码分析法

查看竞品落地页的 HTML 源码，提取 SEO 核心元素：

```
操作步骤：

1. 打开竞品落地页
2. 右键 → "查看页面源代码"（或 Ctrl+U / Cmd+U）
3. 提取以下元素：

<title>Best Project Management Software for Teams | Monday.com</title>
→ 关键词：project management software, project management for teams

<meta name="description" content="Monday.com is the #1 project
management tool for teams of all sizes. Plan, track, and manage
your work in one place.">
→ 关键词：project management tool, manage work, plan track manage

<h1>The Work OS that lets you shape workflows, your way</h1>
→ 关键词：work OS, workflows

<h2>Project management made simple</h2>
→ 关键词：project management simple
```

### 2.2 关键元素提取清单

| HTML 元素 | 关键词价值 | 提取方法 |
|-----------|-----------|---------|
| `<title>` | 主关键词 | 查看源码搜索 `<title>` |
| `<meta description>` | 主关键词 + 长尾词 | 搜索 `meta name="description"` |
| `<h1>` | 页面核心主题词 | 搜索 `<h1>` |
| `<h2>` / `<h3>` | 功能词 / 子话题词 | 搜索 `<h2>` |
| 图片 `alt` 属性 | 补充关键词 | 搜索 `alt=` |
| URL 路径 | 关键词意图信号 | 查看地址栏 |
| 内链锚文本 | 相关关键词 | 查看页面中的链接文字 |

### 2.3 Google 搜索运算符法

使用 Google 高级搜索运算符，系统化地找到竞品的各类落地页：

```
# 找到竞品所有被索引的页面
site:competitor.com

# 找到竞品特定类型的页面
site:competitor.com inurl:features
site:competitor.com inurl:solutions
site:competitor.com inurl:vs
site:competitor.com inurl:alternative

# 找到竞品包含特定关键词的页面
site:competitor.com "project management"
site:competitor.com "free trial"

# 找到竞品的高权重页面（通常有外链指向）
site:competitor.com intitle:"guide" OR intitle:"how to"
```

### 2.4 Chrome DevTools 批量提取

用浏览器控制台一键提取页面所有标题和元数据：

```javascript
// 在竞品落地页按 F12 打开 DevTools，Console 中执行：

// 提取所有 H1-H3 标题
document.querySelectorAll('h1, h2, h3').forEach(el => {
  console.log(`${el.tagName}: ${el.textContent.trim()}`)
});

// 提取 title 和 meta description
console.log('Title:', document.title);
console.log('Description:',
  document.querySelector('meta[name="description"]')?.content);

// 提取所有图片 alt 文本
document.querySelectorAll('img[alt]').forEach(img => {
  if(img.alt.trim()) console.log('IMG Alt:', img.alt.trim())
});
```

---

## 三、付费方法：专业工具深度分析

### 3.1 Ahrefs Site Explorer

Ahrefs 是竞品关键词分析的首选工具。

**操作路径**：Ahrefs → Site Explorer → 输入竞品域名

**核心功能一：Organic Keywords（有机关键词）**

筛选竞品所有获得自然排名的关键词：

| 筛选条件 | 推荐设置 | 目的 |
|---------|---------|------|
| Position | 1-10 | 只看排名靠前的高价值词 |
| Volume | > 100 | 排除无搜索量的词 |
| KD | 0-30 | 找到低竞争度的机会词 |
| Traffic | > 50 | 确保有实际流量 |

**核心功能二：Top Pages（流量最高页面）**

查看竞品哪些页面获得了最多的自然流量：

```
竞品 Top Pages 分析示例：

#1 competitor.com/blog/best-pm-tools
   流量：12,500/月 | 关键词数：350 | 内容类型：博客

#2 competitor.com/features
   流量：8,200/月 | 关键词数：180 | 内容类型：功能页

#3 competitor.com/vs/asana
   流量：5,100/月 | 关键词数：95 | 内容类型：对比页

#4 competitor.com/solutions/marketing
   流量：3,800/月 | 关键词数：120 | 内容类型：行业页

→ 洞察：竞品依赖博客内容获客，对比页是重要流量来源
```

**核心功能三：Content Gap（关键词差距）**

这是最直接的找词方法——找到竞品排名但你没有排名的关键词：

1. 在上方输入 2-3 个竞品域名
2. 在下方输入你自己的域名
3. 设置 "At least 2 of the targets should rank"
4. 按 Volume 降序排列
5. 筛选 KD < 40

### 3.2 SEMrush 竞品分析

**Keyword Gap 工具**

SEMrush 的 Keyword Gap 提供四种对比维度：

| 类型 | 含义 | 应用场景 |
|------|------|---------|
| Shared | 你和竞品都排名的词 | 找到需要优化超越的词 |
| Missing | 竞品排名但你完全没有 | 发现内容空白 |
| Weak | 你排名低于竞品的词 | 找到需要提升的词 |
| Unique | 你排名但竞品没有 | 发现你的竞争优势 |

> **重点关注 Missing 和 Weak 类型**——这些是最直接的增长机会。

**Position Changes（排名变化）**

监控竞品关键词排名的变化，捕捉时机：

- **新增（New）**：竞品新进入排名的词——可能是新发布的内容
- **下降（Declined）**：竞品排名下降的词——你的超越机会
- **丢失（Lost）**：竞品丢失排名的词——可能是内容过时

### 3.3 SimilarWeb 流量来源分析

SimilarWeb 可以查看竞品的整体流量构成，帮你判断哪些页面值得深入分析：

- 搜索流量占比（品牌词 vs 非品牌词）
- 引荐来源（哪些网站给竞品带流量）
- 热门页面访问量排序

---

## 四、关键词机会评分

从竞品落地页收集到大量关键词后，需要用评分模型确定优先级：

| 评分维度 | 权重 | 1 分 | 3 分 | 5 分 |
|---------|------|------|------|------|
| 搜索量 | 25% | < 100 | 100-1,000 | > 1,000 |
| 关键词难度（KD） | 25% | KD > 60 | KD 30-60 | KD < 30 |
| 业务相关度 | 30% | 弱相关 | 一般相关 | 强相关 |
| 竞品覆盖度 | 20% | 1 个竞品排名 | 2 个竞品排名 | 3+ 竞品排名 |

**计算公式**：`机会分 = 搜索量分 x 25% + KD分 x 25% + 相关度分 x 30% + 覆盖度分 x 20%`

优先执行机会分最高的关键词。

---

## 五、实战 SOP：竞品落地页找词流程

```
步骤 1：识别 3-5 个 SEO 竞品
  │  Google 搜索核心关键词，记录排名前 10 的域名
  │
  ▼
步骤 2：手动分析竞品核心落地页（免费）
  │  提取 title、meta description、H1-H3、URL 路径
  │  使用 Google site: 运算符找到所有页面类型
  │
  ▼
步骤 3：工具深度分析（付费）
  │  ├── Ahrefs Content Gap 找到关键词差距
  │  ├── Ahrefs Top Pages 分析流量页面
  │  └── SEMrush Keyword Gap 补充分析
  │
  ▼
步骤 4：整理到 Google Sheets
  │  合并去重，补充搜索量、KD、CPC 数据
  │
  ▼
步骤 5：关键词机会评分
  │  按评分模型打分，降序排列
  │
  ▼
步骤 6：制定内容计划
     ├── Top 10 关键词 → 立即创建内容
     ├── Top 11-30 → 本月内安排
     └── 其余 → 纳入季度计划
```

---

## 六、注意事项

- **不要抄袭竞品内容**：分析关键词可以，复制内容不行。你需要创作比竞品更好的原创内容
- **SEO 竞品 ≠ 商业竞品**：在 Google 搜索结果中与你竞争排名的网站才是 SEO 竞品，它们可能是博客、媒体或聚合站
- **定期更新分析**：建议每季度重新运行一次竞品分析，竞品的关键词策略在不断变化
- **结合自身优势**：不要盲目追逐竞品的所有关键词，选择与你自身产品/内容优势匹配的方向

---

## 七、本节检查清单

- [ ] 能手动从竞品落地页源码中提取关键 SEO 元素
- [ ] 掌握 Google 搜索运算符找到竞品各类页面
- [ ] 会使用 Chrome DevTools 批量提取页面信息
- [ ] 掌握 Ahrefs Content Gap 和 Top Pages 分析
- [ ] 了解 SEMrush Keyword Gap 的四种对比维度
- [ ] 能使用关键词机会评分模型确定优先级
- [ ] 建立了定期竞品落地页分析的流程
