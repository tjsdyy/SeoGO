---
title: 支付接口集成
---

# 支付接口集成

> 当你的 SEO 站点需要变现时，集成支付接口是关键一步。无论是 SaaS 订阅、一次性付费工具还是付费内容，都需要一个可靠的支付通道。本节详解 Stripe、PayPal 和 Creem 三种支付方案的技术集成细节，并涵盖银行卡准备和收款账户配置等实操环节。

---

## 银行卡与收款账户准备

在集成支付接口之前，你首先需要解决"钱往哪里收"的问题。海外支付平台要求绑定境外银行账户，国内银联卡在大多数平台上无法使用。

### 方案一：香港银行卡（推荐）

香港银行卡支持 Visa/Mastercard 网络，可绑定 Stripe、PayPal 等所有主流支付平台，资金进出无外汇管制。

| 银行 | 开户门槛 | 管理费 | 优势 | 劣势 |
|------|----------|--------|------|------|
| 汇丰银行 (HSBC) | 较高，建议存入 50 万港币 | 月均余额低于 20 万收 HK$120/月 | 品牌强、ATM 多、网银好用 | 门槛高、排队时间长 |
| 中银香港 (BOCHK) | 中等，内地中行客户可见证开户 | 月均余额低于 1 万收 HK$60/月 | 内地关联方便、门槛适中 | 网银体验一般 |
| ZA Bank (众安银行) | 低，线上开户 | 免管理费 | 纯线上、门槛低、免管理费 | 虚拟银行、部分平台不认 |

**港卡开户流程（以中银香港为例）：**

1. **准备材料**：内地身份证原件、港澳通行证或护照、三个月内地址证明、入境小白条
2. **预约方式**：内地中行见证开户（无需赴港）或香港网点预约
3. **开户当日**：携带原件到场，填写申请表，说明开户目的为个人理财/跨境消费
4. **开户后设置**：下载中银香港 App，开通 FPS 转数快，设置交易通知

> **提示**：开户时一并申请港币和美元账户。很多海外服务以美元计价，有美元账户可以减少货币转换费用。

### 方案二：Wise 多币种账户

Wise 是一家总部位于伦敦的金融科技公司，提供多币种账户和低成本跨境转账服务。对于暂时无法开设港卡的人来说，Wise 是最佳替代方案。

- **多币种账户**：支持 50+ 种货币，可同时持有美元、欧元、英镑等余额
- **真实银行账户信息**：获得美国、英国、欧洲等地的本地银行账号
- **低汇率转换费**：使用中间市场汇率，费率通常在 0.3%-1% 之间
- **Wise 借记卡**：实体卡和虚拟卡均可申请，可在全球消费

**注册流程**：访问 wise.com 注册 → 身份验证（建议用护照） → 地址验证 → 入金激活 → 申请借记卡（可选）。

### 方案三：OCBC 华侨银行（新加坡）

新加坡华侨银行（OCBC）支持中国大陆居民纯线上开户，无需出境。

- **开户条件**：年满 18 周岁、中国护照、有效手机号和邮箱
- **操作步骤**：下载 OCBC Digital App → 扫描护照 → 人脸识别 → 填写信息 → 等待审核（3-5 个工作日）→ 首次入金激活
- **优势**：纯线上操作、支持多币种、新加坡金融监管严格安全性高

> **建议**：如果条件允许，香港银行卡和 Wise 两者都开。港卡用于绑定 Stripe 收款和大额转账，Wise 用于多币种收付和跨境转账。

---

## 三种支付方案对比

| 维度 | Stripe | PayPal | Creem |
|------|--------|--------|-------|
| **最适合** | 独立站在线收款 | 小额/个人交易、用户偏好覆盖 | 快速集成、数字产品 |
| **标准费率** | 2.9% + $0.30 | 3.49% + $0.49 | 按方案定价 |
| **国际交易附加** | +1% | +1.5% | 已含 |
| **注册难度** | 高（需境外公司） | 低（个人可注册） | 中等 |
| **技术门槛** | 中等（API 强大） | 低（可无代码集成） | 低 |
| **支持币种** | 135+ | 25 | 多币种支持 |
| **订阅支持** | 原生 Billing 系统 | 基础支持 | 内置订阅管理 |
| **Webhook** | 完善，事件类型丰富 | 基础（IPN） | 支持 |
| **资金安全** | 高 | 中（新账户冻结风险） | 中 |
| **到账速度** | 2-7 天到银行账户 | 即时到 PayPal 余额 | 按周期结算 |
| **税务处理** | 需自行处理 | 需自行处理 | 自动处理全球销售税 |
| **文档质量** | 极好 | 一般 | 较好 |

