---
title: 上线部署
---

# 上线部署

> 网站开发完成后，选择合适的部署方案直接影响页面加载速度、SEO 表现和运维成本。本节详细对比三种主流部署方式——独立服务器（VPS）、Vercel 和 Cloudflare Pages，并提供完整的部署操作指南。

---

## 部署方案概览

部署方案的选择取决于你的项目类型、技术栈和预算：

| 部署方式 | 适用场景 | 月费参考 | 技术门槛 |
|----------|----------|----------|----------|
| 独立服务器（VPS） | 全栈应用、WordPress、需要完全控制 | $5-100 | 高 |
| Vercel | Next.js 项目、React 应用 | $0-20 | 低 |
| Cloudflare Pages | 静态站点、Astro/Hugo 项目 | $0 | 低 |

---

## 方案一：独立服务器（VPS/云服务器）

### 适用场景

- WordPress 或其他传统 CMS 站点
- 需要运行后端服务（Node.js、Python、数据库）
- 需要完全控制服务器环境
- 多站点统一管理

### 主流 VPS 供应商对比

| 供应商 | 最低月费 | 数据中心 | 特点 |
|--------|----------|----------|------|
| **Vultr** | $2.5/月 | 32 个城市 | 按小时计费、全球节点多 |
| **DigitalOcean** | $4/月 | 15 个城市 | 文档优秀、一键安装镜像多 |
| **Linode (Akamai)** | $5/月 | 25+ 个城市 | 稳定、性价比高 |
| **Hetzner** | ~$3.5/月 | 欧洲+美国 | 欧洲市场首选、极高性价比 |
| **AWS Lightsail** | $3.5/月 | 全球 | AWS 生态、简化版 VPS |

### VPS 部署完整流程（以 Ubuntu + Next.js 为例）

#### 第一步：购买与初始化服务器

```bash
# 以 DigitalOcean 为例，创建 Droplet 后通过 SSH 连接
ssh root@your-server-ip

# 更新系统
apt update && apt upgrade -y

# 创建非 root 用户
adduser deploy
usermod -aG sudo deploy

# 配置 SSH 密钥登录（更安全）
su - deploy
mkdir ~/.ssh
chmod 700 ~/.ssh
# 将你的公钥粘贴到 authorized_keys
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

#### 第二步：安装运行环境

```bash
# 安装 Node.js（使用 nvm）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20

# 安装 PM2（进程管理）
npm install -g pm2

# 安装 Nginx（反向代理）
sudo apt install nginx -y
```

#### 第三步：部署项目

```bash
# 克隆项目
cd /home/deploy
git clone https://github.com/your-username/your-project.git
cd your-project

# 安装依赖并构建
npm install
npm run build

# 使用 PM2 启动
pm2 start npm --name "my-site" -- start
pm2 save
pm2 startup  # 设置开机自启
```

#### 第四步：配置 Nginx 反向代理

```nginx
# /etc/nginx/sites-available/my-site
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # 安全头
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # 静态文件缓存
    location /_next/static/ {
        alias /home/deploy/your-project/.next/static/;
        expires 365d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location /public/ {
        alias /home/deploy/your-project/public/;
        expires 30d;
        access_log off;
    }

    # 反向代理到 Next.js
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# 启用站点配置
sudo ln -s /etc/nginx/sites-available/my-site /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 安装 SSL 证书（Let's Encrypt）
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### VPS 部署的优势与劣势

**优势：**
- 完全控制服务器环境，可安装任何软件
- 适合多站点管理，一台 VPS 可托管多个网站
- 长期成本可预测，不会因流量突增产生高额账单
- 可以运行后台任务（爬虫、数据处理等）

**劣势：**
- 需要自行维护服务器安全和更新
- 没有自动扩容，高峰流量需要提前规划
- 部署流程较为繁琐，需要 DevOps 知识
- SSL 证书需要手动续签（或配置自动续签）

---

## 方案二：Vercel 部署

### 适用场景

- Next.js 项目（Vercel 是 Next.js 官方团队的公司）
- React / Nuxt.js / SvelteKit 等现代前端框架
- 需要 Serverless Functions 的项目
- 追求零运维体验

### Vercel 部署步骤（Next.js 项目）

#### 第一步：准备项目

确保项目根目录有以下文件结构：

```
my-project/
├── app/            # App Router 目录
├── public/         # 静态资源
├── package.json
├── next.config.mjs
└── vercel.json     # Vercel 配置（可选）
```

#### 第二步：连接 Git 仓库并部署

1. 访问 [vercel.com](https://vercel.com)，使用 GitHub 账号登录
2. 点击 "Add New Project"
3. 选择你的 GitHub 仓库
4. Vercel 会自动检测 Next.js 框架
5. 配置环境变量（如果有）
6. 点击 "Deploy"

部署通常在 30-90 秒内完成。

#### 第三步：配置自定义域名

1. 在 Vercel Dashboard 进入项目 Settings > Domains
2. 添加你的域名（如 `yourdomain.com`）
3. 按照提示在 DNS 服务商处添加记录：
   - A 记录：`76.76.21.21`
   - CNAME 记录：`cname.vercel-dns.com`
4. SSL 证书自动签发，无需手动配置

#### 第四步：配置 vercel.json（SEO 优化）

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    },
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "statusCode": 301
    }
  ]
}
```

#### 第五步：配置环境变量

```bash
# 通过 Vercel CLI 设置环境变量
npm i -g vercel
vercel login

