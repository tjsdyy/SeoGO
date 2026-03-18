---
title: 落地页设计
---

# 落地页设计

> 落地页（Landing Page）是用户通过搜索、广告或社交媒体进入你网站后看到的第一个页面，它直接决定了用户是否会留下来、是否会转化。一个高转化的落地页通常由六大核心组件构成：Hero Section、About Section、FAQ Section、案例（Case Studies）、表单（Form）和评论（Reviews）。本节将逐一拆解每个组件的设计要点和 SEO 最佳实践。

---

## 一、落地页整体架构

### 1.1 六大组件布局

一个完整的高转化落地页通常按以下顺序排列：

```
┌─────────────────────────────────────┐
│          Hero Section               │
│   标题 + 副标题 + CTA + 主图        │
├─────────────────────────────────────┤
│          About Section              │
│   品牌故事 + 信任背书               │
├─────────────────────────────────────┤
│          案例 / Case Studies        │
│   社会证明 + 客户证言               │
├─────────────────────────────────────┤
│          FAQ Section                │
│   常见问题 + Schema 标记            │
├─────────────────────────────────────┤
│          评论 / Reviews             │
│   用户评价 + UGC 内容               │
├─────────────────────────────────────┤
│          Form 表单                  │
│   信息收集 + 转化入口               │
└─────────────────────────────────────┘
```

> **注意**：以上顺序不是固定的。根据你的业务模式和用户行为数据，可以灵活调整组件的位置和组合。核心原则是：**让用户在最短的路径内完成"了解 → 信任 → 行动"**。

### 1.2 落地页的 HTML 语义化

落地页同样需要遵循 HTML 语义化原则，确保搜索引擎能正确理解页面结构：

```html
<main>
  <section id="hero" aria-label="Hero">
    <h1>页面主标题（包含主关键词）</h1>
    <!-- Hero 内容 -->
  </section>

  <section id="about" aria-label="About">
    <h2>关于我们 / 为什么选择我们</h2>
    <!-- About 内容 -->
  </section>

  <section id="cases" aria-label="Case Studies">
    <h2>客户案例</h2>
    <!-- 案例内容 -->
  </section>

  <section id="faq" aria-label="FAQ">
    <h2>常见问题</h2>
    <!-- FAQ 内容 -->
  </section>

  <section id="reviews" aria-label="Reviews">
    <h2>用户评价</h2>
    <!-- 评论内容 -->
  </section>

  <section id="contact" aria-label="Contact Form">
    <h2>立即开始 / 联系我们</h2>
    <!-- 表单内容 -->
  </section>
</main>
```

---

## 二、Hero Section 设计

### 2.1 Hero Section 的作用

Hero Section 是用户进入页面后 **第一眼看到的区域**（Above the Fold），通常在 3 秒内决定用户是继续浏览还是离开。它需要在最短时间内传达三个信息：**你是谁、你能解决什么问题、用户下一步该做什么**。

### 2.2 四大核心元素

**1. 主标题（Headline / H1）**

| 要点 | 说明 |
|------|------|
| 包含主关键词 | 同时服务 SEO 和用户理解 |
| 聚焦用户价值 | 不说"我们做什么"，说"你能得到什么" |
| 简短有力 | 控制在 10-15 个英文单词以内 |
| 与 Title Tag 语义一致 | H1 和 Title 可以不完全相同，但主题必须一致 |

```
❌ "Welcome to Our Website"（没有信息量）
❌ "We are the Leading AI-Powered SEO Platform"（以自己为中心）

✅ "Rank Higher on Google with AI-Powered SEO Tools"（聚焦用户价值 + 包含关键词）
✅ "Find Profitable Keywords in Seconds"（简短、有力、聚焦）
```

**2. 副标题（Subheadline）**

副标题是对主标题的补充说明，通常 1-2 句话，解释具体如何实现主标题中的承诺。

```
主标题：Find Profitable Keywords in Seconds
副标题：Our AI analyzes 10 billion search queries to find low-competition,
        high-traffic keywords your competitors are missing.
```

**3. CTA 按钮（Call to Action）**

| 要点 | 说明 |
|------|------|
| 动作导向 | 使用动词开头：Start、Get、Try、Download |
| 降低门槛 | "Start Free Trial" 比 "Buy Now" 转化率高 |
| 视觉突出 | 对比色按钮，足够大，周围留白 |
| 唯一性 | Hero Section 只放一个主 CTA |