---

## Stripe 集成（推荐）

### 为什么选择 Stripe

Stripe 是全球开发者首选的支付平台，被 Shopify、Amazon、Google 等巨头采用。它的 API 设计优雅、文档完善、功能强大，是做海外独立站收款的首选方案。

### 注册 Stripe 账户

Stripe 不直接支持中国大陆企业注册。你需要通过以下方式之一获取 Stripe 账户：

| 方式 | 费用 | 难度 | 推荐度 |
|------|------|------|--------|
| 香港公司 + 港卡 | ~$500-1000 注册费 | 中 | 强烈推荐 |
| 美国 LLC（Firstbase / Stripe Atlas） | ~$500 | 中 | 推荐 |
| LemonSqueezy / Paddle 代收 | 费率略高（~5%） | 低 | 起步可用 |

**验证流程**：注册后需完成公司信息验证 → 提交银行账户信息 → 验证法人身份（护照/身份证扫描）→ 上传公司注册文件 → 等待审核通过。

### Stripe Checkout 集成（最常用方案）

Stripe Checkout 提供托管的支付页面，无需自建支付表单，安全且合规。

#### 第一步：安装 Stripe SDK

```bash
npm install stripe @stripe/stripe-js
```

#### 第二步：创建后端 API 路由

```typescript
// app/api/checkout/route.ts
import Stripe from 'stripe';
import { NextResponse } from 'next/server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});

export async function POST(request: Request) {
  const { priceId, mode = 'subscription' } = await request.json();

  try {
    const session = await stripe.checkout.sessions.create({
      // 支付模式：subscription（订阅）或 payment（一次性）
      mode: mode as 'subscription' | 'payment',

      // 商品信息
      line_items: [
        {
          price: priceId, // 在 Stripe Dashboard 创建的价格 ID
          quantity: 1,
        },
      ],

      // 成功和取消回调 URL
      success_url: `${process.env.NEXT_PUBLIC_APP_URL}/payment/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,

      // 自动收集客户邮箱
      customer_email: undefined, // 或传入已知用户邮箱
      allow_promotion_codes: true, // 允许促销码

      // 订阅免费试用（可选）
      ...(mode === 'subscription' && {
        subscription_data: {
          trial_period_days: 7, // 7 天免费试用
        },
      }),

      // 自定义元数据
      metadata: {
        source: 'website',
      },
    });

    return NextResponse.json({ url: session.url });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

#### 第三步：前端调用

```typescript
// components/PricingButton.tsx
'use client';

import { useState } from 'react';

interface PricingButtonProps {
  priceId: string;
  label: string;
  mode?: 'subscription' | 'payment';
}

export function PricingButton({ priceId, label, mode = 'subscription' }: PricingButtonProps) {
  const [loading, setLoading] = useState(false);

  async function handleClick() {
    setLoading(true);

    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId, mode }),
      });

      const { url, error } = await response.json();

      if (error) {
        alert(`支付出错: ${error}`);
        return;
      }

      // 跳转到 Stripe Checkout 页面
      window.location.href = url;
    } catch (err) {
      alert('网络错误，请重试');
    } finally {
      setLoading(false);
    }
  }

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className="rounded-lg bg-blue-600 px-6 py-3 text-white font-semibold hover:bg-blue-500 disabled:opacity-50 transition-colors"
    >
      {loading ? '处理中...' : label}
    </button>
  );
}
```

### Webhook 处理支付事件

Webhook 是 Stripe 向你的服务器推送支付状态变更的机制。这是支付集成中**最关键**的部分，决定了用户付款后能否正确开通服务。

