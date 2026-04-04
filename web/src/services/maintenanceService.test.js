import { describe, expect, it } from 'vitest';
import { getServiceStatus, getServiceStatusDetailed } from './maintenanceService.js';
import { SERVICE_STATUS } from '../types/domain.js';

describe('maintenanceService', () => {
  it('returns unknown status when no interval is provided', () => {
    const result = getServiceStatusDetailed(12000, { mileage: 10000, date: '2025-01-01' }, null, '2025-04-01');

    expect(result).toEqual({
      status: SERVICE_STATUS.UNKNOWN,
      dueMiles: null,
      dueDate: null,
      overdueAmount: null,
      missing: true,
    });
  });

  it('returns overdue and missing when no last service exists', () => {
    const result = getServiceStatusDetailed(12000, null, { miles: [5000, 7500] }, '2025-04-01');

    expect(result.status).toBe(SERVICE_STATUS.OVERDUE);
    expect(result.missing).toBe(true);
  });

  it('computes mileage due soon and due miles', () => {
    const result = getServiceStatusDetailed(
      17000,
      { mileage: 10000, date: '2025-01-01' },
      { miles: [5000, 7500] },
      '2025-04-01',
    );

    expect(result.status).toBe(SERVICE_STATUS.DUE_SOON);
    expect(result.dueMiles).toBe(17500);
    expect(result.dueDate).toBe(null);
    expect(result.overdueAmount).toBe(null);
    expect(result.missing).toBe(false);
  });

  it('computes mileage overdue amount', () => {
    const result = getServiceStatusDetailed(
      19000,
      { mileage: 10000, date: '2025-01-01' },
      { miles: [5000, 7500] },
      '2025-04-01',
    );

    expect(result.status).toBe(SERVICE_STATUS.OVERDUE);
    expect(result.dueMiles).toBe(17500);
    expect(result.overdueAmount).toBe('1500 mi over');
  });

  it('computes month-based due date and due-soon status', () => {
    const result = getServiceStatusDetailed(
      15000,
      { mileage: 10000, date: '2025-01-31' },
      { months: [3, 6] },
      '2025-05-31',
    );

    expect(result.status).toBe(SERVICE_STATUS.DUE_SOON);
    expect(result.dueDate).toBe('2025-07-31');
    expect(result.overdueAmount).toBe(null);
  });

  it('computes year-based overdue amount using calendar-accurate rollovers', () => {
    const result = getServiceStatusDetailed(
      30000,
      { mileage: 10000, date: '2020-02-29' },
      { years: [3, 5] },
      '2025-03-01',
    );

    expect(result.status).toBe(SERVICE_STATUS.OVERDUE);
    expect(result.dueDate).toBe('2025-02-28');
    expect(result.overdueAmount).toBe('1 days over');
  });

  it('combines mileage and month overdue details', () => {
    const result = getServiceStatusDetailed(
      19500,
      { mileage: 10000, date: '2024-01-01' },
      { miles: [5000, 7500], months: [3, 6] },
      '2025-01-10',
    );

    expect(result.status).toBe(SERVICE_STATUS.OVERDUE);
    expect(result.overdueAmount).toContain('mi over');
    expect(result.overdueAmount).toContain('days over');
  });

  it('preserves compatibility status-only helper', () => {
    const status = getServiceStatus(
      19000,
      { mileage: 10000, date: '2025-01-01' },
      { miles: [5000, 7500] },
      '2025-04-01',
    );

    expect(status).toBe(SERVICE_STATUS.OVERDUE);
  });
});
