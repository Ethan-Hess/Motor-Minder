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
4. Run dev server
