import { test, expect } from '@playwright/test';
import { EquipmentListPage } from '../pages/EquipmentListPage';
import { AddEquipmentPage } from '../pages/AddEquipmentPage';
import { DataGenerator } from '../utils/dataGenerator';

test.describe('Error Scenarios', () => {
  let equipmentListPage: EquipmentListPage;
  let addEquipmentPage: AddEquipmentPage;

  test.beforeEach(async ({ page }) => {
    equipmentListPage = new EquipmentListPage(page);
    addEquipmentPage = new AddEquipmentPage(page);
    await equipmentListPage.navigateTo();
  });

  test('Verify timeout handling for slow API responses', async ({ page }) => {
    // Mock slow API response
    await page.route('**/api/equipment', route => 
      new Promise(resolve => setTimeout(() => route.continue(), 10000))
    );
    
    await equipmentListPage.navigateTo();
    
    // Verify loading state appears
    const loadingElements = await page.locator('.loading, .spinner, [aria-busy="true"]').all();
    
    if (loadingElements.length > 0) {
      await expect(loadingElements[0]).toBeVisible();
    } else {
      // If no loading indicator, verify page eventually loads or times out
      try {
        await equipmentListPage.equipmentTable.waitFor({ state: 'visible', timeout: 15000 });
      } catch (error) {
        // Expected timeout - verify error handling
        const errorMessages = await page.locator('.error-message, .text-red-500, [role="alert"]').allTextContents();
        expect(errorMessages.length).toBeGreaterThan(0);
      }
    }
  });

  test('Verify empty equipment list handling', async ({ page }) => {
    // Mock API returning empty array
    await page.route('**/api/equipment', route => 
      route.fulfill({ 
        status: 200, 
        contentType: 'application/json',
        body: '[]'
      })
    );
    
    await equipmentListPage.navigateTo();
    
    // Verify empty state message
    const emptyMessages = await page.locator('.empty-state, .no-data, .text-center').allTextContents();
    
    if (emptyMessages.length > 0) {
      expect(emptyMessages.some(msg => 
        msg.includes('No equipment') || 
        msg.includes('empty') ||
        msg.includes('Add your first')
      )).toBeTruthy();
    } else {
      // If no empty state, verify table is empty
      const rowCount = await equipmentListPage.getEquipmentCount();
      expect(rowCount).toBe(0);
    }
  });

  test('Verify concurrent status updates handling', async ({ page }) => {
    // Add equipment first
    await equipmentListPage.clickAddEquipment();
    const testData = DataGenerator.generateEquipmentData('Active');
    await addEquipmentPage.fillEquipmentForm(
      testData.name,
      testData.status,
      testData.location
    );
    await addEquipmentPage.submitForm();
    await addEquipmentPage.verifySuccessMessage();
    
    // Find equipment
    const equipmentNames = await equipmentListPage.getEquipmentNames();
    const equipmentIndex = equipmentNames.indexOf(testData.name);
    expect(equipmentIndex).toBeGreaterThanOrEqual(0);
    
    // Simulate concurrent status updates by making multiple rapid changes
    await equipmentListPage.selectStatus('Idle', equipmentIndex);
    await equipmentListPage.waitForStatusUpdate();
    
    // Immediately try another status change
    await equipmentListPage.selectStatus('Under Maintenance', equipmentIndex);
    await equipmentListPage.waitForStatusUpdate();
    
    // Verify final status is correct
    const finalStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    expect(finalStatus).toBe('Under Maintenance');
  });

  test('Verify incorrect web URL handling', async ({ page }) => {
    // Navigate to incorrect URL - this will throw an error
    try {
      await page.goto('https://qa-assignment-omega.vercel.appp/');
    } catch (error) {
      // Expected error for incorrect URL
      const errorMessage = error instanceof Error ? error.message : String(error);
      expect(errorMessage).toMatch(/ERR_NAME_NOT_RESOLVED|net::ERR_NAME_NOT_RESOLVED/);
    }
  });
}); 