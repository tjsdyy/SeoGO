---
title: 登录系统
---

# 登录系统

> 用户登录是 SEO 工具站和 SaaS 产品的基础能力。一个好的登录系统需要兼顾用户体验（降低注册摩擦）和安全性。本节以 Next.js + NextAuth.js（Auth.js）为技术栈，详解 Google OAuth 登录、邮箱登录的完整实现，以及用户数据库设计和安全最佳实践。

---

## Google OAuth 2.0 登录

Google 登录是海外产品最主流的第三方登录方式。用户点击"Sign in with Google"按钮，授权后即可自动创建账户并登录，极大降低注册摩擦。

### 第一步：Google Cloud Console 配置

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)，创建一个新项目（或使用已有项目）
2. 进入 **APIs & Services > OAuth consent screen**
3. 选择 **External** 用户类型（面向所有 Google 用户）
4. 填写应用信息：
   - **App name**：你的产品名称
   - **User support email**：你的邮箱
   - **App logo**：产品 Logo（可选，但建议上传以增加信任感）
   - **Authorized domains**：你的域名（如 `yourdomain.com`）
   - **Developer contact email**：开发者邮箱
5. 添加 Scopes（权限范围）：
   - `openid`（必须）
   - `email`（获取用户邮箱）
   - `profile`（获取用户名和头像）
6. 保存并返回

### 第二步：创建 OAuth 2.0 凭据

1. 进入 **APIs & Services > Credentials**
2. 点击 **Create Credentials > OAuth client ID**
3. 选择 **Web application** 类型
4. 填写：
   - **Name**：如 `My App Web Client`
   - **Authorized JavaScript origins**：`http://localhost:3000`（开发环境）和 `https://yourdomain.com`（生产环境）
   - **Authorized redirect URIs**：`http://localhost:3000/api/auth/callback/google` 和 `https://yourdomain.com/api/auth/callback/google`
5. 创建后获得 **Client ID** 和 **Client Secret**，保存到环境变量中

### 第三步：OAuth 2.0 登录流程说明

```
用户点击 "Sign in with Google"
       |
       v
浏览器跳转到 Google 授权页面
       |
       v
用户确认授权（选择 Google 账号）
       |
       v
Google 回调你的 redirect URI，携带 authorization code
       |
       v
你的服务器用 code 换取 access_token 和 id_token
       |
       v
解析 id_token 获取用户信息（email, name, picture）
       |
       v
查询数据库：用户是否已存在？
  - 已存在 → 直接登录，更新 session
  - 不存在 → 创建新用户，然后登录
       |
       v
设置 session cookie，跳转到应用主页
```

### 第四步：NextAuth.js 实现

```bash
npm install next-auth@beta
```

```typescript
// auth.ts（项目根目录）
import NextAuth from 'next-auth';
import Google from 'next-auth/providers/google';

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],

  // 使用 JWT 模式（推荐，更简单，无需数据库 Session 表）
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 天
  },

  callbacks: {
    // 将用户信息写入 JWT token
    async jwt({ token, user, account }) {
      if (user) {
        token.userId = user.id;
      }
      return token;
    },

    // 将 JWT 信息传递给前端 session
    async session({ session, token }) {
      if (token.userId) {
        session.user.id = token.userId as string;
      }
      return session;
    },

    // 登录成功后的回调（可用于首次注册逻辑）
    async signIn({ user, account, profile }) {
      // 在此处可将用户信息写入 Supabase
      // 例如：检查用户是否存在，不存在则创建
      return true;
    },
  },

  pages: {
    signIn: '/login',  // 自定义登录页面路径
    error: '/login',   // 错误时跳转到登录页
  },
});
```

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth';

export const { GET, POST } = handlers;
```

```typescript
// components/LoginButton.tsx
'use client';

import { signIn, signOut, useSession } from 'next-auth/react';

