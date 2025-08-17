import { test, expect } from '@playwright/test';
import { EquipmentListPage } from '../pages/EquipmentListPage';
import { AddEquipmentPage } from '../pages/AddEquipmentPage';
import { EquipmentStatus } from '../../../data/equipmentInterface';
import { DataGenerator } from '../utils/dataGenerator';

test.describe('Add Equipment', () => {
  let equipmentListPage: EquipmentListPage;
  let addEquipmentPage: AddEquipmentPage;

  test.beforeEach(async ({ page }) => {
    equipmentListPage = new EquipmentListPage(page);
    addEquipmentPage = new AddEquipmentPage(page);
    await equipmentListPage.navigateTo();
    await equipmentListPage.clickAddEquipment();
  });

  // Add Equipment with Active status
  test('Verify adding equipment with Active status appears in equipment list', async ({ page }) => {
    const testData = DataGenerator.generateEquipmentData('Active');
    
    await addEquipmentPage.fillEquipmentForm(
      testData.name,
      testData.status,
      testData.location
    );
    
    await addEquipmentPage.submitForm();
    await addEquipmentPage.verifySuccessMessage();
    
    // Wait for any animations to complete
    await page.waitForTimeout(2000);
    
    // Wait for the list to be fully updated
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    await equipmentListPage.refreshList();
    
    // Retry logic for finding equipment
    let found = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      found = await equipmentListPage.scrollToEquipment(testData.name);
      if (found) break;
      
      if (attempt < 2) {
        console.log(`Equipment not found on attempt ${attempt + 1}, retrying...`);
        await page.waitForTimeout(1000);
        await equipmentListPage.refreshList();
      }
    }
    
    expect(found, `New equipment ${testData.name} should be found in the list`).toBe(true);
    
    const equipmentNames = await equipmentListPage.getEquipmentNames();
    const equipmentStatuses = await equipmentListPage.getEquipmentStatuses();
    
    expect(equipmentNames).toContain(testData.name);
    expect(equipmentStatuses[equipmentNames.indexOf(testData.name)]).toBe(testData.status);
  });

  // Add Equipment with Idle status
  test('Verify adding equipment with Idle status appears in equipment list', async ({ page }) => {
    const testData = DataGenerator.generateEquipmentData('Idle');
    
    await addEquipmentPage.fillEquipmentForm(
      testData.name,
      testData.status,
      testData.location
    );
    
    await addEquipmentPage.submitForm();
    await addEquipmentPage.verifySuccessMessage();
    
    // Wait for any animations to complete
    await page.waitForTimeout(2000);
    
    // Wait for the list to be fully updated
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    await equipmentListPage.refreshList();
    
    // Retry logic for finding equipment
    let found = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      found = await equipmentListPage.scrollToEquipment(testData.name);
      if (found) break;
      
      if (attempt < 2) {
        console.log(`Equipment not found on attempt ${attempt + 1}, retrying...`);
        await page.waitForTimeout(1000);
        await equipmentListPage.refreshList();
      }
    }
    
    expect(found, `New equipment ${testData.name} should be found in the list`).toBe(true);
    
    const equipmentNames = await equipmentListPage.getEquipmentNames();
    const equipmentStatuses = await equipmentListPage.getEquipmentStatuses();
    
    expect(equipmentNames).toContain(testData.name);
    expect(equipmentStatuses[equipmentNames.indexOf(testData.name)]).toBe(testData.status);
  });

  // Add Equipment with Under Maintenance status
  test('Verify adding equipment with Under Maintenance status appears in equipment list', async ({ page }) => {
    const testData = DataGenerator.generateEquipmentData('Under Maintenance');
    
    await addEquipmentPage.fillEquipmentForm(
      testData.name,
      testData.status,
      testData.location
    );
    
    await addEquipmentPage.submitForm();
    await addEquipmentPage.verifySuccessMessage();
    
    // Wait for any animations to complete
    await page.waitForTimeout(2000);
    
    // Wait for the list to be fully updated
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    await equipmentListPage.refreshList();
    
    // Retry logic for finding equipment
    let found = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      found = await equipmentListPage.scrollToEquipment(testData.name);
      if (found) break;
      
      if (attempt < 2) {
        console.log(`Equipment not found on attempt ${attempt + 1}, retrying...`);
        await page.waitForTimeout(1000);
        await equipmentListPage.refreshList();
      }
    }
    
    expect(found, `New equipment ${testData.name} should be found in the list`).toBe(true);
    
    const equipmentNames = await equipmentListPage.getEquipmentNames();
    const equipmentStatuses = await equipmentListPage.getEquipmentStatuses();
    
    expect(equipmentNames).toContain(testData.name);
    expect(equipmentStatuses[equipmentNames.indexOf(testData.name)]).toBe(testData.status);
  });
});