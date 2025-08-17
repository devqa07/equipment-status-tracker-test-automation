import { test, expect } from '@playwright/test';
import { EquipmentListPage } from '../pages/EquipmentListPage';

test.describe('Equipment List', () => {
  let equipmentListPage: EquipmentListPage;

  test.beforeEach(async ({ page }) => {
    equipmentListPage = new EquipmentListPage(page);
    await equipmentListPage.navigateTo();
  });

  test('Verify equipment list page loads successfully', async () => {
    // Wait for page and data to be loaded
    await equipmentListPage.waitForPageLoad();

    // Verify page title and subtitle
    await expect(equipmentListPage.pageTitle).toHaveText('Equipment Status Tracker');
    await expect(equipmentListPage.pageSubtitle).toBeVisible({timeout: 10000});

    // Wait for table to be visible
    await equipmentListPage.equipmentTable.waitFor({ state: 'visible' });
    
    // Wait for rows to be visible
    await equipmentListPage.equipmentRows.first().waitFor({ state: 'visible', timeout: 10000 });
    await equipmentListPage.scrollToBottom();
    
    // Get row count and verify it matches the title
    const rowCount = await equipmentListPage.getEquipmentCount();
    await expect(equipmentListPage.listTitle).toHaveText(`Equipment List (${rowCount} items)`);

    // Verify all status counts match expected relationships
    await equipmentListPage.verifyStatusCounts();
    
    // Verify the list title shows the correct total count
    await expect(equipmentListPage.listTitle).toHaveText(`Equipment List (${rowCount} items)`);
  });

  test('Verify equipment list displays all columns', async () => {
    // Wait for table to be visible
    await equipmentListPage.equipmentTable.waitFor({ state: 'visible' });
    
    // Get and verify column headers
    const headers = await equipmentListPage.getColumnHeaders();
    expect(headers).toEqual(['Equipment', 'Location', 'Status', 'Last Updated', 'Actions']);
  });

  test('Verify equipment list can be refreshed', async () => {
    // Wait for initial load
    await equipmentListPage.equipmentTable.waitFor({ state: 'visible' });
    const beforeRefresh = await equipmentListPage.getEquipmentCount();
    
    // Refresh and verify
    await equipmentListPage.refreshList();
    const afterRefresh = await equipmentListPage.getEquipmentCount();
    
    // After refresh should have at least as many items
    expect(afterRefresh).toBeGreaterThanOrEqual(beforeRefresh);
  });

  test('Verify equipment list scrolling', async () => {
    // Wait for initial load
    await equipmentListPage.equipmentTable.waitFor({ state: 'visible' });
    
    // Get initial count
    const initialCount = await equipmentListPage.getEquipmentCount();
    
    // Scroll through list
    await equipmentListPage.scrollToBottom();
    
    // Get count after scrolling
    const afterScrollCount = await equipmentListPage.getEquipmentCount();
    
    // Should have at least the same number of items
    expect(afterScrollCount).toBeGreaterThanOrEqual(initialCount);
  });
});