export function LoginButton() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <div className="h-10 w-24 animate-pulse rounded-lg bg-gray-200" />;
  }

  if (session?.user) {
    return (
      <div className="flex items-center gap-3">
        <img
          src={session.user.image || '/default-avatar.png'}
          alt="Avatar"
          className="h-8 w-8 rounded-full"
        />
        <span className="text-sm text-gray-700">{session.user.name}</span>
        <button
          onClick={() => signOut()}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          退出
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={() => signIn('google')}
      className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 transition-colors"
    >
      <svg className="h-5 w-5" viewBox="0 0 24 24">
        <path
          d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
          fill="#4285F4"
        />
        <path
          d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          fill="#34A853"
        />
        <path
          d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
          fill="#FBBC05"
        />
        <path
          d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
          fill="#EA4335"
        />
      </svg>
      Sign in with Google
    </button>
  );
}
```

```typescript
// app/layout.tsx 中包裹 SessionProvider
import { SessionProvider } from 'next-auth/react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  );
}
```

---

## 邮箱登录

对于不想使用第三方登录的用户，邮箱登录是必要的补充。推荐使用 Magic Link（魔法链接）方式，用户无需记忆密码，体验更好。

### Magic Link vs 密码登录对比

| 维度 | Magic Link | 密码登录 |
|------|-----------|----------|
| **用户体验** | 无需记忆密码，输入邮箱即可 | 需要设置和记忆密码 |
| **安全性** | 高（链接一次性、有时效） | 取决于密码强度 |
| **实现复杂度** | 需要邮件发送服务 | 需要密码加密存储 |
| **注册摩擦** | 极低 | 中等 |
| **适用场景** | SaaS、工具站、内容站 | 需要频繁登录的应用 |

**推荐**：优先实现 Magic Link，大多数 SEO 工具站和 SaaS 产品的用户使用频率不高，Magic Link 足够满足需求。

### 使用 Resend 发送 Magic Link 邮件

[Resend](https://resend.com) 是一个开发者友好的邮件发送服务，API 简洁、送达率高，免费版每月可发送 3000 封邮件。

```bash
npm install resend
```

### NextAuth.js 邮箱登录实现

```typescript
// auth.ts（在前面 Google 登录的基础上扩展）
import NextAuth from 'next-auth';
import Google from 'next-auth/providers/google';
import Resend from 'next-auth/providers/resend';

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),

    // 邮箱 Magic Link 登录
    Resend({
      apiKey: process.env.RESEND_API_KEY!,
      from: 'noreply@yourdomain.com', // 需要在 Resend 验证域名
    }),
  ],

  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60,
  },

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.userId = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (token.userId) {
        session.user.id = token.userId as string;
      }
      return session;
    },
  },

  pages: {
    signIn: '/login',
    verifyRequest: '/login/check-email', // Magic Link 发送后跳转页面
  },
});
```

### 登录页面完整实现

```typescript
// app/login/page.tsx
'use client';

