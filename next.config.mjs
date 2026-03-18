import nextra from 'nextra'

const withNextra = nextra({
  contentDirBasePath: '/'
})

export default withNextra({
  async redirects() {
    return [
      // Legacy overview.html redirects
      {
        source: '/content/:folder/overview.html',
        destination: '/:folder',
        permanent: true
      },
      {
        source: '/content/:folder/overview',
        destination: '/:folder',
        permanent: true
      },
      {
        source: '/content/:path*.html',
        destination: '/:path*',
        permanent: true
      },
      {
        source: '/content/:path*',
        destination: '/:path*',
        permanent: true
      },
      // Old chapter redirects -> new chapter structure
      {
        source: '/1-preparation',
        destination: '/quick-start',
        permanent: true
      },
      {
        source: '/1-preparation/:path*',
        destination: '/quick-start',
        permanent: true
      },
      {
        source: '/2-fundamentals',
        destination: '/quick-start',
        permanent: true
      },
      {
        source: '/2-fundamentals/:path*',
        destination: '/quick-start',
        permanent: true
      },
      {
        source: '/3-product-positioning',
        destination: '/1-product-selection',
        permanent: true
      },
      {
        source: '/3-product-positioning/:path*',
        destination: '/1-product-selection',
        permanent: true
      },
      {
        source: '/4-keywords-trends',
        destination: '/2-demand-sources',
        permanent: true
      },
      {
        source: '/4-keywords-trends/:path*',
        destination: '/2-demand-sources',
        permanent: true
      },
      {
        source: '/5-site-building',
        destination: '/6-development-launch',
        permanent: true
      },
      {
        source: '/5-site-building/:path*',
        destination: '/6-development-launch',
        permanent: true
      },
      {
        source: '/6-content-strategy',
        destination: '/7-operations',
        permanent: true
      },
      {
        source: '/6-content-strategy/:path*',
        destination: '/7-operations',
        permanent: true
      },
      {
        source: '/7-traffic-acquisition',
        destination: '/7-operations/traffic',
        permanent: true
      },
      {
        source: '/7-traffic-acquisition/:path*',
        destination: '/7-operations/traffic',
        permanent: true
      },
      {
        source: '/8-data-optimization',
        destination: '/7-operations/page-optimization',
        permanent: true
      },
      {
        source: '/8-data-optimization/:path*',
        destination: '/7-operations/page-optimization',
        permanent: true
      },
      {
        source: '/9-risk-compliance',
        destination: '/7-operations',
        permanent: true
      },
      {
        source: '/9-risk-compliance/:path*',
        destination: '/7-operations',
        permanent: true
      }
    ]
  }
})
