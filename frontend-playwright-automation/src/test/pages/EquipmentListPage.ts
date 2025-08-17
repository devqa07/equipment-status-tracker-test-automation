import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class EquipmentListPage extends BasePage {
  readonly addEquipmentButton: Locator;
  readonly equipmentTable: Locator;
  readonly equipmentRows: Locator;
  readonly refreshButton: Locator;
  readonly tableContainer: Locator;
  readonly columnHeaders: Locator;
  readonly pageTitle: Locator;
  readonly pageSubtitle: Locator;
  readonly listTitle: Locator;
  readonly statusSummary: Locator;

  constructor(page: Page) {
    super(page);
    this.addEquipmentButton = page.locator('header button.bg-green-600');
    this.refreshButton = page.locator('header button.bg-blue-600');
    this.equipmentTable = page.locator('table.min-w-full');
    this.equipmentRows = page.locator('table.min-w-full tbody tr');
    this.tableContainer = page.locator('div.overflow-x-auto');
    this.columnHeaders = page.locator('table.min-w-full thead th');
    this.pageTitle = page.locator('h1.text-3xl.font-bold');
    this.pageSubtitle = page.getByText('Monitor and manage equipment status in real-time');
    this.listTitle = page.locator('main > div > div.px-6.py-4.border-b.border-gray-200 > h2');
    this.statusSummary = page.locator('main > div > div.px-6.py-4.border-b.border-gray-200 > p');
  }

  async navigateTo() {
    await this.page.goto('https://qa-assignment-omega.vercel.app/');
    await this.page.waitForLoadState('networkidle');
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForLoadState('domcontentloaded');

    // Check for fetch error and reload if needed
    const errorText = await this.page.getByText('Failed to fetch equipment').isVisible();
    if (errorText) {
      console.log('Detected fetch error, reloading page...');
      await this.page.reload();
      await this.page.waitForLoadState('networkidle');
      await this.page.waitForLoadState('domcontentloaded');
    }
  }

  async waitForEquipmentData() {
    return this.page.waitForResponse(
      response => response.url().includes('/api/equipment') && response.status() === 200,
      { timeout: 10000 }
    );
  }

  async clickAddEquipment() {
    await this.click(this.addEquipmentButton);
  }

  async scrollToBottom() {
    // Scroll to the bottom of the table container
    await this.tableContainer.evaluate((element) => {
      element.scrollTop = element.scrollHeight;
    });
    
    // Also try keyboard End key as backup
    await this.page.keyboard.press('End');
    
    // Wait for any dynamic content to load
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForTimeout(1000); // Give extra time for content to load
  }

  async getEquipmentNames(): Promise<string[]> {
    await this.equipmentTable.waitFor({ state: 'visible' });
    await this.scrollToBottom();

    const names: string[] = [];
    const rows = await this.equipmentRows.all();
    
    for (const row of rows) {
      const nameCell = await row.locator('td').first();
      const fullText = await nameCell.textContent();
      if (fullText) {
        const name = fullText.split('ID:')[0].trim();
        names.push(name);
      }
    }
    
    return names;
  }

  async getEquipmentStatuses(): Promise<string[]> {
    await this.scrollToBottom();

    const statuses: string[] = [];
    const count = await this.equipmentRows.count();
    
    for (let i = 0; i < count; i++) {
      const statusCell = await this.equipmentRows.nth(i).locator('td').nth(2);
      const status = await statusCell.textContent();
      if (status) statuses.push(status.trim());
    }
    
    return statuses;
  }

  async refreshList() {
    await this.refreshButton.waitFor({ state: 'visible' });
    
    await Promise.all([
      this.page.waitForResponse(
        response => response.url().includes('/api/equipment') && response.status() === 200,
        { timeout: 30000 }
      ),
      this.click(this.refreshButton)
    ]);

    await this.equipmentTable.waitFor({ state: 'visible' });
    await this.page.waitForLoadState('networkidle');
    await this.scrollToBottom();
  }

  async getEquipmentCount(): Promise<number> {
    return await this.equipmentRows.count();
  }

  async getColumnHeaders(): Promise<string[]> {
    const headers: string[] = [];
    const count = await this.columnHeaders.count();
    
    for (let i = 0; i < count; i++) {
      const header = await this.columnHeaders.nth(i).textContent();
      if (header) headers.push(header.trim());
    }
    
    return headers;
  }

  async findEquipmentInList(name: string): Promise<boolean> {
    await this.scrollToBottom();
    const names = await this.getEquipmentNames();
    return names.includes(name);
  }

  async scrollToEquipment(name: string): Promise<boolean> {
    console.log(`Looking for equipment: ${name}`);
    
    // Try up to 3 times
    for (let attempt = 0; attempt < 3; attempt++) {
      await this.scrollToBottom();
      
      const rows = await this.equipmentRows.all();
      console.log(`Attempt ${attempt + 1}: Found ${rows.length} equipment rows`);
      
      for (const row of rows) {
        const nameCell = await row.locator('td').first();
        const fullText = await nameCell.textContent();
        if (fullText && fullText.includes(name)) {
          await row.scrollIntoViewIfNeeded();
          console.log(`Found equipment: ${name}`);
          return true;
        }
      }
      
      if (attempt < 2) {
        console.log(`Equipment not found on attempt ${attempt + 1}, retrying...`);
        await this.refreshList();
      }
    }
    
    console.log(`Equipment not found after all attempts: ${name}`);
    return false;
  }

  async getStatusCounts(): Promise<{ active: number; idle: number; maintenance: number }> {
    await this.scrollToBottom();
    const statuses = await this.getEquipmentStatuses();
    
    return {
      active: statuses.filter(status => status === 'Active').length,
      idle: statuses.filter(status => status === 'Idle').length,
      maintenance: statuses.filter(status => status === 'Under Maintenance').length
    };
  }

  async getSummaryStatusCounts(): Promise<{ active: number; idle: number; maintenance: number }> {
    await this.statusSummary.waitFor({ state: 'visible', timeout: 10000 });
    const summaryText = await this.statusSummary.textContent();
    if (!summaryText) throw new Error('Status summary text is empty');

    const matches = summaryText.match(/Active:\s*(\d+)\s*\|\s*Idle:\s*(\d+)\s*\|\s*Maintenance:\s*(\d+)/);
    if (!matches) throw new Error('Failed to parse status summary text');

    const [_, active, idle, maintenance] = matches.map(Number);
    return { active, idle, maintenance };
  }

  async verifyStatusCounts(): Promise<void> {
    const actualCounts = await this.getStatusCounts();
    const summaryCounts = await this.getSummaryStatusCounts();
    const rowCount = await this.getEquipmentCount();

    // Log the analysis
    console.log('\nStatus Count Analysis:');
    console.log('Summary Display:', {
      ...summaryCounts,
      total: summaryCounts.active + summaryCounts.idle + summaryCounts.maintenance
    });
    console.log('Actual List Counts:', {
      ...actualCounts,
      total: actualCounts.active + actualCounts.idle + actualCounts.maintenance
    });
    console.log('Table Row Count:', rowCount);

    // Verify counts
    if (summaryCounts.idle !== actualCounts.idle) {
      throw new Error(`Idle count mismatch: Summary shows ${summaryCounts.idle}, List has ${actualCounts.idle}`);
    }
    if (summaryCounts.maintenance !== actualCounts.maintenance) {
      throw new Error(`Maintenance count mismatch: Summary shows ${summaryCounts.maintenance}, List has ${actualCounts.maintenance}`);
    }
    if (Math.abs(summaryCounts.active - actualCounts.active) > 1) {
      throw new Error(`Active count difference exceeds 1: Summary shows ${summaryCounts.active}, List has ${actualCounts.active}`);
    }
    if (rowCount !== (actualCounts.active + actualCounts.idle + actualCounts.maintenance)) {
      throw new Error(`Row count (${rowCount}) doesn't match sum of status counts (${actualCounts.active + actualCounts.idle + actualCounts.maintenance})`);
    }
  }

  // Status update methods
  async openStatusDropdown(rowIndex: number): Promise<void> {
    const row = this.equipmentRows.nth(rowIndex);
    const statusSelect = row.locator('td:last-child select');
    await statusSelect.click();
  }

  async selectStatus(status: string, rowIndex: number = 0): Promise<void> {
    const row = this.equipmentRows.nth(rowIndex);
    const statusSelect = row.locator('td:last-child select');
    await statusSelect.selectOption(status);
  }

  async waitForStatusUpdate(): Promise<void> {
    await this.page.waitForResponse(
      response => response.url().includes('/api/equipment') && response.status() === 200,
      { timeout: 10000 }
    );
    await this.page.waitForLoadState('networkidle');
  }

  async getEquipmentStatus(rowIndex: number): Promise<string> {
    const row = this.equipmentRows.nth(rowIndex);
    const statusCell = row.locator('td').nth(2);
    const status = await statusCell.textContent();
    return status?.trim() || '';
  }

  async waitForEquipmentToLoad(): Promise<void> {
    await this.equipmentTable.waitFor({ state: 'visible' });
    await this.page.waitForLoadState('networkidle');
  }

  async openHistoryModal(rowIndex: number): Promise<void> {
    const row = this.equipmentRows.nth(rowIndex);
    const historyButton = row.locator('td.px-6.py-4.whitespace-nowrap.text-sm.font-medium.space-x-2 button');
    await historyButton.click();
  }



  async waitForTimeout(ms: number): Promise<void> {
    await this.page.waitForTimeout(ms);
  }
}