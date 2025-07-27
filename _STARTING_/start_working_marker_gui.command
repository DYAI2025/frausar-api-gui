#!/bin/zsh
# One-Click Starter für FUNKTIONALE Marker-Erstellung

# Wechselt ins Frausar_API_GUI Verzeichnis
cd "$(dirname "$0")/../Frausar_API_GUI"

echo "🎯 Starte FUNKTIONALE Marker-Erstellung..."
echo ""

# Prüft ob Python verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

# Prüft ob PyYAML installiert ist
if ! python3 -c "import yaml" &> /dev/null; then
    echo "📦 Installiere PyYAML..."
    pip3 install pyyaml
    if [ $? -ne 0 ]; then
        echo "❌ Fehler beim Installieren von PyYAML!"
        read -p "Drücken Sie Enter zum Beenden..."
        exit 1
    fi
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Startet die GUI
echo "🚀 Starte Marker-Erstellung..."
echo ""
echo "Anleitung:"
echo "1. Text in das Feld einfügen"
echo "2. 'Marker erstellen' klicken"
echo "3. Fertig!"
echo ""

python3 working_marker_gui.py

echo ""
echo "👋 Marker-Erstellung beendet"
read -p "Drücken Sie Enter zum Schließen..." 