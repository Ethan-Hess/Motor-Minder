# MotorMinder Web Setup Guide (Vite + React + Firebase)

This guide is the practical setup companion to `docs/migration_plan.md`.
It is designed for this exact repository and assumes you will run commands manually.

## 1) Target Folder Layout (Inside Current Repo)

Keep Python and web code side-by-side during migration:

```text
The-Backlog-Blackhole/
├── docs/
├── mvp/                  # existing Python CLI app
└── web/                  # new React + Vite app
```

Reason: both codebases can evolve in parallel while you validate parity.

## 2) Manual Setup Commands (Run Yourself)

From repository root:

```bash
npm create vite@latest web -- --template react-ts
cd web
npm install
npm install firebase react-router-dom
```

Optional dev dependencies:

```bash
npm install -D eslint prettier @types/node
```

## 3) Recommended Web App Structure

Inside `web/src/`:

```text
src/
├── app/
│   └── router.tsx
├── components/
├── features/
│   ├── vehicles/
│   ├── services/
│   └── mechanics/
├── lib/
│   └── firebase.ts
├── pages/
│   ├── DashboardPage.tsx
│   ├── VehiclesPage.tsx
│   ├── LogServicePage.tsx
│   └── MechanicsPage.tsx
├── services/
│   ├── vehicleService.ts
│   └── maintenanceService.ts
├── types/
│   └── domain.ts
├── App.tsx
└── main.tsx
```

## 4) Starter File Templates

### 4.1 `web/.env.local`

```bash
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
```

### 4.2 `web/src/lib/firebase.ts`

```ts
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
```

### 4.3 `web/src/types/domain.ts`

```ts
export type ServiceName =
  | "oil_change"
  | "air_intake_filter"
  | "cabin_air_filter"
  | "tire_rotation"
  | "transmission_fluid"
  | "brake_pads_inspection"
  | "battery"
  | "coolant_flush"
  | "spark_plugs"
  | "brake_fluid";

export interface ServiceRecord {
  mileage: number;
  date: string; // ISO yyyy-mm-dd
}

export interface Vehicle {
  id: string;
  make: string;
  model: string;
  year: number;
  currentMileage: number;
  userId: string;
  lastService: Partial<Record<ServiceName, ServiceRecord>>;
}
```

### 4.4 `web/src/services/maintenanceService.ts`

```ts
import type { ServiceRecord } from "../types/domain";

export type ServiceStatus = "OK" | "Due Soon" | "Overdue" | "Unknown";

type Interval = {
  miles?: [number, number];
  months?: [number, number];
  years?: [number, number];
};

export function getServiceStatus(
  currentMileage: number,
  lastService: ServiceRecord | undefined,
  interval: Interval | undefined,
): ServiceStatus {
  if (!interval) return "Unknown";
  if (!lastService) return "Overdue";

  let status: ServiceStatus = "OK";
  const milesSince = currentMileage - lastService.mileage;

  if (interval.miles) {
    const [dueSoon, overdue] = interval.miles;
    if (milesSince >= overdue) return "Overdue";
    if (milesSince >= dueSoon) status = "Due Soon";
  }

  return status;
}
```

### 4.5 `web/src/App.tsx`

```tsx
function App() {
  return (
    <main style={{ fontFamily: "system-ui", padding: 16 }}>
      <h1>MotorMinder Web</h1>
      <p>Vite + React + Firebase setup is ready.</p>
    </main>
  );
}

export default App;
```

## 5) Firebase Initialization (Manual)

From `web/` run Firebase init and select:

- Hosting
- Firestore
- Functions
- Emulators (Auth + Firestore + Hosting + Functions)

Then verify:

- `firebase.json` is created
- `.firebaserc` is created
- Firestore rules and indexes files are present

## 6) Mapping Existing Python Models -> Web Types

- `Vehicle` (`mvp/models.py`) -> `Vehicle` (`web/src/types/domain.ts`)
- `ServiceRecord` (`mvp/models.py`) -> `ServiceRecord` (`web/src/types/domain.ts`)
- `ServiceName` enum (`mvp/models.py`) -> string union `ServiceName`
- Controller logic (`mvp/controller.py`) -> `web/src/services/maintenanceService.ts`

## 7) First Milestone Definition (Recommended)

Complete this before feature expansion:

1. App boots in browser from `web/`
2. Firebase config loads from `.env.local`
3. Firestore client initializes without runtime errors
4. One hardcoded `Vehicle` renders in UI
5. `getServiceStatus` returns expected values for one test case each: `OK`, `Due Soon`, `Overdue`

## 8) Quick Validation Checklist

- `web/` exists and dependencies are installed
- `.env.local` has all six Firebase variables
- `web/src/lib/firebase.ts` exports `auth` and `db`
- Domain types compile
- App renders startup message

If you want, the next step can be a minimal parity slice: Vehicle List + Add Vehicle + Log Service + Dashboard status in React using Firestore emulator data.
