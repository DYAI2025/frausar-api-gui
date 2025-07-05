#!/usr/bin/env python3
"""
🧠 OTTO MASTER - Konsolidierte Version
============================================================
🎯 Eine einzige, saubere Otto-Instanz ohne Konflikte
🔧 Konfigurierbare LLM- und TTS-Provider
⚡ Keine API-Konflikte oder doppelte Stimmen
"""

import os
import sys
import time
import json
import yaml
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from typing import Optional, Dict, Any
import threading
import queue

# OpenAI-Integration (neue API v1.0.0+)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ElevenLabs-Integration
try:
    from elevenlabs import generate, save
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

class OttoMaster:
    def __init__(self, config_file: str = "otto_config.yaml"):
        """Initialisiert Otto Master mit Konfiguration"""
        self.config = self.load_config(config_file)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.response_queue = queue.Queue()
        self.is_speaking = False
        self.dialog_active = False
        self.last_interaction = None
        
        # LLM-Client initialisieren
        self.llm_client = self.init_llm()
        
        # TTS-Engine initialisieren
        self.tts_engine = self.init_tts()
        
        # Trigger-Wörter
        self.triggers = ["otto", "ordo", "ordu", "odo", "orden"]
        
        print("🧠 OTTO MASTER - Konsolidierte Version")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(self.triggers)}")
        print(f"🧠 LLM: {self.config['llm']['provider']}")
        print(f"🎤 TTS: {self.config['tts']['provider']}")
        print(f"📋 Features: {', '.join([k for k, v in self.config['features'].items() if v])}")
        print("=" * 60)

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Lädt Konfiguration aus YAML-Datei"""
        default_config = {
            "llm": {
                "provider": "local",  # "local", "openai", "claude"
                "model": "gpt-4",
                "api_key": os.getenv("OPENAI_API_KEY", "")
            },
            "tts": {
                "provider": "pyttsx3",  # "pyttsx3", "elevenlabs"
                "voice": "default",
                "rate": 150
            },
            "features": {
                "learning_system": True,
                "kanban": True,
                "semantic_markers": True
            },
            "audio": {
                "energy_threshold": 4000,
                "pause_threshold": 0.8,
                "dynamic_energy_threshold": True
            }
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
                default_config.update(file_config)
        
        return default_config

    def init_llm(self):
        """Initialisiert LLM-Client basierend auf Konfiguration"""
        provider = self.config['llm']['provider']
        
        if provider == "openai" and OPENAI_AVAILABLE:
            api_key = self.config['llm']['api_key']
            if api_key:
                return OpenAI(api_key=api_key)
            else:
                print("⚠️  OpenAI API-Key nicht gefunden, verwende lokale Logik")
                return None
        else:
            print("🧠 Verwende lokale Logik")
            return None

    def init_tts(self):
        """Initialisiert TTS-Engine"""
        provider = self.config['tts']['provider']
        
        if provider == "pyttsx3":
            engine = pyttsx3.init()
            engine.setProperty('rate', self.config['tts']['rate'])
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
            print("✅ pyttsx3 TTS initialisiert")
            return engine
        elif provider == "elevenlabs" and ELEVENLABS_AVAILABLE:
            print("✅ ElevenLabs TTS verfügbar")
            return "elevenlabs"
        else:
            print("⚠️  ElevenLabs nicht verfügbar, verwende pyttsx3")
            engine = pyttsx3.init()
            return engine

    def speak(self, text: str):
        """Spricht Text aus (thread-safe)"""
        if self.is_speaking:
            return
        
        self.is_speaking = True
        print(f"🗣️  Otto sagt: {text}")
        
        try:
            if self.config['tts']['provider'] == "elevenlabs" and ELEVENLABS_AVAILABLE:
                # ElevenLabs TTS
                audio = generate(text=text, voice="Antoni")
                save(audio, "temp_response.mp3")
                os.system("afplay temp_response.mp3")
                os.remove("temp_response.mp3")
            else:
                # pyttsx3 TTS
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ TTS-Fehler: {e}")
        
        self.is_speaking = False

    def process_with_llm(self, text: str) -> str:
        """Verarbeitet Text mit LLM"""
        if not self.llm_client:
            return self.local_response(text)
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.config['llm']['model'],
                messages=[
                    {"role": "system", "content": "Du bist Otto, ein ruhiger, strukturierter KI-Begleiter. Antworte kurz und hilfreich."},
                    {"role": "user", "content": text}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ LLM-Fehler: {e}")
            return self.local_response(text)

    def local_response(self, text: str) -> str:
        """Lokale Antwortlogik ohne API"""
        text_lower = text.lower()
        
        # Einfache Befehlserkennung
        if any(word in text_lower for word in ["hallo", "hi", "hey"]):
            return "Hallo! Ich bin Otto, dein stiller Begleiter. Wie kann ich dir helfen?"
        
        elif any(word in text_lower for word in ["test", "funktioniert"]):
            return "Otto Test erfolgreich. Ich höre zu und kann sprechen."
        
        elif any(word in text_lower for word in ["strukturieren", "struktur"]):
            return "Ich kann dir dabei helfen, deine Gedanken zu strukturieren. Was möchtest du organisieren?"
        
        elif any(word in text_lower for word in ["hilfe", "help"]):
            return "Ich kann Tasks verwalten, analysieren und strukturieren. Sage mir, was du brauchst."
        
        else:
            return "Ich verstehe deine Anfrage. Wie kann ich dir helfen?"

    def is_trigger_word(self, text: str) -> bool:
        """Prüft, ob Text ein Trigger-Wort enthält"""
        text_lower = text.lower()
        return any(trigger in text_lower for trigger in self.triggers)

    def extract_command(self, text: str) -> str:
        """Extrahiert Befehl aus Trigger-Wort"""
        text_lower = text.lower()
        for trigger in self.triggers:
            if trigger in text_lower:
                return text_lower.replace(trigger, "").strip()
        return text

    def listen(self):
        """Hauptschleife für Spracherkennung"""
        print("🎤 Initialisiere Mikrofon...")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.recognizer.energy_threshold = self.config['audio']['energy_threshold']
            self.recognizer.dynamic_energy_threshold = self.config['audio']['dynamic_energy_threshold']
            self.recognizer.pause_threshold = self.config['audio']['pause_threshold']
        
        print("✅ Mikrofon initialisiert")
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        while True:
            try:
                print("🔊 Höre zu...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                
                print("🔍 Erkenne Sprache...")
                try:
                    text = self.recognizer.recognize_google(audio, language='de-DE')
                    print(f"📝 Erkannt: '{text}'")
                    
                    # Prüfe Trigger-Wort
                    if self.is_trigger_word(text):
                        self.dialog_active = True
                        self.last_interaction = datetime.now()
                        
                        command = self.extract_command(text)
                        print(f"🗣️  Otto aktiviert durch '{next(t for t in self.triggers if t in text.lower())}'")
                        print(f"🧠 Otto verarbeitet: '{command}'")
                        
                        # Verarbeite mit LLM
                        response = self.process_with_llm(command)
                        
                        # Spreche Antwort
                        self.speak(response)
                        
                        # Dialog-Fenster
                        self.dialog_active = True
                        time.sleep(2)  # Kurze Pause für Dialog
                        
                    elif self.dialog_active:
                        # Fortsetzung des Dialogs
                        print(f"🗣️  Fortsetzung: {text}")
                        response = self.process_with_llm(text)
                        self.speak(response)
                        
                        # Dialog-Fenster schließen nach Pause
                        if (datetime.now() - self.last_interaction).seconds > 5:
                            print("⏱️  Dialog-Fenster geschlossen.")
                            self.dialog_active = False
                        else:
                            self.last_interaction = datetime.now()
                    
                except sr.UnknownValueError:
                    pass  # Keine Sprache erkannt
                except sr.RequestError as e:
                    print(f"❌ Spracherkennungsfehler: {e}")
                
            except KeyboardInterrupt:
                print("\n👋 Otto wird beendet...")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

def main():
    """Hauptfunktion"""
    try:
        otto = OttoMaster()
        otto.listen()
    except Exception as e:
        print(f"❌ Kritischer Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 