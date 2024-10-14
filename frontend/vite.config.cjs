import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  test: {
    globalSetup: ['./tests/setup.ts'],
    setupFiles: ['./tests/setupMocks.ts'],
    pool: 'forks',
    detectOpenHandles: true,
    testTimeout: 50000,
  },
})
