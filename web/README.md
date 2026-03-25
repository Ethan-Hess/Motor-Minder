# MotorMinder Web

React + Vite frontend scaffold for MotorMinder migration.

## Structure

- `src/pages`: route-level UI (View layer)
- `src/services`: application logic (Controller layer)
- `src/repositories`: Firestore access wrappers (Data layer)
- `src/types`: domain model types (Model layer)
- `src/lib/firebase.js`: Firebase initialization

## Local setup

1. Copy `.env.local.example` to `.env.local`
2. Fill Firebase config values
3. Install dependencies
4. Start Firebase emulators from `web/`
5. Run Vite dev server

## Recommended emulator workflow

- Java 21+ is required by recent `firebase-tools` for emulator runtime.
- If using dev containers, rebuild the container after pulling latest `.devcontainer` updates.
- Keep `VITE_USE_FIREBASE_EMULATORS=true` in `.env.local` for local development.
- Start emulators using the local Firebase config in this folder.
- Use emulator ports from `firebase.json`:
  - Auth: `127.0.0.1:9099`
  - Firestore: `127.0.0.1:8080`
  - Hosting emulator: `127.0.0.1:5000`
  - Emulator UI: `127.0.0.1:4000`

### Expected behavior

- `src/lib/firebase.js` automatically connects Auth + Firestore to emulators when `VITE_USE_FIREBASE_EMULATORS=true`.
- Turning `VITE_USE_FIREBASE_EMULATORS=false` switches the app back to real Firebase services.
- `firebase login` is recommended; emulators can still run without login, but some features may be limited.
