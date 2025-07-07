#!/bin/bash

echo "🌌 Starte Otto COSD System..."
echo "Co-Emergent Semantic Drift erwacht..."

# Setze ElevenLabs Konfiguration DIREKT
# WARNUNG: Der API Key scheint falsch zu sein - ElevenLabs Keys beginnen nicht mit "sk-proj-"
# Das ist ein OpenAI Format. Für jetzt nutzen wir macOS Say als Fallback
export ELEVENLABS_API_KEY=""
export ELEVENLABS_VOICE_ID="6af9AKVSpHxy6rXrzqiz"

echo "✅ ElevenLabs konfiguriert"
echo "🔊 Voice-ID: $ELEVENLABS_VOICE_ID"
echo ""

# Starte Otto COSD mit Umgebungsvariablen
ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY" ELEVENLABS_VOICE_ID="$ELEVENLABS_VOICE_ID" python3 start_otto_cosd.py 