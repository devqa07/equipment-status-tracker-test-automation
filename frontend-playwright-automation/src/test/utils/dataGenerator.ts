import { faker } from '@faker-js/faker';
import { EquipmentStatus, TestEquipmentData } from '../../../data/equipmentInterface';

export class DataGenerator {
  static generateEquipmentData(status: EquipmentStatus = 'Active'): TestEquipmentData {
    return {
      name: `TF_equipment_${faker.number.int({ min: 10000, max: 99999 })}`,
      location: `TF_location_${faker.number.int({ min: 10000, max: 99999 })}`,
      status
    };
  }
}