#!/bin/zsh
# One-Click Starter für Enhanced Smart Marker GUI
# Multi-Format-Support, Live-Suche und Marker-Übersicht

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

echo "🎯 Starte Enhanced Smart Marker GUI..."
echo "Verzeichnis: $(pwd)"
echo ""

# Prüft ob Python verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nicht gefunden!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Prüft ob Abhängigkeiten installiert sind
if ! python3 -c "import yaml, tkinter" &> /dev/null; then
    echo "📦 Installiere Abhängigkeiten..."
    pip3 install pyyaml
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Startet die Enhanced Smart Marker GUI
echo "🚀 Starte Enhanced Smart Marker GUI..."
echo "Features:"
echo "  ✅ Multi-Format-Support (.txt, .py, .json, .yaml, .yml)"
echo "  ✅ Live-Suche mit Fuzzy-Matching"
echo "  ✅ Marker-Übersicht parallel zur Eingabe"
echo "  ✅ Icon-basierte Kategorisierung"
echo "  ✅ Mehrere Marker auf einmal (getrennt durch '---')"
echo "  ✅ Automatische ID-Erkennung"
echo "  ✅ Inline-Editor für Marker-Bearbeitung"
echo ""

# Wechselt ins Verzeichnis und startet die GUI
cd "$SCRIPT_DIR"
python3 enhanced_smart_marker_gui.py

# Falls das Skript beendet wird
echo ""
echo "👋 Enhanced Smart Marker GUI beendet"
read -p "Drücken Sie Enter zum Schließen..." 