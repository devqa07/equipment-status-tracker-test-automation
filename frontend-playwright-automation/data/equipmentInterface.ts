export interface Equipment {
  id: number;
  name: string;
  status: EquipmentStatus;
  location: string;
  lastUpdated: string;
}

export type EquipmentStatus = 'Active' | 'Idle' | 'Under Maintenance';

export interface EquipmentHistory {
  id: number;
  equipmentId: number;
  previousStatus: EquipmentStatus;
  newStatus: EquipmentStatus;
  timestamp: string;
  changedBy: string;
}

export interface EquipmentHistoryResponse {
  success: boolean;
  data: {
    equipmentId: number;
    history: EquipmentHistory[];
    total: number;
    limit: number;
    offset: number;
    hasMore: boolean;
  };
}

export interface EquipmentListResponse {
  success: boolean;
  data: Equipment[];
  count: number;
}

export interface AddEquipmentRequest {
  name: string;
  status: EquipmentStatus;
  location: string;
}

export interface UpdateStatusRequest {
  status: EquipmentStatus;
  changedBy?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface TestEquipmentData {
  name: string;
  status: EquipmentStatus;
  location: string;
  changedBy?: string;
}

export interface TestFilters {
  status?: EquipmentStatus;
  location?: string;
  limit?: number;
  offset?: number;
} 