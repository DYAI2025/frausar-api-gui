#!/bin/bash
# 🎤 Otto Voice Starter mit echter Stimme
# =====================================

echo "🎤 Starte Otto Voice mit echter ElevenLabs Stimme..."

# Setze ElevenLabs Konfiguration
export ELEVENLABS_API_KEY="sk_a7f0fbc02afb79e9f34ad14e8773aa80e83b930d47c0bf53"
export ELEVENLABS_VOICE_ID="6af9AKVSpHxy6rXrzqiz"

echo "🔊 Voice-ID: $ELEVENLABS_VOICE_ID"
echo "✅ ElevenLabs konfiguriert"

# Starte Otto Voice Interface
python3 otto_voice_macos.py 