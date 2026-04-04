import { getServiceInterval, listServiceIntervals } from '../types/domain.js';

export function getIntervalForService(serviceName) {
  return getServiceInterval(serviceName);
}

export function getAllServiceIntervals() {
  return listServiceIntervals();
}
