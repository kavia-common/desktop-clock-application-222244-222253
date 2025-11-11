#!/usr/bin/env sh
# Wrapper to run the Tkinter app locally or within container shells.

set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ "${HEALTHCHECK_ONLY:-0}" = "1" ]; then
  echo "[run] Health check mode enabled. DISPLAY=${DISPLAY:-<unset>}"
  if command -v python3 >/dev/null 2>&1 && [ -f "main.py" ]; then
    echo "[run] python3 and main.py present. Exiting 0."
    exit 0
  else
    echo "[run][error] Missing python3 or main.py."
    exit 1
  fi
fi

exec python3 main.py