```
✅ 高转化 CTA 示例：
- "Start Your Free Trial"
- "Get Your Free SEO Audit"
- "Try It Free — No Credit Card Required"
- "Download Free Template"

❌ 低转化 CTA 示例：
- "Learn More"（太模糊）
- "Submit"（太冷冰冰）
- "Click Here"（没有价值传达）
```

**4. Hero Image / 视觉元素**

| 类型 | 适用场景 | SEO 注意事项 |
|------|---------|-------------|
| 产品截图 | SaaS、工具类 | Alt 文本包含产品名和功能描述 |
| 演示视频 | 需要解释复杂功能时 | 提供视频文字稿（Transcript） |
| 插图/动画 | 品牌化设计 | 控制文件大小，使用 WebP 格式 |
| 数据展示 | 突出成果和效果 | 使用真实数据，标注来源 |

> **性能提醒**：Hero Image 是首屏资源，必须做好性能优化。建议使用 WebP 格式、设置 width/height 属性防止布局偏移（CLS）、对首屏图片使用 `loading="eager"`。

---

## 三、About Section 设计

### 3.1 About Section 的目的

About Section 的核心目标是 **建立信任**。用户在了解你能解决什么问题后，接下来会问："为什么我应该相信你？"

### 3.2 信任建设的四个层面

**层面一：品牌故事**

简短讲述品牌的起源和使命，让用户产生情感连接。

```
模板：
"[品牌名] 成立于 [年份]，源于 [创始人] 在 [场景] 中发现的 [问题]。
我们的使命是 [使命描述]。如今，我们已帮助 [数量] 位 [用户类型] 实现 [成果]。"
```

**层面二：数据背书**

用具体数字展示实力：

```
✅ "服务 10,000+ 企业客户"
✅ "处理 50 亿次搜索查询"
✅ "平均提升 47% 的有机流量"
✅ "4.8/5 用户评分（来自 2,000+ 条评价）"
```

**层面三：权威认证**

展示行业认证、媒体报道、合作伙伴 Logo。

```html
<!-- 媒体报道 Logo 展示 -->
<div class="media-logos" aria-label="Featured in">
  <p>As seen in:</p>
  <img src="techcrunch.svg" alt="TechCrunch" width="120" height="30">
  <img src="forbes.svg" alt="Forbes" width="100" height="30">
  <img src="producthunt.svg" alt="Product Hunt" width="130" height="30">
</div>
```

**层面四：团队展示**

展示创始团队或核心成员的真实照片和专业背景，增强 E-E-A-T 信号。

### 3.3 About Section 的 SEO 写法

- H2 标题包含次要关键词（如 "Why Choose [Brand] for [Service]"）
- 正文自然融入语义相关词
- 数据和成就用结构化的列表或统计卡片展示
- 为团队成员添加 Person Schema 标记

---

## 四、FAQ Section 设计

### 4.1 FAQ 对 SEO 的价值

FAQ Section 是落地页中 SEO 价值最高的组件之一：

1. **覆盖长尾关键词**：每个 FAQ 问题都是一个潜在的长尾关键词
2. **争取 Featured Snippet**：简洁的问答格式容易被 Google 提取为精选摘要
3. **占据 People Also Ask**：FAQ 内容有机会出现在 PAA 框中
4. **FAQPage Schema**：添加结构化数据后，搜索结果中会展示 FAQ 富文本

### 4.2 FAQ 问题选取策略

| 来源 | 方法 |
|------|------|
| Google PAA | 搜索目标关键词，收集 People Also Ask 中的问题 |
| AlsoAsked.com | 批量获取关键词的关联问题 |
| AnswerThePublic | 获取问题型关键词 |
| 客服/销售常见问题 | 从内部团队收集用户真实疑问 |
| 竞品 FAQ | 分析竞品落地页的 FAQ 内容 |
| Search Console | 查看用户实际搜索的问题型查询 |

### 4.3 FAQ 内容写作规范

```markdown
## 常见问题

### [问题1：使用用户的自然语言]

[直接回答，2-3 句话，40-60 词。先给结论，再做补充说明。]

### [问题2：包含目标关键词的变体]

[直接回答，简洁清晰。]
```

