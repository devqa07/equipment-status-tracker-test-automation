import { test, expect } from '@playwright/test';
import { EquipmentListPage } from '../pages/EquipmentListPage';
import { AddEquipmentPage } from '../pages/AddEquipmentPage';
import { DataGenerator } from '../utils/dataGenerator';

test.describe('Status History', () => {
  let equipmentListPage: EquipmentListPage;
  let addEquipmentPage: AddEquipmentPage;

  test.beforeEach(async ({ page }) => {
    equipmentListPage = new EquipmentListPage(page);
    addEquipmentPage = new AddEquipmentPage(page);
    await equipmentListPage.navigateTo();
    await equipmentListPage.clickAddEquipment();
  });

  // Helper function to add equipment and find it in the list
  const addAndFindEquipment = async (page: any, testData: any) => {
    await addEquipmentPage.fillEquipmentForm(
      testData.name,
      testData.status,
      testData.location
    );
    
    await addEquipmentPage.submitForm();
    await addEquipmentPage.verifySuccessMessage();
    
    // Wait for list to update
    await page.waitForTimeout(2000);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // Find equipment with retry logic
    console.log(`Looking for equipment: ${testData.name}`);
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
    
    const equipmentNames = await equipmentListPage.getEquipmentNames();
    const equipmentIndex = equipmentNames.indexOf(testData.name);
    expect(equipmentIndex).toBeGreaterThanOrEqual(0);
    
    return equipmentIndex;
  };

  // Helper function to change status and verify
  const changeStatusAndVerify = async (fromStatus: string, toStatus: string, equipmentIndex: number) => {
    console.log(`Changing status from ${fromStatus} to ${toStatus}`);
    await equipmentListPage.selectStatus(toStatus, equipmentIndex);
    await equipmentListPage.waitForStatusUpdate();
    
    // Wait a bit more for the UI to update
    await equipmentListPage.waitForTimeout(2000);
    
    // Verify the status change with retry logic
    let newStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    let attempts = 0;
    const maxAttempts = 3;
    
    while (newStatus !== toStatus && attempts < maxAttempts) {
      console.log(`Attempt ${attempts + 1}: Expected ${toStatus}, got ${newStatus}`);
      await equipmentListPage.waitForTimeout(1000);
      await equipmentListPage.scrollToBottom();
      newStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
      attempts++;
    }
    
    expect(newStatus).toBe(toStatus);
  };

  // Helper function to verify history modal
  const verifyHistoryModal = async (page: any, equipmentIndex: number, expectedStatuses: string[]) => {
    console.log('Clicking on History button');
    await equipmentListPage.openHistoryModal(equipmentIndex);
    
    await page.waitForTimeout(2000);
    
    const modal = page.locator('.fixed.inset-0');
    await expect(modal).toBeVisible();
    
    const modalContent = await modal.textContent();
    console.log('Modal content:', modalContent);
    
    // Verify modal contains history information
    expect(modalContent).toContain('History');
    
    // Verify all expected statuses are present
    expectedStatuses.forEach(status => {
      expect(modalContent).toContain(status);
    });
    
    console.log('Status history verification completed');
  };

  test('Verify status history shows Active → Idle → Active changes', async ({ page }) => {
    const testData = DataGenerator.generateEquipmentData('Active');
    
    // Add equipment and get its index
    const equipmentIndex = await addAndFindEquipment(page, testData);
    
    // Verify initial status
    const initialStatus = await equipmentListPage.getEquipmentStatus(equipmentIndex);
    expect(initialStatus).toBe('Active');
    
    // Create status change history: Active → Idle → Active
    await changeStatusAndVerify('Active', 'Idle', equipmentIndex);
    await changeStatusAndVerify('Idle', 'Active', equipmentIndex);
    
    // Verify history modal contains the changes
    await verifyHistoryModal(page, equipmentIndex, ['Active', 'Idle']);
  });

}); 