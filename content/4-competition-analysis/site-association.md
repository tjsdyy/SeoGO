---
title: 站点关联分析
---

# 站点关联分析

> 很多 SEO 高手不止运营一个网站。通过 AdSense ID、Google Ads 账户、技术指纹等线索，你可以发现竞品背后的站群网络——同一个运营者可能拥有 5 个、10 个甚至更多相关站点。掌握站点关联分析技术，你就能看穿竞品的完整商业版图，发现更多竞争对手和市场机会。

---

## 一、为什么要做站点关联分析

### 1.1 竞品背后的隐藏帝国

在 SEO 领域，很多成功的运营者会同时运营多个网站，形成站群（Site Network）。他们可能：

- 在同一个 Niche 运营多个站点，占据更多搜索结果位置
- 在不同 Niche 分别运营站点，分散风险
- 用多个站点互相链接，形成 PBN（Private Blog Network）提升排名
- 通过矩阵式运营，最大化广告收入或联盟佣金

### 1.2 站点关联分析的价值

| 价值 | 说明 |
|------|------|
| 发现更多竞品 | 竞品可能运营着你不知道的其他站点 |
| 识别 PBN 风险 | 如果竞品在使用 PBN，他们的排名可能不稳定 |
| 了解竞品规模 | 站群规模反映竞品的资源和资金实力 |
| 发现新 Niche | 竞品的其他站点可能指向你没发现的赚钱 Niche |
| 学习运营策略 | 分析竞品的站群布局，学习其多站点运营策略 |

---

## 二、AdSense 关联分析

### 2.1 原理

Google AdSense 为每个发布商分配一个唯一的 Publisher ID（格式：`pub-XXXXXXXXXXXXXXXX`）。如果一个人的多个网站都使用同一个 AdSense 账号，它们的页面源代码中会包含相同的 Publisher ID。

### 2.2 手动查找 AdSense ID

**操作步骤**：

1. 打开竞品网站
2. 按 `Ctrl+U`（Windows）或 `Cmd+Option+U`（Mac）查看页面源代码
3. 搜索 `pub-`，查找 AdSense Publisher ID
4. 记录找到的 ID（如 `pub-1234567890123456`）

**常见的 AdSense 代码位置**：

```html
<!-- 在 <head> 或 <body> 中 -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1234567890123456"></script>

<!-- 或在广告单元代码中 -->
<ins class="adsbygoogle"
     data-ad-client="ca-pub-1234567890123456"
     data-ad-slot="9876543210"></ins>
```

### 2.3 使用 SpyOnWeb 反查关联站点

