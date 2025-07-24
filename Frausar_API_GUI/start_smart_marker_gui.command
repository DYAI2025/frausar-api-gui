#!/bin/zsh
# One-Click Starter für Smart Marker-Erstellung
# Benutzerfreundliche GUI mit automatischer Fehlerbehebung

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

echo "🎯 Starte Smart Marker-Erstellung..."
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

# Startet die Smart Marker GUI
echo "🚀 Starte Smart Marker-Erstellung..."
echo "Features:"
echo "  ✅ Automatische YAML-Korrektur"
echo "  ✅ Beliebige Text-Formate"
echo "  ✅ Klare Fehlermeldungen"
echo "  ✅ Sofortige Marker-Erstellung"
echo ""

# Wechselt ins Verzeichnis und startet die GUI
cd "$SCRIPT_DIR"
python3 smart_marker_gui.py

# Falls das Skript beendet wird
echo ""
echo "👋 Smart Marker-Erstellung beendet"
read -p "Drücken Sie Enter zum Schließen..." 