# 添加环境变量
vercel env add DATABASE_URL
vercel env add STRIPE_SECRET_KEY

# 或在 Dashboard > Settings > Environment Variables 中添加
```

### Vercel 免费版与 Pro 版对比

| 功能 | Hobby（免费） | Pro（$20/月） |
|------|--------------|---------------|
| 带宽 | 100 GB/月 | 1 TB/月 |
| Serverless 函数执行 | 100 GB-小时 | 1000 GB-小时 |
| 构建时间 | 6000 分钟/月 | 24000 分钟/月 |
| 团队成员 | 1 人 | 无限 |
| 分析 | 基础 | 高级 |
| 自定义域名 | 支持 | 支持 |
| DDoS 防护 | 基础 | 高级 |
| 支持 | 社区 | 邮件支持 |

### Vercel 的 SEO 优势

- **Edge Network**：全球 CDN，自动将内容分发到离用户最近的节点
- **自动 HTTPS**：SSL 证书自动签发和续签
- **ISR 支持**：增量静态再生，兼顾性能和内容更新
- **Image Optimization**：内置图片优化 API，自动 WebP 转换
- **Web Analytics**：内置性能监控，直观查看 Core Web Vitals

---

## 方案三：Cloudflare Pages 部署

### 适用场景

- 静态网站和 JAMstack 应用
- Astro、Hugo、Gatsby 等 SSG 框架
- 需要无限带宽的项目
- 已经使用 Cloudflare 管理 DNS 的项目

### Cloudflare Pages 部署步骤

#### 第一步：连接 Git 仓库

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 进入 Workers & Pages > Create application > Pages
3. 连接你的 GitHub 或 GitLab 仓库
4. 选择要部署的仓库

#### 第二步：配置构建设置

| 框架 | 构建命令 | 输出目录 |
|------|----------|----------|
| Astro | `npm run build` | `dist` |
| Hugo | `hugo` | `public` |
| Next.js (静态) | `npx @cloudflare/next-on-pages` | `.vercel/output/static` |
| Gatsby | `npm run build` | `public` |
| 纯 HTML | 无需构建 | `/` |

#### 第三步：设置环境变量和自定义域名

```bash
# 使用 Wrangler CLI（Cloudflare 官方工具）
npm install -g wrangler
wrangler login

# 部署
wrangler pages deploy ./dist --project-name=my-site

# 添加自定义域名（在 Dashboard 中操作更方便）
# Pages > 项目 > Custom domains > Set up a custom domain
```

#### 第四步：配置重定向和 Headers

```
# public/_redirects
/old-page    /new-page    301
/blog/old    /blog/new    301

# public/_headers
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin

