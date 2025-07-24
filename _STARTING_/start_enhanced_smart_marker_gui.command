#!/bin/zsh
# One-Click Starter für die Enhanced Smart Marker GUI
# Frausar_API_GUI - Enhanced Smart Marker GUI mit Import Bridge Integration

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Hauptverzeichnis des Projekts
cd "$SCRIPT_DIR/.."

echo "🎯 Starte Enhanced Smart Marker GUI..."
echo "Verzeichnis: $(pwd)"
echo ""

# Findet das Frausar_API_GUI Verzeichnis
FRAUSAR_DIR=""
if [ -d "Frausar_API_GUI" ]; then
    FRAUSAR_DIR="Frausar_API_GUI"
elif [ -d "/Users/benjaminpoersch/claude_curser/Frausar_API_GUI" ]; then
    FRAUSAR_DIR="/Users/benjaminpoersch/claude_curser/Frausar_API_GUI"
else
    echo "❌ Frausar_API_GUI Verzeichnis nicht gefunden!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Prüft ob Python verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Prüft Python-Version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION oder höher erforderlich! (Gefunden: $PYTHON_VERSION)"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION OK"
echo ""

# Prüft ob die Enhanced GUI existiert
if [ ! -f "$FRAUSAR_DIR/enhanced_smart_marker_gui.py" ]; then
    echo "❌ enhanced_smart_marker_gui.py nicht gefunden!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Prüft Abhängigkeiten
echo "📦 Prüfe Abhängigkeiten..."
MISSING_DEPS=()

# Prüft tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    MISSING_DEPS+=("tkinter")
fi

# Prüft yaml
if ! python3 -c "import yaml" &> /dev/null; then
    MISSING_DEPS+=("pyyaml")
fi

# Prüft ruamel.yaml
if ! python3 -c "import ruamel.yaml" &> /dev/null; then
    MISSING_DEPS+=("ruamel.yaml")
fi

# Prüft pydantic
if ! python3 -c "import pydantic" &> /dev/null; then
    MISSING_DEPS+=("pydantic")
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "⚠️ Fehlende Abhängigkeiten: ${MISSING_DEPS[*]}"
    echo "📥 Installiere Abhängigkeiten..."
    
    for dep in "${MISSING_DEPS[@]}"; do
        case $dep in
            "tkinter")
                echo "   tkinter ist normalerweise in Python enthalten"
                ;;
            "pyyaml")
                pip3 install pyyaml
                ;;
            "ruamel.yaml")
                pip3 install ruamel.yaml
                ;;
            "pydantic")
                pip3 install pydantic
                ;;
        esac
    done
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Startet die Enhanced Smart Marker GUI
echo "🎯 Starte Enhanced Smart Marker GUI..."
echo ""
echo "Features:"
echo "  🔍 Live-Suche mit Fuzzy-Matching"
echo "  📋 Marker-Übersicht"
echo "  🔗 Import Bridge Integration"
echo "  📊 Detaillierte Statistiken"
echo "  ✏️ Inline-Editor"
echo ""
echo "Verfügbare Buttons:"
echo "  🔗 Import Bridge - Verwendet Import Bridge für Marker-Erstellung"
echo "  📁 Datei importieren - Importiert Marker aus externen Dateien"
echo "  🚀 Alle Marker erstellen - Erstellt Marker mit Standard-Methode"
echo "  🗑️ Text löschen - Löscht Eingabe-Text"
echo "  🎯 Demo-Marker laden - Lädt Demo-Marker"
echo ""
echo "Drücken Sie Ctrl+C zum Beenden"
echo ""

# Wechselt ins Frausar_API_GUI Verzeichnis und startet die GUI
cd "$FRAUSAR_DIR"
python3 enhanced_smart_marker_gui.py

# Falls das Skript beendet wird
echo ""
echo "👋 Enhanced Smart Marker GUI beendet"
read -p "Drücken Sie Enter zum Schließen..." 