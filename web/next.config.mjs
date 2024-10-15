import bundleAnalyzer from '@next/bundle-analyzer'
import { withSentryConfig } from '@sentry/nextjs'
import * as path from 'path'

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
