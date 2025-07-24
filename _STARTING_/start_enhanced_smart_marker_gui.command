#!/bin/zsh
# One-Click Starter für die Enhanced Smart Marker GUI
# Vollständige GUI mit allen Features: Batch-Import, Statistiken, Templates

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Hauptverzeichnis des Projekts
cd "$SCRIPT_DIR/.."

echo "🎯 Starte Enhanced Smart Marker GUI..."
echo "Verzeichnis: $(pwd)"
echo ""

# Prüft Python-Version
echo "🐍 Prüfe Python-Version..."
if ! python3 --version &> /dev/null; then
    echo "❌ Python 3 nicht gefunden!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION OK"
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

# Prüft ob requirements installiert sind
if [ ! -f "$FRAUSAR_DIR/requirements.txt" ]; then
    echo "❌ requirements.txt nicht gefunden!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Installiert Abhängigkeiten falls nötig
echo "📦 Prüfe Abhängigkeiten..."
if ! python3 -c "import tkinter, yaml, pandas" &> /dev/null; then
    echo "📥 Installiere Abhängigkeiten..."
    pip3 install -r "$FRAUSAR_DIR/requirements.txt"
    if [ $? -ne 0 ]; then
        echo "❌ Fehler beim Installieren der Abhängigkeiten!"
        read -p "Drücken Sie Enter zum Beenden..."
        exit 1
    fi
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Startet die Enhanced Smart Marker GUI
echo "🎯 Starte Enhanced Smart Marker GUI..."
echo "Features:"
echo "  🔍 Live-Suche mit Fuzzy-Matching"
echo "  📋 Marker-Übersicht"
echo "  🔗 Import Bridge Integration"
echo "  📦 Batch-Import-Funktionen"
echo "  📊 Erweiterte Statistiken"
echo "  📋 Marker-Templates"
echo "  ✏️ Inline-Editor"
echo ""
echo "Verfügbare Buttons:"
echo "  🔗 Import Bridge - Verwendet Import Bridge für Marker-Erstellung"
echo "  📁 Datei importieren - Importiert Marker aus externen Dateien"
echo "  📦 Batch-Import - Massenverarbeitung mehrerer Dateien"
echo "  📊 Erweiterte Statistiken - Umfassende Analytics"
echo "  📋 Marker-Templates - Vorlagen für Marker-Erstellung"
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