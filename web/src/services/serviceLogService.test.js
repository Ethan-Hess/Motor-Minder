import { beforeEach, describe, expect, it, vi } from 'vitest';
import {
  getVehicleServices,
  listServiceLogsByVehicle,
  logServiceForVehicle,
} from '../repositories/serviceRepository.js';
import {
  listVehicleServiceHistory,
  listVehicleServices,
  logService,
} from './serviceLogService.js';

vi.mock('../repositories/serviceRepository.js', () => ({
  logServiceForVehicle: vi.fn(),
  listServiceLogsByVehicle: vi.fn(),
  getVehicleServices: vi.fn(),
}));

describe('serviceLogService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('requires a userId for logService', async () => {
    await expect(logService('', 'vehicle-1', 'oil_change', 10000, '2025-01-01'))
      .rejects.toThrow('userId is required for service operations');
  });

  it('forwards logService params to repository', async () => {
    logServiceForVehicle.mockResolvedValueOnce({ id: 'log-1' });

    const result = await logService('user-1', 'vehicle-1', 'oil_change', 10000, '2025-01-01');

    expect(logServiceForVehicle).toHaveBeenCalledWith(
      'user-1',
      'vehicle-1',
      'oil_change',
      10000,
      '2025-01-01',
    );
    expect(result).toEqual({ id: 'log-1' });
  });

  it('returns service history from repository', async () => {
    listServiceLogsByVehicle.mockResolvedValueOnce([{ id: 'log-1' }]);

    const result = await listVehicleServiceHistory('user-1', 'vehicle-1');

    expect(listServiceLogsByVehicle).toHaveBeenCalledWith('user-1', 'vehicle-1');
    expect(result).toEqual([{ id: 'log-1' }]);
  });

  it('returns vehicle services map from repository', async () => {
    getVehicleServices.mockResolvedValueOnce({ oil_change: { mileage: 10000, date: '2025-01-01' } });

    const result = await listVehicleServices('user-1', 'vehicle-1');

    expect(getVehicleServices).toHaveBeenCalledWith('user-1', 'vehicle-1');
    expect(result).toEqual({ oil_change: { mileage: 10000, date: '2025-01-01' } });
  });
});
