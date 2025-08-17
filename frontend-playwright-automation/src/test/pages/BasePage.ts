import { Page, Locator, expect } from '@playwright/test';

export class BasePage {
  protected page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Navigation
  async goto(path: string) {
    try {
      // Use the path directly since baseURL is configured in playwright.config.ts
      await this.page.goto(path, {
        waitUntil: 'networkidle',
        timeout: 30000
      });
    } catch (error) {
      console.error('Navigation error:', error);
      throw error;
    }
  }

  // Basic interactions
  async click(locator: Locator) {
    await locator.click();
  }

  async fill(locator: Locator, value: string) {
    await locator.fill(value);
  }

  // Assertions
  async expectVisible(locator: Locator) {
    await expect(locator).toBeVisible();
  }

  async expectText(locator: Locator, text: string) {
    await expect(locator).toHaveText(text);
  }
} 