```typescript
// app/api/webhooks/stripe/route.ts
import Stripe from 'stripe';
import { NextResponse } from 'next/server';
import { headers } from 'next/headers';
import { supabaseAdmin } from '@/lib/supabase';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export async function POST(request: Request) {
  const body = await request.text();
  const headersList = await headers();
  const signature = headersList.get('stripe-signature')!;

  let event: Stripe.Event;

  // 验证 Webhook 签名（安全必须，防止伪造请求）
  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err: any) {
    console.error('Webhook signature verification failed:', err.message);
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  // 处理不同类型的事件
  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;

      // 支付成功 → 更新用户订阅状态
      await supabaseAdmin
        .from('subscriptions')
        .upsert({
          user_email: session.customer_email,
          stripe_customer_id: session.customer as string,
          stripe_subscription_id: session.subscription as string,
          status: 'active',
          plan: session.metadata?.plan || 'pro',
          current_period_end: new Date(
            (session as any).current_period_end * 1000
          ).toISOString(),
        });

      console.log('New subscription:', session.customer_email);
      break;
    }

    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription;

      // 订阅变更（升级/降级/续费）
      await supabaseAdmin
        .from('subscriptions')
        .update({
          status: subscription.status,
          current_period_end: new Date(
            subscription.current_period_end * 1000
          ).toISOString(),
        })
        .eq('stripe_subscription_id', subscription.id);

      break;
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription;

      // 订阅取消
      await supabaseAdmin
        .from('subscriptions')
        .update({ status: 'canceled' })
        .eq('stripe_subscription_id', subscription.id);

      break;
    }

    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice;
      console.log('Payment failed for:', invoice.customer_email);
      // TODO: 发送通知邮件提醒用户更新支付方式
      break;
    }
  }

  return NextResponse.json({ received: true });
}
```

### 配置 Webhook 端点

```bash
# 本地开发：使用 Stripe CLI 转发 Webhook 到本地
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# 生产环境：在 Stripe Dashboard 配置
# Developers > Webhooks > Add endpoint
# URL: https://yourdomain.com/api/webhooks/stripe
# 选择事件：
#   - checkout.session.completed
#   - customer.subscription.updated
#   - customer.subscription.deleted
#   - invoice.payment_failed
```

### 订阅管理

Stripe 原生支持完整的订阅生命周期管理。以下是常用的订阅操作：

```typescript
// lib/stripe-helpers.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

// 取消订阅（到期后不续费）
export async function cancelSubscription(subscriptionId: string) {
  return await stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true,
  });
}

// 立即取消订阅
export async function cancelSubscriptionImmediately(subscriptionId: string) {
  return await stripe.subscriptions.cancel(subscriptionId);
}

// 创建客户门户链接（让用户自助管理订阅）
export async function createPortalSession(customerId: string, returnUrl: string) {
  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: returnUrl,
  });
  return session.url;
}

// 查询订阅状态
export async function getSubscriptionStatus(subscriptionId: string) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  return {
    status: subscription.status,
    currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    cancelAtPeriodEnd: subscription.cancel_at_period_end,
  };
}
```

### 订阅数据库表设计

```sql
-- 订阅表
CREATE TABLE subscriptions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  user_email TEXT NOT NULL,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  status TEXT DEFAULT 'inactive',  -- active, canceled, past_due, trialing
  plan TEXT DEFAULT 'free',        -- free, pro, enterprise
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 支付记录表
CREATE TABLE payments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  stripe_payment_intent_id TEXT,
  amount INTEGER,          -- 金额（单位：分）
  currency TEXT DEFAULT 'usd',
  status TEXT,             -- succeeded, failed, pending
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_payments_user ON payments(user_id);
```

---

## PayPal 集成

### 适用场景

- 约 10-20% 的海外用户更偏好使用 PayPal
- 作为 Stripe 的备用支付方式，减少结账放弃率
- 不需要公司主体即可接入，个人商业账户即可使用

### 账户注册

1. 访问 PayPal 对应地区官网，选择"商业账户"注册
2. 填写商业信息（个人 freelancer 可选择个体经营）
3. 验证邮箱和手机号
4. 关联银行账户或银行卡（港卡/Wise 均可）
5. 完成身份验证

### PayPal Buttons 集成

```bash
# 安装 PayPal React SDK
npm install @paypal/react-paypal-js
```

```typescript
// app/pricing/paypal-section.tsx
'use client';

import { PayPalScriptProvider, PayPalButtons } from '@paypal/react-paypal-js';

export default function PayPalSection() {
  return (
    <PayPalScriptProvider
      options={{
        clientId: process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID!,
        currency: 'USD',
        vault: true, // 启用订阅支持
        intent: 'subscription',
      }}
    >
      <PayPalButtons
        style={{
          layout: 'vertical',
          color: 'gold',
          shape: 'rect',
          label: 'subscribe',
        }}
        createSubscription={(data, actions) => {
          return actions.subscription.create({
            plan_id: 'P-YOUR_PLAN_ID', // 在 PayPal 后台创建的计划 ID
          });
        }}
        onApprove={async (data) => {
          // 通知后端激活订阅
          await fetch('/api/webhooks/paypal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              subscriptionId: data.subscriptionID,
              orderId: data.orderID,
            }),
          });
          window.location.href = '/payment/success';
        }}
        onError={(err) => {
          console.error('PayPal error:', err);
        }}
      />
    </PayPalScriptProvider>
  );
}
```