import { signIn } from 'next-auth/react';
import { useState } from 'react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [emailSent, setEmailSent] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleEmailLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    try {
      await signIn('resend', {
        email,
        callbackUrl: '/dashboard',
        redirect: false,
      });
      setEmailSent(true);
    } catch (error) {
      console.error('Email login error:', error);
    } finally {
      setLoading(false);
    }
  }

  if (emailSent) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
            <span className="text-2xl">&#9993;</span>
          </div>
          <h2 className="text-xl font-bold text-gray-900">Check your email</h2>
          <p className="mt-2 text-sm text-gray-600">
            We sent a login link to <strong>{email}</strong>.
            Click the link in the email to sign in.
          </p>
          <button
            onClick={() => setEmailSent(false)}
            className="mt-6 text-sm text-blue-600 hover:text-blue-500"
          >
            Use a different email
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">
        <h1 className="text-2xl font-bold text-gray-900 text-center">
          Sign in to YourApp
        </h1>
        <p className="mt-2 text-sm text-gray-600 text-center">
          Start your SEO journey today
        </p>

        {/* Google 登录按钮 */}
        <button
          onClick={() => signIn('google', { callbackUrl: '/dashboard' })}
          className="mt-8 flex w-full items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 transition-colors"
        >
          <svg className="h-5 w-5" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          Continue with Google
        </button>

        {/* 分隔线 */}
        <div className="relative mt-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-200" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="bg-white px-4 text-gray-500">or</span>
          </div>
        </div>

        {/* 邮箱 Magic Link 登录 */}
        <form onSubmit={handleEmailLogin} className="mt-6">
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email address
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
            className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading || !email}
            className="mt-4 w-full rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 disabled:opacity-50 transition-colors"
          >
            {loading ? 'Sending...' : 'Send Magic Link'}
          </button>
        </form>

        <p className="mt-6 text-center text-xs text-gray-500">
          By signing in, you agree to our{' '}
          <a href="/terms" className="text-blue-600 hover:text-blue-500">Terms of Service</a>
          {' '}and{' '}
          <a href="/privacy" className="text-blue-600 hover:text-blue-500">Privacy Policy</a>.
        </p>
      </div>
    </div>
  );
}
```

---

## 用户数据库设计

### Supabase 用户表结构

以下是一个适用于 SEO 工具站 / SaaS 产品的用户数据库设计，基于 Supabase（PostgreSQL）。

```sql
-- 用户基础信息表
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  avatar_url TEXT,
  provider TEXT DEFAULT 'email',       -- google, email, github
  provider_account_id TEXT,            -- 第三方登录的用户 ID
  plan TEXT DEFAULT 'free',            -- free, pro, enterprise
  credits_remaining INTEGER DEFAULT 5, -- 每日免费额度（剩余）
  credits_reset_at TIMESTAMPTZ,        -- 额度重置时间
  stripe_customer_id TEXT,             -- 关联 Stripe 客户
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  last_login_at TIMESTAMPTZ
);

-- 用户使用记录表（用于追踪 API 调用和功能使用）
CREATE TABLE usage_logs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  action TEXT NOT NULL,        -- 'seo_audit', 'keyword_research', 'content_generate'
  credits_used INTEGER DEFAULT 1,
  metadata JSONB,              -- 额外信息，如输入参数、结果摘要
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 会话表（如果使用数据库 Session 而非 JWT）
CREATE TABLE sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  session_token TEXT UNIQUE NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_stripe ON users(stripe_customer_id);
CREATE INDEX idx_usage_logs_user ON usage_logs(user_id);
CREATE INDEX idx_usage_logs_date ON usage_logs(created_at);
CREATE INDEX idx_sessions_token ON sessions(session_token);
```

### 每日免费额度模型

大多数 SEO 工具站采用"每日免费额度 + 付费无限制"的模式来转化用户。以下是额度管理的核心实现：

```typescript
// lib/credits.ts
import { supabaseAdmin } from '@/lib/supabase';

const FREE_DAILY_CREDITS = 5;
const PRO_DAILY_CREDITS = 100;

