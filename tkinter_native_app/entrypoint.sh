#!/usr/bin/env sh
# A simple, safe entrypoint for the Tkinter Ocean Clock app.
# - Runs the Python Tkinter app.
# - Provides clear logs.
# - Avoids reliance on non-existent /usr/local/bin/start_vnc.
# - Uses POSIX sh to prevent syntax errors due to bash-isms.

set -eu

APP_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$APP_DIR"

echo "[entrypoint] Starting Ocean Clock (Tkinter) from: $APP_DIR"
echo "[entrypoint] Python version: $(python3 --version 2>/dev/null || echo 'python3 not found')"

if [ ! -f "main.py" ]; then
  echo "[entrypoint][error] main.py not found in $APP_DIR"
  exit 1
fi

# Note: Tkinter requires a GUI environment (DISPLAY). In CI/headless it may fail.
# The app itself exits with code 1 if Tk cannot initialize; we log it for clarity.
echo "[entrypoint] DISPLAY=${DISPLAY:-<unset>}"
echo "[entrypoint] Launching: python3 main.py"

# Execute and forward exit code
python3 main.py || {
  code=$?
  echo "[entrypoint][warn] Application exited with status $code (likely due to headless environment if DISPLAY is unset)."
  exit $code
}