### IPN（Instant Payment Notification）

PayPal 的 IPN 是其 Webhook 机制，用于接收支付状态变更通知。

```typescript
// app/api/webhooks/paypal/route.ts
import { NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase';

export async function POST(request: Request) {
  const body = await request.text();

  // 向 PayPal 验证 IPN 消息的真实性
  const verifyResponse = await fetch(
    'https://ipnpb.paypal.com/cgi-bin/webscr',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `cmd=_notify-validate&${body}`,
    }
  );

  const verification = await verifyResponse.text();

  if (verification !== 'VERIFIED') {
    console.error('PayPal IPN verification failed');
    return NextResponse.json({ error: 'Invalid IPN' }, { status: 400 });
  }

  // 解析 IPN 参数
  const params = new URLSearchParams(body);
  const txnType = params.get('txn_type');
  const payerEmail = params.get('payer_email');

  switch (txnType) {
    case 'subscr_payment':
      // 订阅付款成功
      await supabaseAdmin
        .from('subscriptions')
        .upsert({
          user_email: payerEmail,
          paypal_subscription_id: params.get('subscr_id'),
          status: 'active',
          plan: 'pro',
        });
      break;

    case 'subscr_cancel':
      // 订阅取消
      await supabaseAdmin
        .from('subscriptions')
        .update({ status: 'canceled' })
        .eq('paypal_subscription_id', params.get('subscr_id'));
      break;

    case 'subscr_failed':
      // 续费失败
      console.log('PayPal subscription payment failed:', payerEmail);
      break;
  }

  return NextResponse.json({ received: true });
}
```

### PayPal 注意事项

- **新账户风控**：前几个月大额收款可能被冻结 21 天，建议从小额交易开始积累信用
- **费率偏高**：跨境交易总费率可达 3.49% + $0.49 + 1.5% 附加费
- **争议处理偏向买家**：卖家需注意保留交易证据和服务交付记录
- **货币转换汇率差**：PayPal 自身的汇率加点约 3-4%，建议保持美元余额后提现

---

## Creem 支付平台

### 什么是 Creem

Creem 是一个面向数字产品和 SaaS 的新兴支付平台，定位为更简单的 Stripe 替代方案。它的核心卖点是帮开发者自动处理全球销售税/增值税合规问题，让你专注于产品本身。

### 核心特性

| 特性 | 说明 |
|------|------|
| **简化集成** | 比 Stripe 更少的代码即可完成集成 |
| **税务自动处理** | 自动计算和代缴全球 VAT/GST/Sales Tax |
| **支付链接** | 无需代码，生成支付链接即可收款 |
| **订阅管理** | 内置订阅、计费和客户门户 |
| **多币种** | 支持多种货币结算 |
| **分析面板** | 内置收入分析仪表盘和 MRR 统计 |

### 注册与设置

1. 访问 Creem 官网注册账户
2. 完成身份验证和公司信息填写
3. 在后台创建产品和定价方案
4. 获取 API Key 和产品 ID
5. 配置 Webhook 回调 URL

### Creem 集成方式

#### 方式一：支付链接（零代码）

最简单的方式，适合快速验证商业模式：

```html
<!-- 在定价页面直接使用支付链接 -->
<a href="https://checkout.creem.io/pay/your-product-id"
   class="bg-blue-600 text-white px-6 py-3 rounded-lg">
  Purchase Now - $29/month
</a>
```

#### 方式二：API 集成

```typescript
// lib/creem.ts
const CREEM_API_KEY = process.env.CREEM_API_KEY!;
const CREEM_BASE_URL = 'https://api.creem.io/v1';

// 创建支付会话
export async function createCreemCheckout(params: {
  productId: string;
  customerEmail: string;
  successUrl: string;
  cancelUrl: string;
}) {
  const response = await fetch(`${CREEM_BASE_URL}/checkout/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${CREEM_API_KEY}`,
    },
    body: JSON.stringify({
      product_id: params.productId,
      customer_email: params.customerEmail,
      success_url: params.successUrl,
      cancel_url: params.cancelUrl,
    }),
  });

  const data = await response.json();
  return data;
}
```