export async function checkAndDeductCredit(userId: string): Promise<{
  allowed: boolean;
  remaining: number;
  plan: string;
}> {
  // 获取用户信息
  const { data: user } = await supabaseAdmin
    .from('users')
    .select('plan, credits_remaining, credits_reset_at')
    .eq('id', userId)
    .single();

  if (!user) {
    return { allowed: false, remaining: 0, plan: 'free' };
  }

  // 付费用户的额度上限更高
  const maxCredits = user.plan === 'free' ? FREE_DAILY_CREDITS : PRO_DAILY_CREDITS;

  // 检查是否需要重置每日额度
  const now = new Date();
  const resetAt = user.credits_reset_at ? new Date(user.credits_reset_at) : null;

  if (!resetAt || now > resetAt) {
    // 重置额度：次日 UTC 0 点重置
    const nextReset = new Date();
    nextReset.setUTCHours(24, 0, 0, 0);

    await supabaseAdmin
      .from('users')
      .update({
        credits_remaining: maxCredits - 1, // 重置后立即扣除本次使用
        credits_reset_at: nextReset.toISOString(),
      })
      .eq('id', userId);

    return { allowed: true, remaining: maxCredits - 1, plan: user.plan };
  }

  // 检查剩余额度
  if (user.credits_remaining <= 0) {
    return { allowed: false, remaining: 0, plan: user.plan };
  }

  // 扣除额度
  await supabaseAdmin
    .from('users')
    .update({
      credits_remaining: user.credits_remaining - 1,
    })
    .eq('id', userId);

  return {
    allowed: true,
    remaining: user.credits_remaining - 1,
    plan: user.plan,
  };
}
```

```typescript
// 在 API 路由中使用额度检查
// app/api/tools/seo-audit/route.ts
import { auth } from '@/auth';
import { checkAndDeductCredit } from '@/lib/credits';
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // 检查并扣除额度
  const creditResult = await checkAndDeductCredit(session.user.id);

  if (!creditResult.allowed) {
    return NextResponse.json(
      {
        error: 'Daily credit limit reached',
        remaining: 0,
        plan: creditResult.plan,
        upgradeUrl: '/pricing',
      },
      { status: 429 }
    );
  }

  // 执行实际业务逻辑...
  const result = await performSeoAudit(request);

  return NextResponse.json({
    ...result,
    credits_remaining: creditResult.remaining,
  });
}
```

### Session 管理：JWT vs 数据库 Session

| 维度 | JWT（推荐） | 数据库 Session |
|------|------------|----------------|
| **性能** | 无需查询数据库，速度快 | 每次请求需查询数据库 |
| **扩展性** | 无状态，天然支持多实例部署 | 需要共享数据库存储 |
| **安全性** | Token 泄露后无法主动失效 | 可随时删除 Session 使其失效 |
| **存储** | 客户端 Cookie 中 | 服务端数据库中 |
| **适用场景** | 大多数 SaaS / 工具站 | 需要严格 Session 控制的场景 |

**推荐使用 JWT 模式**。对于大多数 SEO 工具站和 SaaS 产品，JWT 的无状态特性带来的性能优势更重要。NextAuth.js 默认即支持 JWT 模式。

---

## 安全最佳实践

### CSRF 保护

CSRF（Cross-Site Request Forgery，跨站请求伪造）是 Web 应用最常见的安全威胁之一。NextAuth.js 内置了 CSRF 保护机制，但你仍需在自定义路由中注意防护。

```typescript
// middleware.ts
import { auth } from '@/auth';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  // 保护需要登录的 API 路由
  if (request.nextUrl.pathname.startsWith('/api/tools')) {
    const session = await auth();

    if (!session) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }
  }

  // 保护需要登录的页面
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    const session = await auth();

    if (!session) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/api/tools/:path*', '/dashboard/:path*'],
};
```

### Rate Limiting（速率限制）

防止恶意用户暴力破解登录或滥用 API 接口。推荐使用 Upstash Redis 实现分布式速率限制：

```bash
npm install @upstash/ratelimit @upstash/redis
```

```typescript
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL!,
  token: process.env.UPSTASH_REDIS_TOKEN!,
});

// 登录接口限流：每分钟最多 5 次
export const loginRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, '1 m'),
  analytics: true,
  prefix: 'ratelimit:login',
});

