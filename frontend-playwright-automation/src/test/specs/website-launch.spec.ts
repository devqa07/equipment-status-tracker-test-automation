import { test, expect } from '@playwright/test';

// Basic smoke tests to verify website accessibility and core UI elements
test.describe('Website Launch and Navigation', () => {
  test('Verify website launch and navigation to Add Equipment', async ({ page }) => {
    // Navigate to application URL and wait for initial load
    await page.goto('https://qa-assignment-omega.vercel.app/');
    await page.waitForLoadState('networkidle');
    
    // Verify page title
    const title = await page.title();
    expect(title).toContain('Equipment');
    
    // Verify and interact with Add Equipment button
    const addButton = page.getByRole('button', { name: 'Add Equipment' });
    await expect(addButton).toBeVisible();
    await addButton.click();
    
    // Wait for navigation and capture page state
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'test-results/website-launch-verification.png' });
  });

  test('Verify main page elements', async ({ page }) => {
    // Load main page
    await page.goto('https://qa-assignment-omega.vercel.app/');
    await page.waitForLoadState('networkidle');
    
    // Verify header elements
    await expect(page.getByText('Equipment Status Tracker')).toBeVisible();
    await expect(page.getByText('Monitor and manage equipment status in real-time')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Add Equipment' })).toBeVisible();
    
    // Verify either equipment table or loading state is present
    const hasTable = await page.locator('table').isVisible();
    const hasLoading = await page.getByText('Loading equipment...').isVisible();
    expect(hasTable || hasLoading).toBeTruthy();
  });
}); 