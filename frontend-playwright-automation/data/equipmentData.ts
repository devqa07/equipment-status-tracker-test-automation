import { faker } from '@faker-js/faker';
import { 
  Equipment, 
  EquipmentStatus, 
  TestEquipmentData, 
  AddEquipmentRequest,
  TestFilters 
} from './equipmentInterface';

export class EquipmentTestData {
  static generateEquipmentName(): string {
    return `Test_equipment_${faker.number.int({ min: 100000, max: 999999 })}`;
  }

  static generateLocation(): string {
    return `Test_location_${faker.number.int({ min: 100000, max: 999999 })}`;
  }

  static generateOperatorName(): string {
    return faker.person.fullName();
  }

  static getRandomStatus(): EquipmentStatus {
    const statuses: EquipmentStatus[] = ['Active', 'Idle', 'Under Maintenance'];
    return statuses[Math.floor(Math.random() * statuses.length)];
  }

  static getValidEquipmentData(): TestEquipmentData {
    return {
      name: this.generateEquipmentName(),
      status: this.getRandomStatus(),
      location: this.generateLocation(),
      changedBy: this.generateOperatorName()
    };
  }

  static getValidAddEquipmentRequest(): AddEquipmentRequest {
    const data = this.getValidEquipmentData();
    return {
      name: data.name,
      status: data.status,
      location: data.location
    };
  }

  static getInvalidEquipmentData(): Partial<AddEquipmentRequest> {
    return {
      name: '',
      status: 'InvalidStatus' as EquipmentStatus,
      location: ''
    };
  }

  static getEquipmentWithSpecialCharacters(): TestEquipmentData {
    return {
      name: `Test@#$%^&*()_+{}|:<>?[]\\;'\",./`,
      status: 'Active',
      location: `Location@#$%^&*()_+{}|:<>?[]\\;'\",./`,
      changedBy: this.generateOperatorName()
    };
  }

  static getSampleEquipment(): Equipment[] {
    return [
      {
        id: 1,
        name: 'Excavator CAT 320',
        status: 'Active',
        location: 'Site A',
        lastUpdated: '2024-01-15T10:30:00Z'
      },
      {
        id: 2,
        name: 'Bulldozer Komatsu D65',
        status: 'Idle',
        location: 'Site B',
        lastUpdated: '2024-01-15T09:15:00Z'
      },
      {
        id: 3,
        name: 'Crane Liebherr LTM',
        status: 'Under Maintenance',
        location: 'Workshop',
        lastUpdated: '2024-01-14T16:45:00Z'
      }
    ];
  }

  static getTestFilters(): TestFilters[] {
    return [
      { status: 'Active' },
      { status: 'Idle' },
      { status: 'Under Maintenance' },
      { limit: 5, offset: 0 },
      { limit: 10, offset: 5 },
      { location: 'Site A' },
      { location: 'Workshop' }
    ];
  }

  static getPerformanceTestData(): TestEquipmentData[] {
    const testData: TestEquipmentData[] = [];
    for (let i = 0; i < 10; i++) {
      testData.push(this.getValidEquipmentData());
    }
    return testData;
  }

  static getEdgeCaseData(): TestEquipmentData[] {
    return [
      {
        name: 'A', // Minimum length
        status: 'Active',
        location: 'A',
        changedBy: 'A'
      },
      {
        name: 'A'.repeat(100), // Long name
        status: 'Idle',
        location: 'A'.repeat(100),
        changedBy: 'A'.repeat(50)
      },
      {
        name: 'Equipment with spaces',
        status: 'Under Maintenance',
        location: 'Location with spaces',
        changedBy: 'Operator with spaces'
      }
    ];
  }
} 