// API 接口限流：每分钟最多 30 次
export const apiRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(30, '1 m'),
  analytics: true,
  prefix: 'ratelimit:api',
});
```

```typescript
// 在 API 路由中使用速率限制
// app/api/auth/login/route.ts
import { loginRateLimit } from '@/lib/rate-limit';
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  // 使用 IP 地址作为限流标识
  const ip = request.headers.get('x-forwarded-for') || 'anonymous';
  const { success, remaining, reset } = await loginRateLimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      {
        error: 'Too many login attempts. Please try again later.',
        retryAfter: Math.ceil((reset - Date.now()) / 1000),
      },
      {
        status: 429,
        headers: {
          'X-RateLimit-Remaining': remaining.toString(),
          'Retry-After': Math.ceil((reset - Date.now()) / 1000).toString(),
        },
      }
    );
  }

  // 正常处理登录逻辑...
}
```

### Secure Session Cookies

确保 Session Cookie 的安全配置：

```typescript
// auth.ts 中配置 cookie 安全选项
export const { handlers, signIn, signOut, auth } = NextAuth({
  // ...providers 配置

  cookies: {
    sessionToken: {
      name: '__Secure-authjs.session-token',
      options: {
        httpOnly: true,    // 防止 JavaScript 访问 Cookie（防 XSS）
        sameSite: 'lax',   // 防止 CSRF 攻击
        path: '/',
        secure: process.env.NODE_ENV === 'production', // 生产环境强制 HTTPS
        maxAge: 30 * 24 * 60 * 60, // 30 天
      },
    },
  },

  // 其他安全配置
  trustHost: true,
  secret: process.env.NEXTAUTH_SECRET, // 用于加密 JWT 和 Cookie
});
```

### 安全配置清单

- [ ] 所有密钥（`GOOGLE_CLIENT_SECRET`、`NEXTAUTH_SECRET` 等）存储在环境变量中
- [ ] `NEXTAUTH_SECRET` 使用 `openssl rand -base64 32` 生成的强随机字符串
- [ ] Session Cookie 设置了 `httpOnly`、`secure`、`sameSite` 属性
- [ ] 登录接口实施了速率限制（防暴力破解）
- [ ] API 接口实施了速率限制（防滥用）
- [ ] 所有需要认证的路由通过 middleware 统一保护
- [ ] Google OAuth redirect URI 仅包含你的域名（不含通配符）
- [ ] 生产环境强制使用 HTTPS
- [ ] 定期审查 Google Cloud Console 中的 OAuth 应用权限

---

## 环境变量汇总

```bash
# .env.local

# NextAuth.js
NEXTAUTH_SECRET=your-random-secret-here  # openssl rand -base64 32
NEXTAUTH_URL=http://localhost:3000        # 生产环境改为你的域名

# Google OAuth
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxx

# Resend (Magic Link 邮件)
RESEND_API_KEY=re_xxx

# Supabase (数据库)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_ROLE_KEY=xxx

# Upstash Redis (速率限制)
UPSTASH_REDIS_URL=https://xxx.upstash.io
UPSTASH_REDIS_TOKEN=xxx
```

---

## 常见问题

**Q：Google OAuth 还是邮箱登录优先实现？**
A：优先实现 Google OAuth。海外用户几乎人人有 Google 账号，一键登录的转化率远高于邮箱登录。邮箱 Magic Link 作为补充，供不想使用第三方登录的用户使用。

**Q：NextAuth.js v4 还是 v5（Auth.js）？**
A：推荐使用 v5（`next-auth@beta`，也叫 Auth.js）。v5 原生支持 App Router、React Server Components，与现代 Next.js 项目更契合。本文代码均基于 v5。

**Q：需要自己搭建邮件服务吗？**
A：不需要。使用 Resend 即可，免费版每月 3000 封邮件对于起步阶段绰绰有余。只需在 Resend 后台验证你的域名，配置 DNS 记录即可开始发送。

**Q：用户量大了之后 JWT 模式还够用吗？**
A：对于绝大多数 SEO 工具站（日活 < 10 万），JWT 模式完全够用。如果未来需要即时吊销 Session 的能力（如检测到账户异常需要强制登出），可以在 JWT 基础上增加一层 Redis 黑名单检查。

**Q：如何实现"每日免费 5 次"的额度模型？**
A：参见本文"每日免费额度模型"部分的代码实现。核心逻辑是在 `users` 表中维护 `credits_remaining` 和 `credits_reset_at` 字段，每次 API 调用时检查并扣减额度，UTC 0 点自动重置。
