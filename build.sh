#!/usr/bin/env bash
# Build the desktop app with PyInstaller. Output goes to dist/.
set -euo pipefail
cd "$(dirname "$0")"

# --add-data "ui.html:." copies ui.html into the app; desktop.py finds it
# through sys._MEIPASS when the app is running frozen.
python -m PyInstaller \
    --noconfirm \
    --clean \
    --windowed \
    --name MathCSNotes \
    --add-data "ui.html:." \
    desktop.py

echo "Built: dist/MathCSNotes (on macOS: dist/MathCSNotes.app)"
