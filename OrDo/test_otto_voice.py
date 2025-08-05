#!/usr/bin/env python3
"""
🎤 OTTO VOICE TEST - Testet Voice-Funktionalität
=================================================
🔊 Testet ElevenLabs TTS
🎙️ Testet Speech Recognition
🧠 Testet Otto's Antworten
=================================================
"""

import asyncio
import os
from otto_voice_macos import OttoVoiceMacOS

async def test_otto_voice():
    """Testet Otto's Voice-Funktionalität"""
    print("🎤 OTTO VOICE TEST")
    print("=" * 50)
    
    # Setze Environment Variables
    os.environ["ELEVENLABS_API_KEY"] = "sk_a7f0fbc02afb79e9f34ad14e8773aa80e83b930d47c0bf53"
    os.environ["ELEVENLABS_VOICE_ID"] = "6af9AKVSpHxy6rXrzqiz"
    
    print("🔊 Voice-ID: 6af9AKVSpHxy6rXrzqiz")
    print("✅ Environment konfiguriert")
    
    # Initialisiere Otto Voice
    otto_voice = OttoVoiceMacOS()
    
    print("\n🎙️ Teste Voice-Setup...")
    otto_voice.teste_voice_setup()
    
    print("\n🧠 Teste Antwortgenerierung...")
    test_eingabe = "Hallo Otto, wie geht es dir?"
    antwort = await otto_voice._generiere_otto_antwort(test_eingabe)
    print(f"Eingabe: {test_eingabe}")
    print(f"Antwort: {antwort}")
    
    print("\n🔊 Teste ElevenLabs TTS...")
    test_text = "Hallo, ich bin Otto. Ich bin jetzt bereit für unsere Interaktion."
    success = await otto_voice.spreche_elevenlabs(test_text)
    print(f"TTS Test: {'✅ Erfolgreich' if success else '❌ Fehlgeschlagen'}")
    
    print("\n🎭 Teste Function Call-Trigger...")
    function_test = "Otto, träume von der Zukunft"
    antwort = await otto_voice._generiere_otto_antwort(function_test)
    print(f"Function Call Test: {antwort}")
    
    print("\n✅ Voice-Test abgeschlossen!")
    print("Otto ist bereit für Interaktionen.")

if __name__ == "__main__":
    asyncio.run(test_otto_voice()) 