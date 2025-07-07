#!/bin/bash

# OrDo MLX Voice Agent Start-Skript
# Verwendet lokale MLX-Modelle aus LLM_LOCAL_MODELLS/

echo "🧠 OrDo MLX Voice Agent - Lokale MLX-Modelle"
echo "=========================================================="

# Prüfe Python-Abhängigkeiten
echo "📦 Prüfe Python-Abhängigkeiten..."

# Erstelle requirements.txt falls nicht vorhanden
if [ ! -f "requirements_ordo_mlx.txt" ]; then
    cat > requirements_ordo_mlx.txt << EOF
ruamel.yaml
python-dotenv
SpeechRecognition
pyaudio
requests
websockets
pyttsx3
elevenlabs
EOF
    echo "✅ requirements_ordo_mlx.txt erstellt"
fi

# Installiere Abhängigkeiten
echo "📦 Installiere Abhängigkeiten..."
pip3 install -r requirements_ordo_mlx.txt

# Prüfe lokale MLX-Modelle
echo "📁 Prüfe lokale MLX-Modelle..."
if [ -d "LLM_LOCAL_MODELLS/Qwen3-8B-MLX-4bit" ]; then
    echo "✅ Qwen3-8B MLX-Modell gefunden"
else
    echo "❌ Qwen3-8B MLX-Modell nicht gefunden"
    exit 1
fi

if [ -d "LLM_LOCAL_MODELLS/Phi-4-mini-reasoning-MLX-4bit" ]; then
    echo "✅ Phi-4-mini-reasoning MLX-Modell gefunden"
else
    echo "❌ Phi-4-mini-reasoning MLX-Modell nicht gefunden"
    exit 1
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

if [ -f "ordo_mlx_agent.py" ]; then
    echo "✅ MLX Voice Agent gefunden"
else
    echo "❌ ordo_mlx_agent.py nicht gefunden"
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

# Starte MLX Voice Agent
echo "🚀 Starte OrDo MLX Voice Agent..."
echo "=========================================================="
python3 ordo_mlx_agent.py 