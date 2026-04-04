import {
  collection,
  doc,
  getDoc,
  getDocs,
  runTransaction,
  serverTimestamp,
} from 'firebase/firestore';
import { db } from '../lib/firebase.js';
import { createServiceRecord, isKnownServiceName } from '../types/domain.js';

function userVehicleDoc(userId, vehicleId) {
  return doc(db, 'users', userId, 'vehicles', vehicleId);
}

function userServiceLogsCollection(userId) {
  return collection(db, 'users', userId, 'service_logs');
}

function requireIdentifiers(userId, vehicleId) {
  if (!userId) {
    throw new Error('userId is required for service operations');
  }

  if (!vehicleId) {
    throw new Error('vehicleId is required for service operations');
  }
}

function normalizeDateInput(dateStr) {
  if (typeof dateStr === 'string' && dateStr.trim()) {
    return dateStr;
  }

  return new Date().toISOString().slice(0, 10);
}

export async function logServiceForVehicle(userId, vehicleId, serviceName, mileage, dateStr) {
  requireIdentifiers(userId, vehicleId);

  if (!isKnownServiceName(serviceName)) {
    throw new Error(`Unknown service name: ${serviceName}`);
  }

  const normalizedMileage = Number.isFinite(mileage)
    ? mileage
    : Number.parseInt(mileage ?? 0, 10);

  if (!Number.isFinite(normalizedMileage) || normalizedMileage < 0) {
    throw new Error('mileage must be a non-negative number');
  }

  const normalizedDate = normalizeDateInput(dateStr);
  const nextRecord = createServiceRecord({ mileage: normalizedMileage, date: normalizedDate });

  return runTransaction(db, async (transaction) => {
    const vehicleRef = userVehicleDoc(userId, vehicleId);
    const vehicleSnapshot = await transaction.get(vehicleRef);

    if (!vehicleSnapshot.exists()) {
      throw new Error('Vehicle not found');
    }

    const vehicleData = vehicleSnapshot.data();
    const currentMileage = Number.parseInt(vehicleData.current_mileage ?? 0, 10);
    const nextMileage = Number.isFinite(currentMileage)
      ? Math.max(currentMileage, nextRecord.mileage)
      : nextRecord.mileage;

    const nextLastService = {
      ...(vehicleData.last_service ?? {}),
      [serviceName]: nextRecord,
    };

    const serviceLogRef = doc(userServiceLogsCollection(userId));

    transaction.update(vehicleRef, {
      current_mileage: nextMileage,
      last_service: nextLastService,
      updatedAt: serverTimestamp(),
    });

    transaction.set(serviceLogRef, {
      vehicleId,
      serviceName,
      mileage: nextRecord.mileage,
      date: nextRecord.date,
      createdAt: serverTimestamp(),
    });

    return {
      id: serviceLogRef.id,
      vehicleId,
      serviceName,
      mileage: nextRecord.mileage,
      date: nextRecord.date,
    };
  });
}

export async function listServiceLogsByVehicle(userId, vehicleId) {
  requireIdentifiers(userId, vehicleId);

  const snapshot = await getDocs(userServiceLogsCollection(userId));
  const logs = snapshot.docs
    .map((serviceLogDoc) => ({ id: serviceLogDoc.id, ...serviceLogDoc.data() }))
    .filter((serviceLog) => serviceLog.vehicleId === vehicleId)
    .sort((left, right) => {
      if (left.date === right.date) {
        return 0;
      }

      return left.date < right.date ? 1 : -1;
    });

  return logs.map((serviceLog) => ({
    id: serviceLog.id,
    vehicleId: serviceLog.vehicleId,
    serviceName: serviceLog.serviceName,
    ...createServiceRecord(serviceLog),
  }));
}

export async function getVehicleServices(userId, vehicleId) {
  requireIdentifiers(userId, vehicleId);

  const vehicleSnapshot = await getDoc(userVehicleDoc(userId, vehicleId));

  if (!vehicleSnapshot.exists()) {
    return {};
  }

  const vehicleData = vehicleSnapshot.data();
  const lastService = vehicleData.last_service ?? {};
  const serviceEntries = Object.entries(lastService).map(([serviceName, serviceRecord]) => [
    serviceName,
    createServiceRecord(serviceRecord),
  ]);

  return Object.fromEntries(serviceEntries);
}