/static/*
  Cache-Control: public, max-age=31536000, immutable
```

### Cloudflare Pages 的核心优势

- **无限带宽**：免费版不限制带宽，对高流量站点非常友好
- **全球 300+ 节点**：Cloudflare 的 CDN 网络覆盖全球
- **与 Cloudflare 生态集成**：DNS、WAF、Workers、R2 无缝配合
- **每月 500 次构建**：免费版足够大部分项目使用
- **预览部署**：每个 Pull Request 自动生成预览 URL

---

## 三种方案完整对比

| 维度 | VPS | Vercel | Cloudflare Pages |
|------|-----|--------|-----------------|
| **月费** | $5-100 | $0-20 | $0 |
| **带宽** | 按配置（通常 1-5TB） | 100GB（免费）/ 1TB（Pro） | 无限 |
| **适用框架** | 全部 | Next.js 最优、支持多框架 | SSG 为主、支持 Next.js |
| **SSR 支持** | 完全支持 | 完全支持 | 通过 Workers 支持 |
| **数据库** | 可自行安装 | 需外部服务 | 需外部服务 |
| **构建速度** | 取决于服务器配置 | 快（云端构建） | 快（云端构建） |
| **自动部署** | 需配置 CI/CD | Git 推送自动部署 | Git 推送自动部署 |
| **SSL 证书** | 手动（Let's Encrypt） | 自动 | 自动 |
| **DDoS 防护** | 需自行配置 | 内置基础防护 | 内置企业级防护 |
| **扩容能力** | 手动扩容 | 自动扩容 | 自动扩容 |
| **运维难度** | 高 | 极低 | 极低 |
| **自定义能力** | 最高 | 中等 | 中等 |

---

## 部署方案选型决策

```
你的项目需求？
│
├── Next.js 全栈项目，需要 SSR/ISR？
│   └── Vercel（官方支持，体验最佳）
│
├── 静态站点（Astro/Hugo/博客）？
│   └── Cloudflare Pages（无限带宽，完全免费）
│
├── WordPress 或需要数据库的传统应用？
│   └── VPS（完全控制，可安装任何服务）
│
├── 需要运行后台任务（定时爬虫、数据处理）？
│   └── VPS（没有 Serverless 的执行时间限制）
│
└── 预算极有限，流量可能很大？
    └── Cloudflare Pages（免费且无限带宽）
```

---

## 上线前关键检查项

### SEO 检查

- [ ] 所有页面的 Title 和 Meta Description 已配置
- [ ] Sitemap.xml 已生成并可访问
- [ ] Robots.txt 已配置正确（不要误屏蔽重要页面）
- [ ] Canonical URL 已设置
- [ ] Open Graph 和 Twitter Card 标签已添加
- [ ] 结构化数据（Schema Markup）已添加

### 性能检查

- [ ] Google PageSpeed Insights 评分 > 90
- [ ] 首字节时间（TTFB）< 200ms
- [ ] 图片已压缩并使用 WebP/AVIF 格式
- [ ] CSS/JS 已压缩
- [ ] 启用了 Gzip/Brotli 压缩
- [ ] 关键资源已设置预加载

### 安全检查

- [ ] HTTPS 已启用且强制跳转
- [ ] 安全头已配置（CSP、X-Frame-Options 等）
- [ ] 敏感环境变量未暴露在前端代码中
- [ ] API 路由已添加速率限制

### 监控配置

- [ ] Google Search Console 已验证并提交 Sitemap
- [ ] Google Analytics 4 已安装
- [ ] 错误监控已配置（如 Sentry）
- [ ] 已设置 Uptime 监控（UptimeRobot 免费版即可）

---

## 成本优化建议

### 起步阶段（月收入 < $500）

```
推荐配置：
Cloudflare Pages（免费）或 Vercel Hobby（免费）
+ Cloudflare DNS（免费）
+ Let's Encrypt SSL（免费）
─────────────────
总成本：$0/月
```

### 成长阶段（月收入 $500-5000）

```
推荐配置：
Vercel Pro（$20/月）
+ Cloudflare DNS + CDN（免费）
+ 外部数据库服务（$0-25/月）
─────────────────
总成本：$20-45/月
```

### 规模化阶段（月收入 > $5000）

```
推荐配置：
VPS（$20-50/月）+ Cloudflare Pro（$20/月）
或 Vercel Pro + 更高配置的数据库
+ 监控和日志服务
─────────────────
总成本：$50-100/月
```
