import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: '../src/test/specs',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: '../reports/html-report' }],
    ['allure-playwright', { 
      outputFolder: '../allure-results',
      detail: true,
      suiteTitle: false,
      environmentInfo: {
        framework: 'playwright',
        language: 'typescript'
      }
    }]
  ],
  use: {
    baseURL: 'https://qa-assignment-omega.vercel.app',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 15000,
    navigationTimeout: 30000
  },

  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 }
      },
    },
    {
      name: 'firefox',
      use: { 
        ...devices['Desktop Firefox'],
        viewport: { width: 1920, height: 1080 },
        actionTimeout: 30000,  // Increased timeout for Firefox
        navigationTimeout: 45000,  // Increased timeout for Firefox
        launchOptions: {
          firefoxUserPrefs: {
            'dom.disable_beforeunload': true,
            'browser.tabs.warnOnClose': false
          }
        }
      },
    }
  ]
});