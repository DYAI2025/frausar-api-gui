#!/usr/bin/env python3
"""
🎤 OTTO VOICE INTERFACE
============================================================
🎯 Sprach-Ein- und Ausgabe für Otto Evolution
🔊 ElevenLabs TTS Integration
🎙️ Kontinuierliches Lauschen
🗣️ Natürliche Sprachinteraktion
============================================================
"""

import asyncio
import speech_recognition as sr
import requests
import pygame
import io
import os
import threading
import time
from pathlib import Path
import tempfile
from typing import Optional

from otto_evolution_master import OttoEvolutionMaster

class OttoVoiceInterface:
    def __init__(self):
        print("🎤 Initialisiere Otto Voice Interface...")
        
        # Otto Evolution System
        self.otto = OttoEvolutionMaster()
        
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # ElevenLabs Configuration
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID', "6af9AKVSpHxy6rXrzqiz")  # Deine Otto-Stimme
        
        # Audio Setup
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Lausch-Status
        self.is_listening = False
        self.is_speaking = False
        
        # Kalibriere Mikrofon
        self._kalibriere_mikrofon()
        
        print("✅ Otto Voice Interface bereit!")
        
    def _kalibriere_mikrofon(self):
        """Kalibriert das Mikrofon für Umgebungsgeräusche"""
        print("🎙️ Kalibriere Mikrofon für Umgebungsgeräusche...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Mikrofon kalibriert")
        
    async def spreche(self, text: str) -> bool:
        """Lässt Otto mit ElevenLabs sprechen"""
        if not self.elevenlabs_api_key:
            print("⚠️ ElevenLabs API Key fehlt - verwende Text-Ausgabe")
            print(f"Otto: {text}")
            return False
            
        try:
            self.is_speaking = True
            print(f"🗣️ Otto sagt: {text}")
            
            # ElevenLabs API Call
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.2,
                    "use_speaker_boost": True
                }
            }
            
            # Async HTTP Request
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                # Spiele Audio ab
                audio_data = io.BytesIO(response.content)
                
                # Speichere temporär für pygame
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_path = temp_file.name
                
                # Spiele ab
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                
                # Warte bis fertig
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
                    
                # Lösche temporäre Datei
                os.unlink(temp_path)
                
                self.is_speaking = False
                return True
            else:
                print(f"❌ ElevenLabs Fehler: {response.status_code}")
                print(f"Otto: {text}")  # Fallback zu Text
                self.is_speaking = False
                return False
                
        except Exception as e:
            print(f"❌ Sprach-Fehler: {e}")
            print(f"Otto: {text}")  # Fallback zu Text
            self.is_speaking = False
            return False
            
    def lausche_einmal(self) -> Optional[str]:
        """Lauscht einmal auf Spracheingabe"""
        try:
            with self.microphone as source:
                print("🎙️ Lausche...")
                # Kurzes Timeout für kontinuierliches Lauschen
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
            print("🔄 Erkenne Sprache...")
            # Verwende Google Speech Recognition (kostenlos)
            text = self.recognizer.recognize_google(audio, language='de-DE')
            print(f"👂 Gehört: {text}")
            return text
            
        except sr.WaitTimeoutError:
            # Kein Problem - einfach weiter lauschen
            return None
        except sr.UnknownValueError:
            # Sprache nicht verstanden
            return None
        except sr.RequestError as e:
            print(f"❌ Speech Recognition Fehler: {e}")
            return None
            
    async def kontinuierliches_lauschen(self):
        """Lauscht kontinuierlich im Hintergrund"""
        print("👂 Starte kontinuierliches Lauschen...")
        self.is_listening = True
        
        while self.is_listening:
            try:
                # Lausche nicht während Otto spricht
                if self.is_speaking:
                    await asyncio.sleep(0.5)
                    continue
                    
                # Lausche auf Eingabe
                eingabe = self.lausche_einmal()
                
                if eingabe:
                    # Verarbeite durch Otto Evolution System
                    antwort = await self.otto.verarbeite_interaktion(eingabe)
                    
                    # Otto antwortet
                    await self.spreche(antwort)
                    
                else:
                    # Kurze Pause zwischen Lausch-Versuchen
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                print(f"❌ Lausch-Fehler: {e}")
                await asyncio.sleep(1)
                
    def stoppe_lauschen(self):
        """Stoppt das kontinuierliche Lauschen"""
        print("⏹️ Stoppe Lauschen...")
        self.is_listening = False
        
    async def starte_voice_session(self):
        """Startet eine Voice Session mit Otto"""
        print("\n🎤 OTTO VOICE SESSION")
        print("=" * 50)
        print("🗣️ Sprich mit Otto! Er lauscht kontinuierlich.")
        print("⌨️ Drücke Ctrl+C zum Beenden")
        print("🔊 Stelle sicher, dass deine Lautsprecher an sind!")
        
        # Begrüßung
        await self.spreche("Hallo! Ich bin Otto. Ich höre dir zu und wir können ganz normal miteinander reden!")
        
        try:
            # Starte kontinuierliches Lauschen
            await self.kontinuierliches_lauschen()
            
        except KeyboardInterrupt:
            print("\n👋 Otto Voice Session beendet")
            await self.spreche("Bis bald! Es war schön mit dir zu reden!")
            self.stoppe_lauschen()
            
    def teste_voice_setup(self):
        """Testet das Voice Setup"""
        print("\n🧪 Teste Voice Setup:")
        
        # Test Mikrofon
        print("1. Teste Mikrofon...")
        test_input = self.lausche_einzel_test()
        if test_input:
            print(f"✅ Mikrofon funktioniert: '{test_input}'")
        else:
            print("❌ Mikrofon-Problem")
            
        # Test ElevenLabs
        print("2. Teste ElevenLabs...")
        if self.elevenlabs_api_key:
            print("✅ API Key gefunden")
        else:
            print("❌ ElevenLabs API Key fehlt")
            print("💡 Setze ELEVENLABS_API_KEY in der Umgebung")
            
    def lausche_einzel_test(self) -> Optional[str]:
        """Einmaliger Test für Mikrofon"""
        try:
            with self.microphone as source:
                print("🎙️ Sage etwas zum Testen...")
                audio = self.recognizer.listen(source, timeout=5)
                
            text = self.recognizer.recognize_google(audio, language='de-DE')
            return text
        except:
            return None


# Haupt-Interface
async def main():
    # Erstelle Voice Interface
    voice_otto = OttoVoiceInterface()
    
    # Teste Setup
    voice_otto.teste_voice_setup()
    
    # Starte Voice Session
    await voice_otto.starte_voice_session()


if __name__ == "__main__":
    print("🎤 Otto Voice Interface wird gestartet...")
    asyncio.run(main()) 