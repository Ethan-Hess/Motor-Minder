# MotorMinder Web

React + Vite frontend for MotorMinder vehicle maintenance tracker.

## Quick Start

### Prerequisites

- Node.js 20+ (check with `node --version`)
- Java 21+ (check with `java -version`) — required for Firebase emulator runtime
- Firebase CLI (`firebase --version`)

### Setup (First Time Only)

1. **Navigate to the web directory:**

   ```bash
   cd /workspaces/The-Backlog-Blackhole/web
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **No Firebase config swapping needed for local dev.** Use the npm scripts below to choose emulator or live mode.

### Running the App Locally

**Emulator mode (recommended for development):**

```bash
cd The-Backlog-Blackhole/web
npm run dev:emulators
```

This starts Firebase emulators and Vite together in one command.

Expected output includes:

```
✔  All emulators ready! It is now safe to connect your app.
│ i  View Emulator UI at http://127.0.0.1:4000/
```

```
  VITE v6.2.1  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

**Live Firebase mode (no emulators):**

```bash
cd The-Backlog-Blackhole/web
npm run dev
```

### Access the App

1. **Web App:** Open `http://localhost:5173` in your browser
2. **Emulator UI:** View Firestore data at `http://127.0.0.1:4000/firestore`

### Seed Test Data (Optional)

Load the sample vehicles from the MVP into the emulator:

**Terminal 3 — Seed emulator data:**

```bash
cd The-Backlog-Blackhole/web
npm run seed-emulator
```

Expected output:

```
📡 Connecting to Firestore emulator...
📚 Loaded 3 vehicles from vehicles.json
  ✓ Added: 2017 Toyota Camry (68500 mi)
  ✓ Added: 2020 Honda Civic (32000 mi)
  ✓ Added: 2010 Chevrolet Cobalt (125000 mi)

✅ Emulator seeded successfully!
```

This loads 3 sample vehicles with service history from `../mvp/vehicles.json`. The emulator will clear this data when restarted, so re-run the seed command after each emulator restart if you want fresh test data.

Note: local Firestore rules allow unauthenticated read/write only for `users/dev-local-user/**` in the emulator to support this seed workflow. Authenticated users still use `request.auth.uid`-scoped access.

## Architecture

- `src/pages/`: Route-level UI components (View layer)
- `src/services/`: Application logic (Controller layer)
- `src/repositories/`: Firestore access wrappers (Data layer)
- `src/types/`: Domain model types and validators (Model layer)
- `src/lib/firebase.js`: Firebase SDK initialization with emulator auto-connection

## Testing

This project uses **Vitest** for frontend unit tests.

### Run tests

```bash
cd /workspaces/The-Backlog-Blackhole/web
npm test
```

Run in watch mode while developing:

```bash
cd /workspaces/The-Backlog-Blackhole/web
npm run test:watch
```

### Current test coverage

- `src/services/maintenanceService.test.js`
  - Verifies status computation for unknown, missing, due soon, overdue, mileage-only, time-only, and combined scenarios.
- `src/services/serviceIntervalService.test.js`
  - Verifies interval lookup for known/unknown services and interval list shape.
- `src/services/serviceLogService.test.js`
  - Verifies service-layer validation and delegation to repository functions.
- `src/services/mechanicService.test.js`
  - Verifies city/state matching behavior, normalization, and no-match cases.

### Recommended local validation sequence

```bash
cd /workspaces/The-Backlog-Blackhole/web
npm run lint
npm test
npm run build
```

## Using Services In Frontend

Frontend pages/components should call **service modules** in `src/services`.
Avoid calling repository modules directly from UI components.

### 1) Vehicle operations

Use `src/services/vehicleService.js` for list/get/add/edit/remove flows.

```js
import { addVehicle, listVehicles } from "../services/vehicleService.js";

const userId = auth.currentUser?.uid ?? "dev-local-user";
const vehicles = await listVehicles(userId);

await addVehicle(userId, {
  make: "Toyota",
  model: "Camry",
  year: 2018,
  currentMileage: 72000,
});
```

### 2) Service logging and history

Use `src/services/serviceLogService.js` to write logs and read history.

```js
import {
  logService,
  listVehicleServiceHistory,
  listVehicleServices,
} from "../services/serviceLogService.js";

const userId = auth.currentUser?.uid ?? "dev-local-user";

await logService(userId, vehicleId, "oil_change", 73500, "2026-03-26");

const history = await listVehicleServiceHistory(userId, vehicleId);
const latestByService = await listVehicleServices(userId, vehicleId);
```

### 3) Interval lookup + maintenance status

Use `src/services/serviceIntervalService.js` with `src/services/maintenanceService.js`.

```js
import { getIntervalForService } from "../services/serviceIntervalService.js";
import { getServiceStatusDetailed } from "../services/maintenanceService.js";

const interval = getIntervalForService("oil_change");
const status = getServiceStatusDetailed(
  vehicle.currentMileage,
  vehicle.lastService?.oil_change,
  interval,
  new Date(),
);

// status => { status, dueMiles, dueDate, overdueAmount, missing }
```

### 4) Mechanic lookup

Use `src/services/mechanicService.js` for list/search behavior.

```js
import {
  findMechanicByCityState,
  listMechanics,
} from "../services/mechanicService.js";

const allMechanics = await listMechanics();
const match = await findMechanicByCityState("Alpine", "UT");
```

### Error handling pattern

Service functions throw errors for invalid input or failed operations. Handle them in UI code:

```js
try {
  await logService(userId, vehicleId, serviceName, mileage, date);
} catch (error) {
  setError(error.message ?? "Operation failed");
}
```

## Development Tips

### Emulator Configuration

- Emulator hosts and ports are defined in `src/lib/firebase.js`
- Use `npm run dev:emulators` to run app + emulators together
- Use `npm run dev` to run the app against live Firebase by default
- Emulator mode is enabled by Vite mode (`vite --mode emulators`), not by env variables

### Firestore Emulator Data

- All data created in the emulator is cleared when the emulator restarts
- Use the Emulator UI (`http://127.0.0.1:4000/firestore`) to inspect collections and documents in real-time
- The app uses user-scoped paths: `users/{userId}/vehicles/{vehicleId}` and `users/{userId}/service_logs/{logId}`
- Mechanics lookup data is stored in top-level collection: `mechanics/{mechanicId}`

### Local Development User

- Currently using fallback user ID: `dev-local-user`
- All vehicles are stored under: `users/dev-local-user/vehicles/`
- Real Firebase Authentication will be integrated later

## Emulator Ports

| Service     | Host      | Port |
| ----------- | --------- | ---- |
| Firestore   | 127.0.0.1 | 8080 |
| Auth        | 127.0.0.1 | 9099 |
| Hosting     | 127.0.0.1 | 5000 |
| Emulator UI | 127.0.0.1 | 4000 |
