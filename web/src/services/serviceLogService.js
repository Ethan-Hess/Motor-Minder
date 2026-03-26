import {
  getVehicleServices,
  listServiceLogsByVehicle,
  logServiceForVehicle,
} from '../repositories/serviceRepository.js';

function requireUserId(userId) {
  if (!userId) {
    throw new Error('userId is required for service operations');
  }
}

export async function logService(userId, vehicleId, serviceName, mileage, dateStr) {
  requireUserId(userId);
  return logServiceForVehicle(userId, vehicleId, serviceName, mileage, dateStr);
}

export async function listVehicleServiceHistory(userId, vehicleId) {
  requireUserId(userId);
  return listServiceLogsByVehicle(userId, vehicleId);
}

export async function listVehicleServices(userId, vehicleId) {
  requireUserId(userId);
  return getVehicleServices(userId, vehicleId);
}
