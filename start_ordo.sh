#!/bin/bash

# OrDo Voice Agent Start-Skript
# Integriert Resonanz-Trichord Router mit Otto-System

echo "🧠 OrDo Voice Agent - Resonanz-Trichord Router Integration"
echo "=========================================================="

# Prüfe Python-Abhängigkeiten
echo "📦 Prüfe Python-Abhängigkeiten..."

# Erstelle requirements.txt falls nicht vorhanden
if [ ! -f "requirements_ordo.txt" ]; then
    cat > requirements_ordo.txt << EOF
ruamel.yaml
python-dotenv
SpeechRecognition
pyaudio
requests
websockets
pyttsx3
elevenlabs
EOF
    echo "✅ requirements_ordo.txt erstellt"
fi

# Installiere Abhängigkeiten
echo "📦 Installiere Abhängigkeiten..."
pip3 install -r requirements_ordo.txt

# Prüfe Ollama
echo "🔍 Prüfe Ollama-Service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama nicht erreichbar. Starte Ollama..."
    echo "💡 Führe 'ollama serve' in einem separaten Terminal aus"
    echo "💡 Oder installiere Ollama: https://ollama.ai"
fi

# Prüfe verfügbare Modelle
echo "🔍 Prüfe verfügbare Modelle..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama verfügbar"
    echo "📋 Verfügbare Modelle:"
    curl -s http://localhost:11434/api/tags | python3 -m json.tool | grep -E '"name"' | head -5
else
    echo "❌ Ollama nicht verfügbar"
fi

# Prüfe Konfigurationsdateien
echo "📋 Prüfe Konfigurationsdateien..."
if [ -f "resonanz_trichord_router.yaml" ]; then
    echo "✅ Router-Konfiguration gefunden"
else
    echo "❌ resonanz_trichord_router.yaml nicht gefunden"
    exit 1
fi

if [ -f "router.py" ]; then
    echo "✅ Router-Implementation gefunden"
else
    echo "❌ router.py nicht gefunden"
    exit 1
fi

if [ -f "ordo_voice_agent.py" ]; then
    echo "✅ Voice Agent gefunden"
else
    echo "❌ ordo_voice_agent.py nicht gefunden"
    exit 1
fi

# Prüfe Umgebungsvariablen
echo "🔧 Prüfe Umgebungsvariablen..."
if [ -f ".env" ]; then
    echo "✅ .env Datei gefunden"
    source .env
else
    echo "⚠️  .env Datei nicht gefunden"
fi

# Starte Voice Agent
echo "🚀 Starte OrDo Voice Agent..."
echo "=========================================================="
python3 ordo_voice_agent.py 