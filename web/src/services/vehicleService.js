import {
  createVehicle as createVehicleShape,
} from '../types/domain.js';
import {
  createVehicle as createVehicleRepo,
  deleteVehicle as deleteVehicleRepo,
  fetchVehicleById,
  fetchVehiclesByUser,
  updateVehicle as updateVehicleRepo,
} from '../repositories/vehicleRepository.js';

function requireUserId(userId) {
  if (!userId) {
    throw new Error('userId is required for vehicle operations');
  }
}

export async function listVehicles(userId) {
  requireUserId(userId);
  return fetchVehiclesByUser(userId);
}

export async function getVehicle(userId, vehicleId) {
  requireUserId(userId);

  if (!vehicleId) {
    throw new Error('vehicleId is required');
  }

  return fetchVehicleById(userId, vehicleId);
}

export async function addVehicle(userId, vehicleInput) {
  requireUserId(userId);

  const vehicle = createVehicleShape({ ...vehicleInput, userId });
  return createVehicleRepo(userId, vehicle);
}

export async function editVehicle(userId, vehicleId, vehicleInput) {
  requireUserId(userId);

  if (!vehicleId) {
    throw new Error('vehicleId is required');
  }

  const vehicle = createVehicleShape({ ...vehicleInput, id: vehicleId, userId });
  return updateVehicleRepo(userId, vehicleId, vehicle);
}

export async function removeVehicle(userId, vehicleId) {
  requireUserId(userId);

  if (!vehicleId) {
    throw new Error('vehicleId is required');
  }

  await deleteVehicleRepo(userId, vehicleId);
}
