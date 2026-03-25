#!/usr/bin/env node

/**
 * Seed the Firebase emulator with test data from ../mvp/vehicles.json
 * 
 * Usage:
 *   npm run seed-emulator
 * 
 * Make sure the emulator is running first:
 *   firebase emulators:start --project motor-minder
 */

import { initializeApp } from 'firebase/app';
import { connectFirestoreEmulator, getFirestore, collection, doc, setDoc } from 'firebase/firestore';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = resolve(__filename, '..');

const DEV_USER_ID = 'dev-local-user';
const EMULATOR_HOST = '127.0.0.1';
const EMULATOR_PORT = 8080;

// Initialize Firebase with dummy config (emulator doesn't validate)
const firebaseConfig = {
  apiKey: 'dummy-key',
  authDomain: 'motor-minder.firebaseapp.com',
  projectId: 'motor-minder',
  storageBucket: 'motor-minder.appspot.com',
  messagingSenderId: '123456789012',
  appId: '1:123456789012:web:dummy1234567890ab',
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Connect to emulator
connectFirestoreEmulator(db, EMULATOR_HOST, EMULATOR_PORT);

async function seedEmulator() {
  try {
    console.log(`📡 Connecting to Firestore emulator at ${EMULATOR_HOST}:${EMULATOR_PORT}...`);

    // Read vehicles from MVP data
    const vehiclesPath = resolve(__dirname, '../../mvp/vehicles.json');
    const vehiclesData = JSON.parse(readFileSync(vehiclesPath, 'utf-8'));

    console.log(`📚 Loaded ${vehiclesData.vehicles.length} vehicles from vehicles.json`);

    // Seed each vehicle
    const userVehiclesCollection = collection(db, 'users', DEV_USER_ID, 'vehicles');

    for (const vehicle of vehiclesData.vehicles) {
      const vehicleId = `${vehicle.make.toLowerCase()}-${vehicle.model.toLowerCase()}-${vehicle.year}`;
      const vehicleDocRef = doc(userVehiclesCollection, vehicleId);

      // Transform MVP format to storage format (snake_case)
      const vehicleData = {
        make: vehicle.make,
        model: vehicle.model,
        year: vehicle.year,
        current_mileage: vehicle.current_mileage,
        last_service: vehicle.last_service || {},
      };

      await setDoc(vehicleDocRef, vehicleData);
      console.log(`  ✓ Added: ${vehicle.year} ${vehicle.make} ${vehicle.model} (${vehicleData.current_mileage} mi)`);
    }

    console.log(`\n✅ Emulator seeded successfully!`);
    console.log(`📍 Data location: users/${DEV_USER_ID}/vehicles/`);
    console.log(`🔍 View in Emulator UI: http://127.0.0.1:4000/firestore\n`);

    process.exit(0);
  } catch (error) {
    console.error('❌ Error seeding emulator:', error.message);
    process.exit(1);
  }
}

seedEmulator();