```typescript
// app/api/checkout/creem/route.ts
import { createCreemCheckout } from '@/lib/creem';
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { productId, email } = await request.json();

  try {
    const session = await createCreemCheckout({
      productId,
      customerEmail: email,
      successUrl: `${process.env.NEXT_PUBLIC_APP_URL}/payment/success`,
      cancelUrl: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    });

    return NextResponse.json({ url: session.checkout_url });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

### Creem 适用场景

- **不想自行处理税务合规**：Creem 自动处理全球各地的销售税，免去注册税号的麻烦
- **需要快速上线收款**：支付链接方式零代码即可接入
- **数字产品和 SaaS**：Creem 专门为此类产品设计
- **独立开发者**：一个人运营时，减少合规方面的精力投入

---

## 实操建议

### 推荐的集成策略

**第一步：以 Stripe 为主要支付方式。** Stripe 的支付成功率最高、API 最完善、文档最好。定价页面的主按钮应走 Stripe Checkout。

**第二步：加入 PayPal 作为覆盖补充。** 约 10-20% 的海外用户偏好 PayPal，在定价页面提供 PayPal 选项可以显著降低结账放弃率。

**第三步：根据具体情况考虑 Creem。** 如果你的产品面向全球用户，不想自行处理各国税务合规，或者你是独立开发者希望尽量简化流程，Creem 是一个值得考虑的选择。

### 分阶段落地

| 阶段 | 月收入 | 推荐操作 |
|------|--------|----------|
| 起步期 | < $1,000 | 先接入 Stripe（或 LemonSqueezy 如无公司主体），够用即可 |
| 成长期 | $1,000 - $10,000 | 加入 PayPal，优化定价页面，建立完善的 Webhook 处理 |
| 规模期 | > $10,000 | 谈判 Stripe 定制费率，考虑 Creem 处理税务，建立自动化对账 |

### 环境变量配置清单

```bash
# .env.local

# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx

# PayPal
NEXT_PUBLIC_PAYPAL_CLIENT_ID=xxx
PAYPAL_CLIENT_SECRET=xxx

# Creem
CREEM_API_KEY=creem_live_xxx

# App
NEXT_PUBLIC_APP_URL=https://yourdomain.com
```

---

## 支付安全清单

- [ ] 所有 API 密钥存储在环境变量中，未暴露到前端代码
- [ ] Webhook 端点已验证签名（Stripe 签名验证 / PayPal IPN 验证）
- [ ] 所有支付页面使用 HTTPS
- [ ] 开启 Stripe 的 Radar 欺诈防护
- [ ] 设置支付异常的监控告警（Stripe Dashboard 或自建通知）
- [ ] 退款和争议处理流程已建立
- [ ] 所有支付记录已写入数据库（便于对账和审计）
- [ ] 开启了所有平台的 2FA 双因素认证
- [ ] 隐私政策和服务条款页面已上线
- [ ] 价格页面显示了正确的币种和含税说明
- [ ] 资金分散在多个渠道，不依赖单一收款平台

---

## 常见问题

**Q：没有境外公司，怎么接入 Stripe？**
A：可以使用 LemonSqueezy 或 Paddle，它们作为商家（Merchant of Record）帮你处理支付合规，你作为供应商入驻。费率略高（约 5%），但无需注册公司。

**Q：Stripe 和 PayPal 应该都接入吗？**
A：推荐。提供多种支付方式可以减少结账放弃率。先把 Stripe 跑通，再加 PayPal 作为补充。

**Q：如何处理订阅续费失败？**
A：Stripe 内置 Smart Retries（智能重试），会在卡被拒后自动重试多次。同时建议监听 `invoice.payment_failed` 事件，通过邮件通知用户更新支付方式。

**Q：Creem 和 LemonSqueezy 有什么区别？**
A：两者都是 Merchant of Record 模式。LemonSqueezy 底层走 Stripe，历史更久生态更成熟；Creem 更新，集成更简洁，适合快速启动的数字产品。根据你的具体需求选择即可。

**Q：首次入金需要准备多少资金？**
A：建议准备 $500-1000 美元等值的资金，覆盖前几个月的域名、服务器、SEO 工具等基础开销。日常保持账户中至少有 3 个月工具订阅费用的余额。
