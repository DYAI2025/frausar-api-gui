#!/bin/zsh
# One-Click Starter für REPARIERTE Frausar GUI
# Marker werden SOFORT erstellt - keine Genehmigungsschleife

# Wechselt ins Marker_assist_bot Verzeichnis
cd "$(dirname "$0")/../Marker_assist_bot"

echo "🎯 Starte REPARIERTE Frausar GUI..."
echo ""

# Prüft ob Python verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

echo "✅ Python3 verfügbar"
echo ""

# Startet die GUI
echo "🚀 Starte Frausar GUI..."
echo ""
echo "Features:"
echo "  • Marker werden SOFORT erstellt"
echo "  • Keine Genehmigungsschleife"
echo "  • Copy-Paste funktioniert"
echo "  • YAML-Import funktioniert"
echo ""

python3 frausar_gui.py

echo ""
echo "👋 Frausar GUI beendet"
read -p "Drücken Sie Enter zum Schließen..." 