**写作要点**：
- 问题使用用户搜索的自然语言，而非企业内部术语
- 答案开头直接给结论，不要绕弯子
- 每个答案控制在 50-100 词
- 适当在答案中包含内链到相关页面

### 4.4 FAQPage Schema 标记

为 FAQ Section 添加 FAQPage 结构化数据，可以在 Google 搜索结果中展示 FAQ 富文本，显著增加 SERP 占据面积：

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is keyword research?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Keyword research is the process of finding and analyzing search terms that people enter into search engines. It helps you understand what your target audience is looking for and create content that matches their needs."
      }
    },
    {
      "@type": "Question",
      "name": "How long does SEO take to work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO typically takes 3-6 months to show significant results. However, the timeline depends on factors like website age, competition level, content quality, and link building efforts."
      }
    }
  ]
}
```

---

## 五、案例 Section（Case Studies / 社会证明）

### 5.1 社会证明的 SEO 价值

案例和证言不仅提升转化率，还为页面贡献 UGC（用户生成内容）和语义丰富度，有助于覆盖更多长尾关键词。

### 5.2 案例展示的四种形式

**形式一：客户证言（Testimonials）**

```markdown
> "使用 [产品] 三个月后，我们的有机流量增长了 156%，
> 关键词排名前 10 的数量从 12 个增加到 87 个。"
>
> — **张明，某科技公司 SEO 负责人**
```

展示要点：
- 包含具体数据（不是"效果很好"，而是"增长 156%"）
- 附上真实姓名、职位和公司（经授权）
- 配上头像照片增加真实感

**形式二：案例研究卡片**

```
案例：[公司名] 如何用 [产品] 在 6 个月内提升 200% 有机流量

挑战：[简述客户面临的问题]
方案：[简述使用你的产品/服务的解决方案]
成果：[列出 2-3 个关键数据指标]

→ 阅读完整案例
```

**形式三：Logo 墙**

展示知名客户的 Logo，快速建立信任。

**形式四：数据统计**

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  10,000+  │  │   47%    │  │  4.8/5   │
│  企业用户  │  │ 平均流量  │  │  用户评分  │
│          │  │  增长率    │  │          │
└──────────┘  └──────────┘  └──────────┘
```

### 5.3 案例 Section 的 Schema 标记

为客户证言添加 Review Schema：

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "你的产品名",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "2156"
  },
  "review": [
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "张明"
      },
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5"
      },
      "reviewBody": "使用三个月后，有机流量增长了 156%。"
    }
  ]
}
```

---

## 六、Form 表单设计

### 6.1 表单的核心原则

表单是落地页的转化终点。一个好的表单设计需要在"获取足够信息"和"降低用户填写门槛"之间找到平衡。

### 6.2 表单设计最佳实践

| 要点 | 说明 |
|------|------|
| 字段最少化 | 每多一个字段，转化率下降约 10%。初次转化只要邮箱即可 |
| 分步表单 | 长表单拆分为 2-3 步，降低心理压力 |
| 进度指示 | 多步表单显示"第 1 步 / 共 3 步" |
| 按钮文案 | 使用价值导向文案代替"提交"："Get My Free Report" |
| 隐私声明 | 在表单下方注明隐私政策（GDPR/CCPA 合规） |
| 社交登录 | 提供 Google/GitHub 一键登录降低门槛 |

### 6.3 表单转化率优化技巧

**技巧一：在表单旁添加信任信号**

```
[表单区域]                  [信任信号]
┌──────────────────┐       ✓ 30 天免费试用
│ Email:           │       ✓ 无需信用卡
│ ________________ │       ✓ 随时可取消
│                  │       ✓ 10,000+ 用户信赖
│ [Get Free Trial] │       ⭐⭐⭐⭐⭐ 4.8/5 评分
└──────────────────┘
```

**技巧二：退出意图弹窗（Exit Intent Popup）**

当用户即将离开页面时，显示一个简化版的转化弹窗，提供额外的激励：

```
即将离开？获取我们的免费 SEO 检查清单

[您的邮箱地址]
[立即获取]

