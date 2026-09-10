import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/browser',
  outputDir: './reports/phase-0/playwright-results',
  snapshotDir: './tests/browser/__screenshots__',
  timeout: 45_000,
  expect: { timeout: 8_000 },
  fullyParallel: true,
  reporter: [
    ['list'],
    ['json', { outputFile: 'reports/phase-0/playwright-report.json' }],
    ['html', { outputFolder: 'reports/phase-0/playwright-html', open: 'never' }]
  ],
  use: {
    baseURL: process.env.UKPG_BASE_URL || 'http://127.0.0.1:8765',
    launchOptions: {
      executablePath: process.env.UKPG_BROWSER_EXECUTABLE || undefined
    },
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure'
  },
  projects: [
    { name: 'desktop-chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile-chromium', use: { ...devices['Pixel 7'] } }
  ],
  webServer: process.env.UKPG_BASE_URL ? undefined : {
    command: 'python -m http.server 8765 --bind 127.0.0.1 --directory artifacts/phase-0-canary-site',
    url: 'http://127.0.0.1:8765/',
    reuseExistingServer: true,
    timeout: 30_000
  }
});
