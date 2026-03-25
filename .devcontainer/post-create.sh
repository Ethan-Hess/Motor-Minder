#!/usr/bin/env bash
set -euo pipefail

echo "[devcontainer] Verifying toolchain..."
node --version
npm --version
python3 --version
java -version
firebase --version

java_major="$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | awk -F. '{print $1}')"
if [ -z "$java_major" ] || [ "$java_major" -lt 21 ]; then
  echo "[devcontainer] Warning: Java 21+ is required for firebase emulators."
  echo "[devcontainer] Current Java version appears to be: ${java_major:-unknown}"
fi

echo "[devcontainer] Installing Python dependencies if present..."
if ! python3 -m pip install --user --upgrade pip --break-system-packages; then
  echo "[devcontainer] Warning: pip upgrade skipped (externally managed Python environment)"
fi
if [ -f requirements.txt ]; then
  if ! python3 -m pip install --user -r requirements.txt --break-system-packages; then
    echo "[devcontainer] Warning: requirements install failed; continuing setup"
  fi
fi

echo "[devcontainer] Installing Node dependencies if package.json exists..."
if [ -f package.json ]; then
  echo "[devcontainer] Found package.json at repo root"
  npm install
else
  frontend_dir=""
  for candidate in motorminder-web web app frontend client; do
    if [ -f "$candidate/package.json" ]; then
      frontend_dir="$candidate"
      break
    fi
  done

  if [ -n "$frontend_dir" ]; then
    echo "[devcontainer] Found package.json in ./$frontend_dir"
    npm --prefix "$frontend_dir" install
  else
    echo "[devcontainer] No package.json found at root or common frontend paths; skipping npm install"
  fi
fi

echo "[devcontainer] Setup complete."
