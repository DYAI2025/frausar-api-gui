#!/bin/zsh
# One-Click Starter für die einfache Marker-Erstellungs-GUI
# Funktional und sofort einsatzbereit

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Verzeichnis
cd "$SCRIPT_DIR"

echo "🎯 Starte einfache Marker-Erstellungs-GUI..."
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
echo "🚀 Starte Marker-Erstellungs-GUI..."
echo ""
echo "Features:"
echo "  • Copy-Paste-Funktionalität (Ctrl+V)"
echo "  • Automatische Fehlerbehebung"
echo "  • Sofortige Verarbeitung"
echo "  • Demo-Marker zum Testen"
echo ""

python3 simple_marker_gui.py

echo ""
echo "👋 Marker-Erstellungs-GUI beendet"
read -p "Drücken Sie Enter zum Schließen..." 