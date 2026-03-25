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

3. **The `.env` file is already configured for local development.** It uses dummy Firebase credentials that work with the local emulator. No action needed.

### Running the App Locally

**Terminal 1 — Start Firebase emulators:**

```bash
cd /workspaces/The-Backlog-Blackhole/web
firebase emulators:start --project motor-minder
```

Expected output includes:

```
✔  All emulators ready! It is now safe to connect your app.
│ i  View Emulator UI at http://127.0.0.1:4000/
```

**Terminal 2 — Start Vite dev server:**

```bash
cd /workspaces/The-Backlog-Blackhole/web
npm run dev
```

Expected output includes:

```
  VITE v6.2.1  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

### Access the App

1. **Web App:** Open `http://localhost:5173` in your browser
2. **Emulator UI:** View Firestore data at `http://127.0.0.1:4000/firestore`

### Seed Test Data (Optional)

Load the sample vehicles from the MVP into the emulator:

**Terminal 3 — Seed emulator data:**

```bash
cd /workspaces/The-Backlog-Blackhole/web
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

## Development Tips

### Emulator Configuration

- Emulator hosts and ports are configured in `firebase.json` and `.env`
- The app automatically connects to emulators when `VITE_USE_FIREBASE_EMULATORS=true` in `.env`
- To switch to production Firebase, set `VITE_USE_FIREBASE_EMULATORS=false` and provide real Firebase config values in `.env`

### Firestore Emulator Data

- All data created in the emulator is cleared when the emulator restarts
- Use the Emulator UI (`http://127.0.0.1:4000/firestore`) to inspect collections and documents in real-time
- The app uses user-scoped paths: `users/{userId}/vehicles/{vehicleId}`

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