已有 5,000+ 人下载
```

**技巧三：A/B 测试关键要素**

建议优先测试以下要素（按影响排序）：

1. CTA 按钮文案
2. 表单字段数量
3. 标题/价值主张
4. 表单位置
5. 信任信号的内容和位置

### 6.4 表单与 SEO

表单本身对 SEO 没有直接影响，但需要注意：

- 不要用 JavaScript 动态渲染整个表单区域（影响爬虫）
- 表单的 `<label>` 标签有助于可访问性
- "Thank You" 页面可以设置为 `noindex`，避免稀释爬虫预算

---

## 七、评论 / Reviews Section 设计

### 7.1 UGC 对 SEO 的价值

用户生成内容（User Generated Content）对 SEO 有多重价值：

| 价值维度 | 说明 |
|---------|------|
| 新鲜内容 | 用户不断产生的新评论向 Google 发送"内容在更新"的信号 |
| 长尾关键词 | 用户用自然语言描述产品，覆盖你可能想不到的长尾词 |
| 信任信号 | 真实评价增强 E-E-A-T 中的 Trustworthiness |
| 富文本展示 | Review Schema 可以让搜索结果显示星级评分 |

### 7.2 评论展示设计

**基础展示结构**：

```html
<div class="review" itemscope itemtype="https://schema.org/Review">
  <div class="review-rating">
    <span itemprop="reviewRating" itemscope itemtype="https://schema.org/Rating">
      <meta itemprop="ratingValue" content="5">
      ⭐⭐⭐⭐⭐
    </span>
  </div>
  <blockquote itemprop="reviewBody">
    "评价内容..."
  </blockquote>
  <cite itemprop="author" itemscope itemtype="https://schema.org/Person">
    <span itemprop="name">用户姓名</span>
  </cite>
  <time itemprop="datePublished" datetime="2025-01-15">2025年1月15日</time>
</div>
```

### 7.3 评论管理最佳实践

| 实践 | 说明 |
|------|------|
| 鼓励真实评论 | 购买/使用后发送邮件邀请评价 |
| 回复所有评论 | 包括差评——展示你重视反馈 |
| 不删除差评 | 全是五星好评反而降低可信度 |
| 标注验证状态 | "已验证购买"标签增加真实感 |
| 评论内容审核 | 过滤垃圾内容和敏感信息，但保留真实负面反馈 |

### 7.4 聚合评分的 Schema 标记

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "产品名称",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "bestRating": "5",
    "ratingCount": "2156"
  }
}
```

> **注意**：Google 对 Review Schema 的使用有严格要求。不允许为整个网站或品牌添加 Review Schema（只允许产品、服务、课程等具体实体），不允许自己给自己写评价并标记 Schema。

---

## 八、落地页 SEO 综合清单

### 技术层面

```
□ H1 唯一且包含主关键词
□ H2 用于各 Section 标题，包含次要关键词
□ H3 用于 Section 内的子内容
□ 标题层级正确嵌套，不跳级
□ 每个 Section 使用 <section> 标签和 aria-label
□ 图片使用 WebP 格式，设置 alt、width、height
□ 首屏加载时间 < 2.5 秒（LCP 指标）
□ 移动端完全响应式适配
```

### 内容层面

```
□ Hero 标题清晰传达价值主张
□ About Section 包含数据背书和信任信号
□ FAQ 覆盖用户常见问题和长尾关键词
□ 案例包含具体数据和真实客户信息
□ 评论展示真实用户反馈
□ CTA 文案动作导向、降低门槛
```

### 结构化数据

```
□ FAQPage Schema 已添加
□ Product / Service Schema 已添加
□ AggregateRating Schema 已添加（如有评分）
□ Organization Schema 已添加
□ BreadcrumbList Schema 已添加
□ 通过 Google Rich Results Test 验证通过
```

---

## 九、本节要点回顾

- 落地页由六大核心组件构成：Hero、About、FAQ、案例、表单、评论
- Hero Section 需要在 3 秒内传达价值主张，H1 包含主关键词
- About Section 通过数据、认证、团队展示建立信任
- FAQ Section 是 SEO 价值最高的组件，配合 FAQPage Schema 可获得富文本展示
- 案例和评论提供社会证明，UGC 内容贡献长尾关键词和新鲜度信号
- 表单设计需要平衡信息获取和用户体验，字段越少转化率越高
- 所有组件都应遵循 HTML 语义化和标题层级规范
