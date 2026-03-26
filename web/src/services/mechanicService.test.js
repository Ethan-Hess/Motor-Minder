import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fetchAllMechanics } from '../repositories/mechanicRepository.js';
import { findMechanicByCityState, listMechanics } from './mechanicService.js';

vi.mock('../repositories/mechanicRepository.js', () => ({
  fetchAllMechanics: vi.fn(),
}));

describe('mechanicService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns normalized mechanic objects', async () => {
    fetchAllMechanics.mockResolvedValueOnce([
      {
        id: 'm-1',
        name: 'A Shop',
        address: { city: 'Alpine', state: 'UT', address_line_1: '1 Main', zip_code: 84004, country: 'USA' },
        services: ['oil_change', 'invalid'],
        rating: 4.2,
      },
    ]);

    const result = await listMechanics();

    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('m-1');
    expect(result[0].services).toEqual(['oil_change']);
  });

  it('returns first city/state match using case-insensitive comparison', async () => {
    fetchAllMechanics.mockResolvedValueOnce([
      {
        id: 'm-1',
        name: 'A Shop',
        address: { city: 'ALPINE', state: 'ut', address_line_1: '1 Main', zip_code: 84004, country: 'USA' },
      },
      {
        id: 'm-2',
        name: 'B Shop',
        address: { city: 'Alpine', state: 'UT', address_line_1: '2 Main', zip_code: 84004, country: 'USA' },
      },
    ]);

    const result = await findMechanicByCityState(' alpine ', ' UT ');

    expect(result).not.toBeNull();
    expect(result.id).toBe('m-1');
  });

  it('returns null for blank query inputs', async () => {
    expect(await findMechanicByCityState('', 'UT')).toBeNull();
    expect(await findMechanicByCityState('Alpine', '')).toBeNull();
  });

  it('returns null when no mechanics match', async () => {
    fetchAllMechanics.mockResolvedValueOnce([
      {
        id: 'm-1',
        name: 'A Shop',
        address: { city: 'Lehi', state: 'UT', address_line_1: '1 Main', zip_code: 84043, country: 'USA' },
      },
    ]);

    const result = await findMechanicByCityState('Alpine', 'UT');
    expect(result).toBeNull();
  });
});
