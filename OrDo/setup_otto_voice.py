#!/usr/bin/env python3
"""
🎤 OTTO VOICE SETUP
=====================================
Installiert alle Dependencies für Otto Voice Interface
"""

import subprocess
import sys
import os

def installiere_dependencies():
    """Installiert alle Voice Dependencies"""
    print("🎤 Otto Voice Setup")
    print("=" * 40)
    
    # Installiere Requirements
    print("📦 Installiere Voice Dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_voice.txt"
        ])
        print("✅ Dependencies installiert!")
    except subprocess.CalledProcessError:
        print("❌ Fehler beim Installieren der Dependencies")
        return False
    
    # Check ElevenLabs API Key
    print("\n🔑 Prüfe ElevenLabs Setup...")
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if api_key:
        print("✅ ElevenLabs API Key gefunden!")
    else:
        print("⚠️ ElevenLabs API Key fehlt!")
        print("\n💡 So setzt du den API Key:")
        print("   export ELEVENLABS_API_KEY='dein_api_key'")
        print("   # Oder in ~/.zshrc für permanent")
        
    print("\n🎙️ Voice Setup abgeschlossen!")
    print("🚀 Starte Otto mit: python3 otto_voice_interface.py")
    
    return True

if __name__ == "__main__":
    installiere_dependencies() 