[SpyOnWeb](https://spyonweb.com/) 是专门用于发现关联站点的免费工具。

**操作步骤**：

1. 访问 `https://spyonweb.com/`
2. 输入竞品域名或 AdSense Publisher ID
3. 查看结果中列出的关联站点

**SpyOnWeb 结果解读**：

| 关联类型 | 含义 | 可信度 |
|---------|------|--------|
| Same Adsense ID | 使用相同 AdSense 账号 | 极高——同一个运营者 |
| Same Google Analytics ID | 使用相同 GA 账号 | 极高——同一个运营者 |
| Same IP Address | 托管在相同 IP 地址 | 中——可能是同一主机，也可能是共享主机 |
| Same Nameserver | 使用相同的 DNS 服务器 | 低——很多网站使用同一 DNS 服务商 |

### 2.4 批量查询示例

```
输入：example-tool.com
SpyOnWeb 返回结果：

AdSense ID: pub-1234567890123456
关联站点：
├── example-tool.com      (竞品本站)
├── another-tool.com      (同 Niche 的另一个站)
├── tool-reviews.com      (评测站)
├── best-software.net     (聚合站)
└── niche-blog.com        (内容站)

→ 发现竞品实际运营 5 个站点！
→ 其中 tool-reviews.com 和 best-software.net 可能互相链接
→ 需要进一步检查是否构成 PBN
```

---

## 三、Google Ads 关联分析

### 3.1 Google Ads 透明度中心

Google 在 2023 年推出了 [Ads Transparency Center](https://adstransparency.google.com/)，允许公众查看任何广告主在 Google 上投放的所有广告。

**操作步骤**：

1. 访问 `https://adstransparency.google.com/`
2. 搜索竞品品牌名或域名
3. 查看该广告主投放的所有广告
4. 注意广告中出现的不同域名——这些可能是同一运营者的不同站点

### 3.2 通过广告分析发现关联站点

| 分析维度 | 具体方法 | 发现意义 |
|---------|---------|---------|
| 同一广告主的不同落地页 | 查看广告指向的不同域名 | 发现竞品的多站点布局 |
| 相似广告文案 | 不同域名但文案风格一致 | 可能是同一团队运营 |
| 相同的转化追踪 ID | 页面源代码中的 Google Ads 转化标签 | 同一广告账户管理 |

### 3.3 搜索竞品广告的其他方法

**使用 SEMrush / SpyFu**：

```
操作路径（SEMrush）：
1. Advertising Research → 输入竞品域名
2. 查看 Competitors 标签
3. 关注"共同广告关键词"重叠度极高的站点
4. 如果两个站点的广告关键词重叠度 > 80%，可能是同一运营者

操作路径（SpyFu）：
1. 输入竞品域名 → Ad History
2. 查看历史广告中出现的其他域名
3. 交叉检查这些域名的 AdSense/Analytics ID
```

---

## 四、技术指纹分析

### 4.1 使用 BuiltWith 分析技术栈

[BuiltWith](https://builtwith.com/) 可以检测网站使用的所有技术工具，包括分析代码、广告平台、CMS 等。

**操作步骤**：

1. 访问 `https://builtwith.com/`
2. 输入竞品域名
3. 查看完整的技术栈报告
4. 重点关注以下"指纹"信息：

| 技术指纹 | 关联意义 | 可信度 |
|---------|---------|--------|
| Google Analytics ID（UA-XXXXXXX 或 G-XXXXXXX） | 同一 GA 账号 = 同一运营者 | 极高 |
| AdSense Publisher ID | 同一广告账号 | 极高 |
| Facebook Pixel ID | 同一 Facebook 广告账号 | 高 |
| 相同的 CDN 配置 | 可能是同一技术团队 | 中 |
| 相同的 CMS + 主题 | 可能是同一运营者 | 低-中 |
| 相同的自定义脚本 | 同一开发者 | 高 |

### 4.2 BuiltWith 的关联站点功能

BuiltWith 的付费版提供 **Relationship Profiles** 功能：

- 输入一个域名，自动列出使用相同技术 ID 的所有其他域名
- 可以按技术类型筛选（Analytics、Advertising、Email 等）
- 非常适合批量发现站群网络

### 4.3 使用 Wappalyzer 快速识别技术栈

[Wappalyzer](https://www.wappalyzer.com/) 是一个浏览器扩展，可以实时显示当前访问网站的技术栈。

**安装和使用**：

1. 在 Chrome Web Store 安装 Wappalyzer 扩展
2. 访问竞品网站，点击扩展图标
3. 查看列出的技术工具清单
4. 重点记录唯一标识性技术（如自定义字体、特定插件等）

---

## 五、其他关联发现技术

### 5.1 WHOIS 信息关联

虽然很多域名开启了隐私保护，但仍有一些信息可以用于关联分析：

| 信息 | 关联方法 |
|------|---------|
| 注册人邮箱 | 同一邮箱注册的所有域名可能属于同一人 |
| 注册人姓名 | 搜索同名注册的其他域名 |
| 注册商 | 仅参考，关联度低 |
| DNS 服务器 | 自建 DNS 的站点可能属于同一组织 |

**工具推荐**：

- **DomainTools Reverse WHOIS**：通过邮箱或姓名反查所有关联域名
- **ViewDNS.info**：提供 Reverse IP、Reverse WHOIS 等多种反查功能

### 5.2 IP 地址关联

如果多个网站托管在同一个 IP 地址上（且不是大型共享主机），它们很可能属于同一运营者。

**操作步骤**：

1. 使用 `nslookup` 或在线工具查询竞品网站的 IP 地址
2. 使用 **ViewDNS Reverse IP** 查看同一 IP 上的其他域名
3. 排除大型云主机商的共享 IP（这些IP上可能有数千个不相关网站）
4. 对于使用独立 IP 或小型主机的网站，关联度更高

### 5.3 SSL 证书关联

SSL 证书有时会覆盖多个域名（SAN 证书），检查证书详情可以发现关联域名：

```
查看 SSL 证书中的 SAN（Subject Alternative Names）：

1. 在浏览器中点击地址栏的锁图标
2. 查看证书详情
3. 查看"主题备用名称"(Subject Alternative Names) 字段
4. 列出的所有域名都是同一证书覆盖的 → 同一运营者
```

### 5.4 内容和设计风格关联

有时候，即使技术指纹都不同，通过内容和设计风格也能发现关联：

| 线索 | 说明 |
|------|------|
| 相似的页面布局和设计风格 | 同一设计师/模板 |
| 相同的写作风格和用语习惯 | 同一作者或团队 |
| 交叉链接 | 站点之间频繁互相链接 |
| 相同的 About 页面联系方式 | 同一公司/个人 |
| 相同的 Privacy Policy 模板 | 使用了相同的法律模板，可能同一运营者 |

---

## 六、站点关联分析实战工作流

### 6.1 完整分析流程

```
Step 1: 收集基础信息
    → 竞品域名列表（3-5 个核心竞品）
    → 使用 Wappalyzer/BuiltWith 记录每个竞品的技术指纹

Step 2: AdSense / Analytics ID 反查
    → 查看源代码提取 AdSense ID 和 GA ID
    → 使用 SpyOnWeb 反查关联站点
    → 记录发现的所有关联域名

Step 3: Google Ads 反查
    → 在 Ads Transparency Center 搜索竞品
    → 使用 SEMrush 查看广告竞品重叠度
    → 记录可疑的关联域名

Step 4: WHOIS + IP 反查
    → DomainTools / ViewDNS 反查
    → 记录共享 IP 或 WHOIS 信息的域名

Step 5: 交叉验证
    → 将所有发现的域名汇总
    → 对每个域名验证 2 种以上关联信号
    → 确认关联关系

Step 6: 绘制站群地图
    → 将确认的关联站点绘制成网络图
    → 标注站点间的链接关系
    → 分析站群的运营策略
```

### 6.2 站群地图示例

```
                    运营者 X
                       │
          ┌────────────┼────────────┐
          │            │            │
    ┌─────▼─────┐ ┌────▼────┐ ┌────▼────┐
    │ 主站 A     │ │ 站点 B  │ │ 站点 C  │
    │ (SaaS 产品)│ │ (评测站) │ │ (聚合站) │
    │ DR: 55    │ │ DR: 38  │ │ DR: 42  │
    └─────┬─────┘ └────┬────┘ └────┬────┘
          │            │            │
          └──── 互相链接 ────────────┘
                       │
              ┌────────┼────────┐
              │        │        │
         ┌────▼───┐ ┌──▼──┐ ┌──▼──┐
         │ 博客 D │ │ PBN │ │ PBN │
         │ DR: 25│ │  E  │ │  F  │
         └───────┘ └─────┘ └─────┘

分析发现：
- 运营者 X 拥有 6 个站点
- 站点 B 和 C 为主站 A 提供外链和引荐流量
- 博客 D 是内容输出站，为整个网络提供 Guest Post 支撑
- PBN E 和 F 是低质量链接站，存在被 Google 惩罚的风险
```

### 6.3 分析结论的应用

| 发现 | 应对策略 |
|------|---------|
| 竞品拥有 PBN | 竞品的排名基础不稳定，算法更新时可能暴跌 |
| 竞品通过评测站给自己导流 | 学习这种多站点矩阵策略，或联系第三方评测站获取你的评测 |
| 竞品的站群规模很大 | 竞品资源充沛，避免正面竞争，寻找其未覆盖的细分领域 |
| 竞品的多个站点互相链接 | 分析其链接结构，同时也可以向这些站点请求链接 |
| 发现竞品的新 Niche 站点 | 可能是竞品正在测试的新方向，密切关注 |

---

## 七、实操清单

- [ ] 查看 3-5 个竞品网站的源代码，提取 AdSense ID 和 GA ID
- [ ] 使用 SpyOnWeb 反查每个 ID 的关联站点
- [ ] 在 Google Ads Transparency Center 搜索竞品品牌
- [ ] 使用 BuiltWith 分析竞品的完整技术栈
- [ ] 使用 ViewDNS Reverse IP 检查竞品的 IP 关联
- [ ] 汇总所有发现的关联域名，交叉验证
- [ ] 绘制竞品站群地图
- [ ] 基于站群分析结论，调整你的竞争策略
