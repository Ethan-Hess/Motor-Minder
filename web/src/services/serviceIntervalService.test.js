import { describe, expect, it } from 'vitest';
import { getAllServiceIntervals, getIntervalForService } from './serviceIntervalService.js';

describe('serviceIntervalService', () => {
  it('returns interval details for known service names', () => {
    const interval = getIntervalForService('oil_change');

    expect(interval).toEqual({ miles: [5000, 7500], months: [3, 6] });
  });

  it('returns null for unknown services', () => {
    expect(getIntervalForService('unknown_service')).toBeNull();
  });

  it('returns a list of intervals with serviceName keys', () => {
    const intervals = getAllServiceIntervals();

    expect(intervals.length).toBeGreaterThan(0);
    expect(intervals[0]).toHaveProperty('serviceName');
  });
});
