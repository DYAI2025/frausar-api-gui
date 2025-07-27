#!/bin/zsh
# One-Click Starter für die NEUE Frausar API GUI

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Hauptverzeichnis des Projekts (eine Ebene über _STARTING_)
cd "$SCRIPT_DIR/.."

# Führt das Python-Skript der NEUEN GUI aus
python3 Frausar_API_GUI/main.py 