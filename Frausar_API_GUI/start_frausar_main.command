#!/bin/zsh
# One-Click Starter für Frausar API GUI Hauptmenü
# Zentrale Anlaufstelle für alle Frausar-Funktionen

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

echo "🚀 Starte Frausar API GUI Hauptmenü..."
echo "Verzeichnis: $(pwd)"
echo ""

# Prüft ob Python verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nicht gefunden!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Prüft ob Abhängigkeiten installiert sind
if ! python3 -c "import tkinter, yaml" &> /dev/null; then
    echo "📦 Installiere Abhängigkeiten..."
    pip3 install pyyaml
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Startet das Hauptmenü
echo "🎯 Starte Frausar API GUI Hauptmenü..."
echo "Verfügbare Funktionen:"
echo "  🎯 Smart Marker-Erstellung"
echo "  🌐 Frausar AI-API"
echo "  🧪 Tests & Diagnose"
echo ""

# Wechselt ins Verzeichnis und startet die GUI
cd "$SCRIPT_DIR"
python3 main.py

# Falls das Skript beendet wird
echo ""
echo "👋 Frausar API GUI beendet"
read -p "Drücken Sie Enter zum Schließen..." 