import {
  addDoc,
  collection,
  deleteDoc,
  doc,
  getDoc,
  getDocs,
  setDoc,
} from 'firebase/firestore';
import { db } from '../lib/firebase.js';
import { toMvpVehicleFromWeb, toWebVehicleFromMvp } from '../types/domain.js';

function userVehiclesCollection(userId) {
  return collection(db, 'users', userId, 'vehicles');
}

function userVehicleDoc(userId, vehicleId) {
  return doc(db, 'users', userId, 'vehicles', vehicleId);
}

export async function fetchVehiclesByUser(userId) {
  const snapshot = await getDocs(userVehiclesCollection(userId));

  return snapshot.docs.map((vehicleDoc) =>
    toWebVehicleFromMvp(vehicleDoc.data(), { id: vehicleDoc.id, userId }),
  );
}

export async function fetchVehicleById(userId, vehicleId) {
  const snapshot = await getDoc(userVehicleDoc(userId, vehicleId));

  if (!snapshot.exists()) {
    return null;
  }

  return toWebVehicleFromMvp(snapshot.data(), { id: snapshot.id, userId });
}

export async function createVehicle(userId, vehicle) {
  const mvpShapeVehicle = toMvpVehicleFromWeb({ ...vehicle, userId });
  const created = await addDoc(userVehiclesCollection(userId), mvpShapeVehicle);

  return {
    ...vehicle,
    id: created.id,
    userId,
  };
}

export async function updateVehicle(userId, vehicleId, vehicle) {
  const mvpShapeVehicle = toMvpVehicleFromWeb({ ...vehicle, id: vehicleId, userId });

  await setDoc(userVehicleDoc(userId, vehicleId), mvpShapeVehicle, { merge: true });

  return {
    ...vehicle,
    id: vehicleId,
    userId,
  };
}

export async function deleteVehicle(userId, vehicleId) {
  await deleteDoc(userVehicleDoc(userId, vehicleId));
}
