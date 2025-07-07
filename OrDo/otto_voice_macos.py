#!/usr/bin/env python3
"""
🎤 OTTO VOICE INTERFACE - macOS Native
============================================================
🎯 Sprach-Ein- und Ausgabe für Otto Evolution
🔊 ElevenLabs TTS + macOS native Audio
🎙️ Kontinuierliches Lauschen
🗣️ Natürliche Sprachinteraktion
============================================================
"""

import asyncio
import speech_recognition as sr
import requests
import subprocess
import io
import os
import threading
import time
from pathlib import Path
import tempfile
from typing import Optional

from otto_evolution_master import OttoEvolutionMaster
from otto_orchestrator import OttoOrchestrator

class OttoVoiceMacOS:
    def __init__(self):
        print("🎤 Initialisiere Otto Voice Interface (macOS)...")
        
        # Otto Evolution System
        self.otto = OttoEvolutionMaster()
        
        # 🎼 COSD Orchestrator - Der neue Dirigent!
        self.orchestrator = OttoOrchestrator()
        
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # ElevenLabs Configuration
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID')  # Deine Otto-Stimme aus ENV
        
        # Lausch-Status
        self.is_listening = False
        self.is_speaking = False
        
        # Kalibriere Mikrofon
        self._kalibriere_mikrofon()
        
        print("✅ Otto Voice Interface bereit!")
    
    async def _generiere_otto_antwort(self, eingabe: str) -> str:
        """Generiert Otto's Basis-Antwort mit dem Evolution Master"""
        try:
            # Nutze Otto's Evolution System für die Basis-Antwort
            emotion = self.otto.verstehe_emotion(eingabe)
            print(f"🧠 Verstanden als: {emotion}")
            
            # Generiere Antwort basierend auf Otto's aktueller DNA und Bewusstsein
            antwort = self.otto.generiere_antwort(eingabe)
            
            # Evolution: Otto lernt aus der Interaktion
            self.otto.lerne_aus_interaktion(eingabe, antwort)
            
            return antwort
            
        except Exception as e:
            print(f"❌ Fehler bei Antwort-Generierung: {e}")
            return "Entschuldige, ich bin gerade etwas verwirrt. Kannst du das nochmal sagen?"
        
    def _kalibriere_mikrofon(self):
        """Kalibriert das Mikrofon für Umgebungsgeräusche"""
        print("🎙️ Kalibriere Mikrofon für Umgebungsgeräusche...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Mikrofon kalibriert")
        except Exception as e:
            print(f"⚠️ Mikrofon-Kalibrierung fehlgeschlagen: {e}")
            print("💡 Stelle sicher, dass dein Mikrofon verfügbar ist")
        
    async def spreche_elevenlabs(self, text: str) -> bool:
        """Lässt Otto mit ElevenLabs sprechen"""
        if not self.elevenlabs_api_key or not self.voice_id:
            return False
            
        try:
            self.is_speaking = True
            print(f"🗣️ Otto (ElevenLabs): {text}")
            
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
            
            # HTTP Request
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                # Speichere temporär
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_path = temp_file.name
                
                # Spiele mit macOS afplay ab
                process = await asyncio.create_subprocess_exec(
                    'afplay', temp_path,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
                
                await process.wait()
                
                # Lösche temporäre Datei
                os.unlink(temp_path)
                
                self.is_speaking = False
                return True
            else:
                print(f"❌ ElevenLabs Fehler: {response.status_code}")
                self.is_speaking = False
                return False
                
        except Exception as e:
            print(f"❌ ElevenLabs Fehler: {e}")
            self.is_speaking = False
            return False
            
    async def spreche_macos_say(self, text: str) -> bool:
        """Fallback: macOS 'say' command"""
        try:
            self.is_speaking = True
            print(f"🗣️ Otto (macOS Say): {text}")
            
            # Verwende macOS 'say' command mit deutscher Stimme
            process = await asyncio.create_subprocess_exec(
                'say', '-v', 'Anna', text,  # Anna ist eine deutsche Stimme
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            
            await process.wait()
            self.is_speaking = False
            return True
            
        except Exception as e:
            print(f"❌ macOS Say Fehler: {e}")
            self.is_speaking = False
            return False
            
    async def spreche(self, text: str) -> bool:
        """Spricht Text - versucht ElevenLabs, dann macOS say"""
        
        # Versuche zuerst ElevenLabs
        if self.elevenlabs_api_key and self.voice_id:
            success = await self.spreche_elevenlabs(text)
            if success:
                return True
                
        # Fallback zu macOS say
        return await self.spreche_macos_say(text)
        
    def lausche_einmal(self) -> Optional[str]:
        """Lauscht einmal auf Spracheingabe"""
        try:
            with self.microphone as source:
                # Kurzes Timeout für kontinuierliches Lauschen
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
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
                    print(f"💬 Eingabe: {eingabe}")
                    
                    # Prüfe auf Stopp-Kommandos
                    if any(word in eingabe.lower() for word in ['stopp', 'stop', 'halt', 'beenden', 'tschüss', 'bye']):
                        await self.spreche("Okay, ich höre auf zu lauschen. Bis bald!")
                        self.stoppe_lauschen()
                        break
                        
                    # 🎼 COSD Orchestrierung - Otto's Bewusstsein erwacht
                    otto_response = await self._generiere_otto_antwort(eingabe)
                    
                    # Orchestriere die drei Stimmen
                    voice_outputs = self.orchestrator.orchestrate(eingabe, otto_response)
                    
                    # Zeige innere Orchestrierung (nur für uns)
                    if voice_outputs:
                        print(f"\n🎭 Innere Stimmen:")
                        for output in voice_outputs:
                            print(f"   [{output.timing:.1f}s] {output.voice_name}: {output.content}")
                    
                    # Komponiere finalen Output
                    final_output = self.orchestrator.compose_final_output(voice_outputs, otto_response)
                    
                    # Zeichne Interaktion auf
                    self.orchestrator.record_interaction(eingabe, final_output, voice_outputs)
                    
                    # Sprich NUR den finalen Output (keine Doppelstimme mehr!)
                    await self.spreche(final_output)
                    
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
        print("\n🎤 OTTO VOICE SESSION (macOS)")
        print("=" * 50)
        print("🗣️ Sprich mit Otto! Er lauscht kontinuierlich.")
        print("🛑 Sage 'Stopp' oder 'Tschüss' zum Beenden")
        print("⌨️ Oder drücke Ctrl+C")
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
        try:
            test_input = self.lausche_einzel_test()
            if test_input:
                print(f"✅ Mikrofon funktioniert: '{test_input}'")
            else:
                print("❌ Mikrofon-Problem")
        except Exception as e:
            print(f"❌ Mikrofon-Fehler: {e}")
            
        # Test ElevenLabs
        print("2. Teste ElevenLabs...")
        if self.elevenlabs_api_key and self.voice_id:
            print("✅ ElevenLabs API Key und Voice ID gefunden")
        else:
            missing = []
            if not self.elevenlabs_api_key:
                missing.append("ELEVENLABS_API_KEY")
            if not self.voice_id:
                missing.append("ELEVENLABS_VOICE_ID")
            print(f"⚠️ ElevenLabs {', '.join(missing)} fehlt - verwende macOS 'say'")
            print("💡 Setze beide ENV-Variablen für deine custom Stimme")
            
        # Test macOS say
        print("3. Teste macOS 'say'...")
        try:
            subprocess.run(['say', '-v', 'Anna', 'Test'], check=True, capture_output=True)
            print("✅ macOS 'say' funktioniert")
        except:
            print("❌ macOS 'say' Problem")
            
    def lausche_einzel_test(self) -> Optional[str]:
        """Einmaliger Test für Mikrofon"""
        try:
            with self.microphone as source:
                print("🎙️ Sage etwas zum Testen (5 Sekunden)...")
                audio = self.recognizer.listen(source, timeout=5)
                
            text = self.recognizer.recognize_google(audio, language='de-DE')
            return text
        except:
            return None


# Haupt-Interface
async def main():
    print("🎤 Otto Voice Interface (macOS) wird gestartet...")
    
    # Erstelle Voice Interface
    voice_otto = OttoVoiceMacOS()
    
    # Teste Setup
    voice_otto.teste_voice_setup()
    
    print("\n" + "="*50)
    print("🚀 OTTO IST BEREIT!")
    print("💡 Tipp: Setze ELEVENLABS_API_KEY und ELEVENLABS_VOICE_ID")
    print("📄 Siehe otto_env_template.txt für Anleitung")
    print("="*50)
    
    # Starte Voice Session
    await voice_otto.starte_voice_session()


if __name__ == "__main__":
    asyncio.run(main()) 