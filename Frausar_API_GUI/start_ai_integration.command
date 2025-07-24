#!/bin/zsh
# One-Click Starter für die Frausar AI-Integration

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Hauptverzeichnis des Projekts (eine Ebene über Frausar_API_GUI)
cd "$SCRIPT_DIR/.."

# Prüft ob Python 3.10+ verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "Bitte installieren Sie Python 3.10 oder höher."
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Prüft Python-Version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION gefunden, aber $REQUIRED_VERSION+ erforderlich!"
    echo "Bitte aktualisieren Sie Python auf Version 3.10 oder höher."
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

echo "🚀 Starte Frausar AI-Integration..."
echo "Python Version: $PYTHON_VERSION"
echo "Verzeichnis: $(pwd)"
echo ""

# Prüft ob requirements installiert sind
if [ ! -f "Frausar_API_GUI/requirements_ai.txt" ]; then
    echo "❌ requirements_ai.txt nicht gefunden!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Installiert Abhängigkeiten falls nötig
echo "📦 Prüfe Abhängigkeiten..."
if ! python3 -c "import fastapi, pandas, uvicorn" &> /dev/null; then
    echo "📥 Installiere Abhängigkeiten..."
    pip3 install -r Frausar_API_GUI/requirements_ai.txt
    if [ $? -ne 0 ]; then
        echo "❌ Fehler beim Installieren der Abhängigkeiten!"
        read -p "Drücken Sie Enter zum Beenden..."
        exit 1
    fi
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Startet die AI-Integration
echo "🎯 Starte Frausar AI-Integration..."
echo "API wird verfügbar unter: http://localhost:8000"
echo "API-Docs: http://localhost:8000/docs"
echo ""
echo "Drücken Sie Ctrl+C zum Beenden"
echo ""

# Führt das Hauptskript aus
python3 Frausar_API_GUI/main_ai_integration.py

# Falls das Skript beendet wird
echo ""
echo "👋 Frausar AI-Integration beendet"
read -p "Drücken Sie Enter zum Schließen..." 