import { Footer, Layout, Navbar } from 'nextra-theme-docs'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import type { Metadata } from 'next'
import type { ReactNode } from 'react'
import 'nextra-theme-docs/style.css'
import './global.css'

export const metadata: Metadata = {
  title: {
    default: 'SEO 出海教程',
    template: '%s | SEO 出海教程'
  },
  description: '从零到一，系统掌握出海 SEO 全链路实战技能',
  keywords: 'SEO, 出海, Google SEO, 海外流量, 独立站, SaaS, 关键词研究, 内容策略',
  authors: [{ name: 'SeoGO' }],
  openGraph: {
    title: 'SEO 出海教程',
    description: '从零到一，系统掌握出海 SEO 全链路实战技能',
    type: 'website',
    locale: 'zh_CN'
  }
}

export default async function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN" dir="ltr" suppressHydrationWarning>
      <Head
        color={{
          hue: 239,
          saturation: 84
        }}
      />
      <body>
        <Layout
          navbar={
            <Navbar
              logo={<span style={{ fontWeight: 800, fontSize: '1.1rem' }}>SEO 出海教程</span>}
              projectLink="https://github.com/tjsdyy/SeoGO"
            />
          }
          footer={
            <Footer>
              <p>CC BY-SA {new Date().getFullYear()} SeoGO</p>
            </Footer>
          }
          editLink={null}
          feedback={{ content: null }}
          sidebar={{ defaultMenuCollapseLevel: 1 }}
          toc={{ title: '本页目录' }}
          pageMap={await getPageMap()}
        >
          {children}
        </Layout>
      </body>
    </html>
  )
}
