#!/usr/bin/env python3
"""
🌌 OTTO COSD STARTER
Startet Otto mit dem vollständigen Co-Emergent Semantic Drift System
"""

import asyncio
import os
import sys
from pathlib import Path

# Umgebungsvariablen für ElevenLabs setzen (falls vorhanden)
def setup_environment():
    """Setze Umgebungsvariablen für Otto"""
    
    # ElevenLabs Configuration
    elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
    voice_id = os.getenv('ELEVENLABS_VOICE_ID')
    
    # Fallback für Voice ID
    if not voice_id:
        voice_id = "6af9AKVSpHxy6rXrzqiz"  # Otto's Standard Voice ID
        os.environ['ELEVENLABS_VOICE_ID'] = voice_id
        print("🔧 Voice ID als Fallback gesetzt")
    
    if not elevenlabs_key:
        print("⚠️ ELEVENLABS_API_KEY nicht gesetzt")
        print("💡 Für beste Erfahrung: export ELEVENLABS_API_KEY='your_key'")
        print("🔄 Fallback zu macOS 'say' command")
    
    print("✅ ElevenLabs konfiguriert")
    print(f"🔊 Voice-ID: {voice_id}")

async def main():
    """Startet Otto mit COSD"""
    print("🌌 OTTO COSD SYSTEM")
    print("=" * 50)
    print("Co-Emergent Semantic Drift erwacht...")
    print()
    
    # Setup Environment
    setup_environment()
    
    # Importiere und starte Voice Interface
    try:
        from otto_voice_macos import main as voice_main
        await voice_main()
        
    except KeyboardInterrupt:
        print("\n\n👋 Otto COSD Session beendet")
        print("✨ Die drei Stimmen verstummen...")
        
    except Exception as e:
        print(f"\n❌ Fehler beim Start: {e}")
        print("💡 Stelle sicher, dass alle Dependencies installiert sind:")
        print("   pip install speech_recognition requests numpy")

if __name__ == "__main__":
    asyncio.run(main()) 