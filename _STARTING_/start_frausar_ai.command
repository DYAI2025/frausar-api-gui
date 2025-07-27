#!/bin/zsh
# One-Click Starter für die Frausar AI-Integration
# Frausar_API_GUI - AI-gestützte Datenanalyse und -bereinigung

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Hauptverzeichnis des Projekts
cd "$SCRIPT_DIR/.."

echo "🚀 Starte Frausar AI-Integration..."
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
echo "ReDoc: http://localhost:8000/redoc"
echo ""
echo "Verfügbare Endpunkte:"
echo "  POST /upload - Datei hochladen"
echo "  POST /clean - Datenbereinigung starten"
echo "  GET /result - Ergebnisse abrufen"
echo "  GET /status - System-Status"
echo ""
echo "Drücken Sie Ctrl+C zum Beenden"
echo ""

# Wechselt ins Frausar_API_GUI Verzeichnis und startet die API
cd Frausar_API_GUI
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# Falls das Skript beendet wird
echo ""
echo "👋 Frausar AI-Integration beendet"
read -p "Drücken Sie Enter zum Schließen..." 