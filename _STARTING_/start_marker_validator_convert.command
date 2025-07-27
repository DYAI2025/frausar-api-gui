#!/bin/zsh
# One-Click Starter für Marker Validator Convert
# GUI-basierte Marker-Validierung und -Konvertierung

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Hauptverzeichnis des Projekts
cd "$SCRIPT_DIR/.."

echo "🔧 Starte Marker Validator Convert..."
echo "Verzeichnis: $(pwd)"
echo ""

# Prüft ob Node.js verfügbar ist
if ! command -v node &> /dev/null; then
    echo "❌ Node.js ist nicht installiert!"
    echo "Bitte installieren Sie Node.js von https://nodejs.org/"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION OK"
echo ""

# Wechselt ins Marker_validator_convert Verzeichnis
if [ ! -d "Marker_validator_convert" ]; then
    echo "❌ Marker_validator_convert Verzeichnis nicht gefunden!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

cd Marker_validator_convert

# Prüft ob pnpm verfügbar ist
if ! command -v pnpm &> /dev/null; then
    echo "📦 Installiere pnpm..."
    npm install -g pnpm
    if [ $? -ne 0 ]; then
        echo "❌ Fehler beim Installieren von pnpm!"
        read -p "Drücken Sie Enter zum Beenden..."
        exit 1
    fi
fi

echo "✅ pnpm verfügbar"
echo ""

# Installiert Abhängigkeiten falls nötig
if [ ! -d "node_modules" ]; then
    echo "📦 Installiere Abhängigkeiten..."
    pnpm install
    if [ $? -ne 0 ]; then
        echo "❌ Fehler beim Installieren der Abhängigkeiten!"
        read -p "Drücken Sie Enter zum Beenden..."
        exit 1
    fi
fi

echo "✅ Abhängigkeiten OK"
echo ""

# Startet die GUI
echo "🎯 Starte Marker Validator Convert GUI..."
echo ""
echo "Features:"
echo "  🔍 Marker-Validierung"
echo "  🔄 Format-Konvertierung"
echo "  🛠️ Automatische Reparaturen"
echo "  📊 Batch-Verarbeitung"
echo "  🎨 Benutzerfreundliche GUI"
echo ""
echo "Verfügbare Funktionen:"
echo "  • Dateien per Drag & Drop hinzufügen"
echo "  • Validierung gegen Schema"
echo "  • Automatische Reparaturen"
echo "  • Format-Konvertierung (YAML ↔ JSON)"
echo "  • Batch-Verarbeitung mehrerer Dateien"
echo "  • Interaktive Reparatur-Vorschau"
echo ""
echo "GUI wird im Browser geöffnet..."
echo "Drücken Sie Ctrl+C zum Beenden"
echo ""

# Startet die Entwicklungsserver
echo "🚀 Starte Entwicklungsserver..."
pnpm dev

# Falls das Skript beendet wird
echo ""
echo "👋 Marker Validator Convert beendet"
read -p "Drücken Sie Enter zum Schließen..." 