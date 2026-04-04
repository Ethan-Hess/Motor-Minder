import { createMechanic } from '../types/domain.js';
import { fetchAllMechanics } from '../repositories/mechanicRepository.js';

export async function listMechanics() {
  const mechanics = await fetchAllMechanics();
  return mechanics.map((mechanic) => ({ id: mechanic.id, ...createMechanic(mechanic) }));
}

export async function findMechanicByCityState(city, state) {
  const normalizedCity = (city ?? '').trim().toLowerCase();
  const normalizedState = (state ?? '').trim().toLowerCase();

  if (!normalizedCity || !normalizedState) {
    return null;
  }

  const mechanics = await listMechanics();

  for (const mechanic of mechanics) {
    const mechanicCity = mechanic.address.city.trim().toLowerCase();
    const mechanicState = mechanic.address.state.trim().toLowerCase();

    if (mechanicCity === normalizedCity && mechanicState === normalizedState) {
      return mechanic;
    }
  }

  return null;
}
