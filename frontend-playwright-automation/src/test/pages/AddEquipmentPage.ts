import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';
import { EquipmentStatus } from '../../../data/equipmentInterface';

export class AddEquipmentPage extends BasePage {
  private readonly nameInput: Locator;
  private readonly statusSelect: Locator;
  private readonly locationInput: Locator;
  private readonly submitButton: Locator;
  private readonly cancelButton: Locator;
  private readonly form: Locator;
  private readonly successMessage: Locator;

  constructor(page: Page) {
    super(page);
    
    this.nameInput = page.locator('#name');
    this.statusSelect = page.locator('#status');
    this.locationInput = page.locator('#location');
    this.submitButton = page.locator('form button.bg-blue-600');
    this.cancelButton = page.locator('form button.border-gray-300');
    this.form = page.locator('form');
    this.successMessage = page.getByText('Equipment added successfully');
  }

  async fillEquipmentForm(name: string, status: EquipmentStatus, location: string) {
    await this.form.waitFor({ state: 'visible' });
    
    await this.fill(this.nameInput, name);
    await this.nameInput.evaluate(el => el.blur());
    
    if (status !== 'Active') {
      await this.statusSelect.selectOption(status);
      await this.page.waitForFunction(
        (status) => (document.querySelector('#status') as HTMLSelectElement)?.value === status,
        status
      );
    }
    
    await this.fill(this.locationInput, location);
    await this.locationInput.evaluate(el => el.blur());
  }

  async submitForm() {
    // Click the submit button first
    await this.click(this.submitButton);
    
    // Wait for either the success message or a response
    try {
      await Promise.race([
        this.page.waitForResponse(
          response => response.url().includes('/api/equipment') && response.status() === 200,
          { timeout: 15000 }
        ),
        this.successMessage.waitFor({ state: 'visible', timeout: 15000 })
      ]);
    } catch (error) {
      // If API response times out, still check for success message
      console.log('API response timeout, checking for success message...');
      await this.successMessage.waitFor({ state: 'visible', timeout: 5000 });
    }
  }

  async cancelForm() {
    await this.click(this.cancelButton);
  }

  async verifySuccessMessage() {
    await this.successMessage.waitFor({ state: 'visible' });
  }
}