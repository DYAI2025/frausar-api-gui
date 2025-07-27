#!/bin/zsh
# One-Click Starter für die FRAUSAR GUI

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Hauptverzeichnis des Projekts (eine Ebene über _STARTING_)
cd "$SCRIPT_DIR/.."

# Führt das Python-Skript der GUI aus
python3 Marker_assist_bot/frausar_gui.py 