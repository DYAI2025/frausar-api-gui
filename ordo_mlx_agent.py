#!/usr/bin/env python3
"""
OrDo MLX Voice Agent - Verwendet lokale MLX-Modelle
Qwen3-8B und Phi-4-mini-reasoning direkt aus LLM_LOCAL_MODELLS/
"""

import os
import sys
import json
import time
import speech_recognition as sr
import threading
import queue
from datetime import datetime, timedelta
import yaml
from dotenv import load_dotenv
import random
import re
from pathlib import Path
import requests
import asyncio
import websockets
from typing import Dict, List, Optional, Any

# Import Router
from router import Router, load_router_config

# Lade Umgebungsvariablen
load_dotenv()

# Konfiguration
TRIGGER_WORDS = ['ordo', 'ordu', 'odo', 'orden', 'otto']
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')

class OrDoMLXAgent:
    """OrDo Voice Agent mit lokalen MLX-Modellen"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.conversation_active = False
        self.conversation_timeout = 30
        self.last_conversation_time = 0
        self.learning_data = []
        
        # Router Integration
        self.router = None
        self.setup_router()
        
        # Lokale MLX-Modelle
        self.mlx_models = {
            'qwen3:8b': {
                'path': 'LLM_LOCAL_MODELLS/Qwen3-8B-MLX-4bit',
                'temperature': 0.7,
                'max_tokens': 200,
                'type': 'mlx'
            },
            'phi-4-mini:reasoning': {
                'path': 'LLM_LOCAL_MODELLS/Phi-4-mini-reasoning-MLX-4bit',
                'temperature': 0.8,
                'max_tokens': 150,
                'type': 'mlx'
            }
        }
        
        # Fallback zu OpenAI
        self.openai_config = {
            'model': 'gpt-4',
            'temperature': 0.6,
            'max_tokens': 300,
            'endpoint': 'https://api.openai.com/v1/chat/completions'
        }
        
        self.setup_microphone()
        self.setup_voice()
        
        # ElevenLabs Setup
        if ELEVENLABS_API_KEY:
            try:
                from elevenlabs import generate, play, set_api_key
                set_api_key(ELEVENLABS_API_KEY)
                self.elevenlabs_available = True
            except:
                self.elevenlabs_available = False
        else:
            self.elevenlabs_available = False
    
    def setup_router(self):
        """Initialisiert Resonanz-Trichord Router"""
        try:
            config = load_router_config('resonanz_trichord_router.yaml')
            self.router = Router(config)
            print("✅ Resonanz-Trichord Router initialisiert")
        except Exception as e:
            print(f"❌ Router-Initialisierung fehlgeschlagen: {e}")
            self.router = None
    
    def setup_microphone(self):
        """Initialisiert Mikrofon"""
        print("🎤 Initialisiere Mikrofon...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Mikrofon initialisiert")
    
    def setup_voice(self):
        """Initialisiert Sprachausgabe"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
            self.pyttsx3_available = True
        except:
            self.pyttsx3_available = False
            print("⚠️  pyttsx3 nicht verfügbar")
    
    def listen_for_speech(self):
        """Hört auf Sprache"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
            
            try:
                text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                print(f"📝 Erkannt: '{text}'")
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print(f"❌ Spracherkennungsfehler: {e}")
                return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"❌ Mikrofonfehler: {e}")
            return None
    
    def is_trigger_word(self, text):
        """Prüft Trigger-Wörter"""
        if not text:
            return False
        return any(trigger in text for trigger in TRIGGER_WORDS)
    
    def get_trigger_word(self, text):
        """Extrahiert Trigger-Wort"""
        for trigger in TRIGGER_WORDS:
            if trigger in text:
                return trigger
        return None
    
    def clean_input(self, text, trigger_word):
        """Bereinigt Input"""
        return text.replace(trigger_word, '').strip()
    
    def get_mlx_response(self, model_name: str, prompt: str) -> str:
        """Holt Antwort von lokalem MLX-Modell"""
        try:
            # TODO: Implementiere MLX-Modell-Inferenz
            # Für jetzt: Fallback-Antwort
            model_config = self.mlx_models.get(model_name)
            if model_config:
                print(f"🧠 Verwende lokales MLX-Modell: {model_name}")
                return f"[MLX {model_name}] Ich verstehe: {prompt}. Das ist eine lokale Antwort."
            else:
                return f"Modell {model_name} nicht verfügbar."
                
        except Exception as e:
            print(f"❌ MLX-Fehler für {model_name}: {e}")
            return f"Entschuldigung, {model_name} ist nicht verfügbar."
    
    def get_openai_response(self, prompt: str) -> str:
        """Holt Antwort von OpenAI"""
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                return "OpenAI API Key nicht konfiguriert."
            
            headers = {
                'Authorization': f'Bearer {openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.6,
                "max_tokens": 300
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return f"OpenAI-Fehler: {response.status_code}"
                
        except Exception as e:
            print(f"❌ OpenAI-Fehler: {e}")
            return "OpenAI ist momentan nicht verfügbar."
    
    def route_and_respond(self, text: str) -> str:
        """Routet Text zu passendem Modell und generiert Antwort"""
        if not self.router:
            return self.get_fallback_response(text)
        
        try:
            # Erstelle Event für Router
            event = {
                'text': text,
                'timestamp': datetime.now().isoformat(),
                'metadata': {'source': 'voice_input'}
            }
            
            # Route zu Modell
            chosen_model = self.router.route(event)
            print(f"🧠 Router wählte: {chosen_model}")
            
            # Generiere Antwort basierend auf Modell-Typ
            if chosen_model in self.mlx_models:
                response = self.get_mlx_response(chosen_model, text)
            elif chosen_model == 'GPT-4.1':
                response = self.get_openai_response(text)
            else:
                response = self.get_fallback_response(text)
            
            # Lerne aus Interaktion
            self.learn_from_interaction(text, response, chosen_model)
            
            return response
            
        except Exception as e:
            print(f"❌ Routing-Fehler: {e}")
            return self.get_fallback_response(text)
    
    def get_fallback_response(self, text: str) -> str:
        """Fallback-Antwort wenn Router nicht verfügbar"""
        fallback_responses = [
            "Ich verstehe. Lass mich das verarbeiten.",
            "Interessant. Ich lerne daraus.",
            "Danke für die Information.",
            "Ich nehme das zur Kenntnis.",
            "Verstanden. Ich werde das berücksichtigen."
        ]
        return random.choice(fallback_responses)
    
    def learn_from_interaction(self, input_text: str, response: str, model: str):
        """Lernt aus Interaktion"""
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'input': input_text,
            'response': response,
            'model': model,
            'type': 'voice_interaction'
        }
        
        self.learning_data.append(learning_entry)
        
        # Speichere in Datei
        try:
            with open('ordo_learning_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Fehler beim Speichern: {e}")
    
    def speak_response(self, text: str):
        """Spricht Antwort"""
        if self.elevenlabs_available:
            try:
                from elevenlabs import generate, play
                audio = generate(
                    text=text,
                    voice=VOICE_ID,
                    model="eleven_multilingual_v2"
                )
                
                def play_audio():
                    play(audio)
                
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.start()
                
                print(f"🗣️  OrDo sagt: {text}")
                
            except Exception as e:
                print(f"❌ ElevenLabs-Fehler: {e}")
                self.speak_fallback(text)
        else:
            self.speak_fallback(text)
    
    def speak_fallback(self, text: str):
        """Fallback-Sprachausgabe"""
        if self.pyttsx3_available:
            def speak_thread():
                self.engine.say(text)
                self.engine.runAndWait()
            
            thread = threading.Thread(target=speak_thread)
            thread.start()
            print(f"🗣️  OrDo sagt: {text}")
        else:
            print(f"🗣️  OrDo sagt: {text}")
    
    def run(self):
        """Hauptschleife"""
        print("🧠 OrDo MLX Voice Agent - Lokale MLX-Modelle")
        print("=" * 70)
        print(f"🎯 Trigger-Wörter: {', '.join(TRIGGER_WORDS)}")
        print(f"🧠 Router: {'✅ Aktiviert' if self.router else '❌ Nicht verfügbar'}")
        print(f"🎵 ElevenLabs: {'✅ Verfügbar' if self.elevenlabs_available else '❌ Nicht verfügbar'}")
        print(f"🔊 pyttsx3: {'✅ Verfügbar' if self.pyttsx3_available else '❌ Nicht verfügbar'}")
        print("📁 Lokale MLX-Modelle:")
        for model_name, config in self.mlx_models.items():
            path_exists = os.path.exists(config['path'])
            print(f"  {'✅' if path_exists else '❌'} {model_name}: {config['path']}")
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 70)
        
        while True:
            try:
                print("🔊 Höre zu...")
                text = self.listen_for_speech()
                
                if text:
                    # Prüfe Trigger
                    if self.is_trigger_word(text):
                        trigger_word = self.get_trigger_word(text)
                        clean_text = self.clean_input(text, trigger_word)
                        
                        print(f"🧠 OrDo aktiviert durch '{trigger_word}'")
                        print(f"🧠 OrDo verarbeitet: '{clean_text}'")
                        
                        # Starte Konversation
                        self.conversation_active = True
                        self.last_conversation_time = time.time()
                        
                        # Route und generiere Antwort
                        response = self.route_and_respond(clean_text)
                        self.speak_response(response)
                        
                    elif self.conversation_active:
                        # Fortsetzung der Konversation
                        print(f"🧠 Fortsetzung: {text}")
                        
                        # Prüfe Timeout
                        if time.time() - self.last_conversation_time > self.conversation_timeout:
                            print("⏱️  Dialog-Fenster geschlossen.")
                            self.conversation_active = False
                        else:
                            # Route und generiere Antwort
                            response = self.route_and_respond(text)
                            self.speak_response(response)
                            self.last_conversation_time = time.time()
                    
                    else:
                        # Passive Analyse
                        print(f"🔍 Passiv analysiert: {text[:50]}...")
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 OrDo MLX Voice Agent wird beendet...")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

def main():
    """Hauptfunktion"""
    agent = OrDoMLXAgent()
    agent.run()

if __name__ == "__main__":
    main() 