#!/bin/zsh
# One-Click Starter für Frausar AI-Integration Tests
# Automatisierte Tests für alle Komponenten

# Ermittelt das Verzeichnis, in dem das Skript liegt
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Wechselt in das Hauptverzeichnis des Projekts
cd "$SCRIPT_DIR/.."

echo "🧪 Starte Frausar AI-Integration Tests..."
echo ""

# Prüft ob das Hauptsystem läuft
echo "📡 Prüfe API-Verfügbarkeit..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API läuft bereits"
else
    echo "⚠️  API läuft nicht - starte im Hintergrund..."
    echo "   (API wird automatisch gestartet und nach Tests beendet)"
    
    # Startet API im Hintergrund
    cd Frausar_API_GUI
    python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &
    API_PID=$!
    cd ..
    
    # Wartet bis API verfügbar ist
    echo "⏳ Warte auf API-Start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            echo "✅ API gestartet"
            break
        fi
        sleep 1
    done
fi

echo ""
echo "🎯 Führe Tests aus..."
echo ""

# Führt Tests direkt aus (ohne interaktives Menü)
cd Frausar_API_GUI
python3 test_ai_integration.py

# Beendet API falls wir sie gestartet haben
if [ ! -z "$API_PID" ]; then
    echo ""
    echo "🛑 Beende API..."
    kill $API_PID 2>/dev/null
fi

echo ""
echo "✅ Tests abgeschlossen"
read -p "Drücken Sie Enter zum Schließen..." 