import { test, expect } from '@playwright/test';
import { EquipmentListPage } from '../pages/EquipmentListPage';
import { AddEquipmentPage } from '../pages/AddEquipmentPage';
import { DataGenerator } from '../utils/dataGenerator';

test.describe('Update Equipment Status', () => {
  let equipmentListPage: EquipmentListPage;
  let addEquipmentPage: AddEquipmentPage;

  test.beforeEach(async ({ page }) => {
    equipmentListPage = new EquipmentListPage(page);
    addEquipmentPage = new AddEquipmentPage(page);
    await equipmentListPage.navigateTo();
    await equipmentListPage.clickAddEquipment();
  });

  test('Verify status change: Active → Idle', async ({ page }) => {
    // Add new equipment with Active status
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
    
    // Find and scroll to the newly added equipment
    console.log(`Looking for equipment: ${testData.name}`);
    
    // Retry logic for finding equipment
    let found = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      found = await equipmentListPage.scrollToEquipment(testData.name);
      if (found) break;
      
      if (attempt < 2) {
        console.log(`Equipment not found on attempt ${attempt + 1}, retrying...`);
        await page.waitForTimeout(1000);
        await page.reload();
        await page.waitForLoadState('networkidle');
      }
    }
    
    expect(found, `New equipment ${testData.name} should be found in the list`).toBe(true);
    
    // Get equipment index
    const equipmentNames = await equipmentListPage.getEquipmentNames();
    const equipmentIndex = equipmentNames.indexOf(testData.name);
    expect(equipmentIndex).toBeGreaterThanOrEqual(0);
    
    // Verify initial status is Active
    const initialStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    expect(initialStatus).toBe('Active');
    
    // Change from Active to Idle
    console.log('Changing status from Active to Idle');
    await equipmentListPage.selectStatus('Idle', equipmentIndex);
    await equipmentListPage.waitForStatusUpdate();
    
    // Verify status changed to Idle
    const updatedStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    expect(updatedStatus).toBe('Idle');
    
    // Verify equipment remains in list
    const updatedEquipmentNames = await equipmentListPage.getEquipmentNames();
    expect(updatedEquipmentNames[equipmentIndex]).toContain(testData.name);
  });

  test('Verify status change: Idle → Active', async ({ page }) => {
    // Add new equipment with Active status
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
    
    // Find and scroll to the newly added equipment
    console.log(`Looking for equipment: ${testData.name}`);
    
    // Retry logic for finding equipment
    let found = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      found = await equipmentListPage.scrollToEquipment(testData.name);
      if (found) break;
      
      if (attempt < 2) {
        console.log(`Equipment not found on attempt ${attempt + 1}, retrying...`);
        await page.waitForTimeout(1000);
        await page.reload();
        await page.waitForLoadState('networkidle');
      }
    }
    
    expect(found, `New equipment ${testData.name} should be found in the list`).toBe(true);
    
    // Get equipment index
    const equipmentNames = await equipmentListPage.getEquipmentNames();
    const equipmentIndex = equipmentNames.indexOf(testData.name);
    expect(equipmentIndex).toBeGreaterThanOrEqual(0);
    
    // Verify initial status is Active
    const initialStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    expect(initialStatus).toBe('Active');
    
    // First change from Active to Idle
    console.log('First changing status from Active to Idle');
    await equipmentListPage.selectStatus('Idle', equipmentIndex);
    await equipmentListPage.waitForStatusUpdate();
    
    const idleStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    expect(idleStatus).toBe('Idle');
    
    // Then change from Idle to Active
    console.log('Then changing status from Idle to Active');
    await equipmentListPage.selectStatus('Active', equipmentIndex);
    await equipmentListPage.waitForStatusUpdate();
    
    // Wait a bit more for the status to update
    await page.waitForTimeout(2000);
    
    const finalStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    console.log(`Expected status: Active, Actual status: ${finalStatus}`);
    expect(finalStatus).toBe('Active');
    
    // Verify equipment remains in list
    const updatedEquipmentNames = await equipmentListPage.getEquipmentNames();
    expect(updatedEquipmentNames[equipmentIndex]).toContain(testData.name);
  });

  test('Verify status change: Active → Under Maintenance', async ({ page }) => {
    // Add new equipment with Active status
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
    
    // Find and scroll to the newly added equipment
    console.log(`Looking for equipment: ${testData.name}`);
    
    // Retry logic for finding equipment
    let found = false;
    for (let attempt = 0; attempt < 3; attempt++) {
      found = await equipmentListPage.scrollToEquipment(testData.name);
      if (found) break;
      
      if (attempt < 2) {
        console.log(`Equipment not found on attempt ${attempt + 1}, retrying...`);
        await page.waitForTimeout(1000);
        await page.reload();
        await page.waitForLoadState('networkidle');
      }
    }
    
    expect(found, `New equipment ${testData.name} should be found in the list`).toBe(true);
    
    // Get equipment index
    const equipmentNames = await equipmentListPage.getEquipmentNames();
    const equipmentIndex = equipmentNames.indexOf(testData.name);
    expect(equipmentIndex).toBeGreaterThanOrEqual(0);
    
    // Verify initial status is Active
    const initialStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    expect(initialStatus).toBe('Active');
    
    // Change from Active to Under Maintenance
    console.log('Changing status from Active to Under Maintenance');
    await equipmentListPage.selectStatus('Under Maintenance', equipmentIndex);
    await equipmentListPage.waitForStatusUpdate();
    
    // Add delay for Under Maintenance status to ensure proper update
    await page.waitForTimeout(2000);
    
    // Verify status changed to Under Maintenance
    const updatedStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    console.log(`Expected status: Under Maintenance, Actual status: ${updatedStatus}`);
    expect(updatedStatus).toBe('Under Maintenance');
    
    // Verify equipment remains in list
    const updatedEquipmentNames = await equipmentListPage.getEquipmentNames();
    expect(updatedEquipmentNames[equipmentIndex]).toContain(testData.name);
  });
});