#!/usr/bin/env sh
# Wrapper to run the Tkinter app locally or within container shells.

set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

exec python3 main.py
