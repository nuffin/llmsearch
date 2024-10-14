import bundleAnalyzer from '@next/bundle-analyzer'
import { withSentryConfig } from '@sentry/nextjs'

const nextI18NextConfig = await import('./next-i18next.config.js').then(
  (m) => m.default
)

// @ts-check
/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation.
 * This is especially useful for Docker builds.
 */
!process.env.SKIP_ENV_VALIDATION && (await import('./src/env/server.mjs'))

/** @type {import("next").NextConfig} */
const config = {
  poweredByHeader: false,
  reactStrictMode: false,
  swcMinify: true,
  // i18n: nextI18NextConfig.i18n,
  eslint: {
    ignoreDuringBuilds: true,
  },
  output: 'export',
  experimental: {
    /**
     * This experimental is unstable, make sure keep `outputFileTracingIgnores` value sync to avoid problem with function size limit
     * @see https://github.com/vercel/next.js/issues/54245
     */
    outputFileTracingExcludes: {
      '*': ['node_modules/canvas', 'node_modules/.pnpm/canvas@2.11.2'],
    },
    webVitalsAttribution: ['CLS', 'LCP'],
    swcPlugins: [['next-superjson-plugin', {}]],
  },
  staticPageGenerationTimeout: 240,
  transpilePackages: ['@flowgpt'],
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 768, 1024, 1280, 1536, 1920, 2250], // sync to tailwind config
    imageSizes: [16, 32, 48, 64, 96, 256, 384],
    remotePatterns: [
      { protocol: 'https', hostname: 'image-cdn.flowgpt.com' },
      {
        protocol: 'https',
        hostname: 'flow-user-images.s3.us-west-1.amazonaws.com',
      },
      {
        protocol: 'https',
        hostname: 'flow-prompt-covers.s3.us-west-1.amazonaws.com',
      },
      {
        protocol: 'https',
        hostname: 'flow-public-assets.s3.us-west-1.amazonaws.com',
      },
      {
        protocol: 'https',
        hostname: 'flow-chat-images.s3.us-west-1.amazonaws.com',
      },
      { protocol: 'https', hostname: 'lh3.googleusercontent.com' },
      { protocol: 'https', hostname: 'media.licdn.com' },
      { protocol: 'https', hostname: 'wallpapers-clan.com' },
      { protocol: 'https', hostname: 'cdn.discordapp.com' },
      { protocol: 'https', hostname: 'abs.twimg.com' },
      { protocol: 'https', hostname: 'pbs.twimg.com' },
      { protocol: 'https', hostname: 'i.pinimg.com' },
      { protocol: 'https', hostname: 'pbs.twimg.com' },
      { protocol: 'https', hostname: 'i.ibb.co' },
      { protocol: 'https', hostname: 'pbs.twimg.com' },
    ],
    minimumCacheTTL: 432000,
  },
  // async headers() {
  //   return []
  // },
  // async rewrites() {
  //   return [
  //   ]
  // },
}

const plugins = [
  bundleAnalyzer({
    enabled: process.env.ANALYZE === 'true',
  }),
]

/** @type {import('next').NextConfig} */
const nextConfig = () => {
  let result = config

  if (process.env.NEXT_PUBLIC_VERCEL_ENV) {
    result = withSentryConfig(
      config,
      {
        // For all available options, see:
        // https://github.com/getsentry/sentry-webpack-plugin#options

        // Suppresses source map uploading logs during build
        silent: true,

        org: 'httpsgithubcomflowgpt',
        project: 'flow-gpt',
      },
      {
        // For all available options, see:
        // https://docs.sentry.io/platforms/javascript/guides/nextjs/manual-setup/

        // Upload a larger set of source maps for prettier stack traces (increases build time)
        widenClientFileUpload: true,

        // Transpiles SDK to be compatible with IE11 (increases bundle size)
        transpileClientSDK: true,

        // Routes browser requests to Sentry through a Next.js rewrite to circumvent ad-blockers (increases server load)
        tunnelRoute: '/monitoring',

        // Hides source maps from generated client bundles
        hideSourceMaps: true,

        // Automatically tree-shake Sentry logger statements to reduce bundle size
        disableLogger: true,

        // Enables automatic instrumentation of Vercel Cron Monitors.
        // See the following for more information:
        // https://docs.sentry.io/product/crons/
        // https://vercel.com/docs/cron-jobs
        automaticVercelMonitors: true,
      }
    )
  }

  return plugins.reduce((acc, next) => next(acc), result)
}

export default nextConfig
