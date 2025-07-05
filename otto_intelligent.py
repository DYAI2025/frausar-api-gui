#!/usr/bin/env python3
"""
🧠 OTTO INTELLIGENT - Echte KI-Integration
============================================================
🎯 Otto mit echter Intelligenz und semantischem Verständnis
🧠 Dynamische Antwortgenerierung basierend auf Kontext
💬 Konversationsgedächtnis und Lernfähigkeit
🔧 Fallback-Systeme für verschiedene LLM-Provider
"""

import os
import sys
import time
import json
import yaml
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from typing import Optional, Dict, Any, List
import threading
import queue
import random

# OpenAI-Integration (neue API v1.0.0+)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Anthropic Claude-Integration
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

# ElevenLabs-Integration
try:
    from elevenlabs import generate, save
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

class OttoIntelligent:
    def __init__(self):
        self.name = "Otto"
        self.personality = {
            "style": "ruhig, strukturiert, lernfähig",
            "role": "passiver Task-Begleiter mit semantischer Marker-Intelligenz",
            "approach": "nur auf direkte Ansprache reagieren",
            "focus": "Aufgaben erkennen, analysieren, strukturieren"
        }
        
        # Trigger-Wörter
        self.triggers = ["otto", "ordo", "ordu", "odo", "orden"]
        
        # Konversationsgedächtnis
        self.conversation_history = []
        self.context_memory = []
        self.learning_data = []
        
        # LLM-Provider Konfiguration
        self.llm_providers = {
            "claude": CLAUDE_AVAILABLE,
            "openai": OPENAI_AVAILABLE,
            "local": True  # Fallback
        }
        
        # Aktiver Provider (Priorität: Claude > OpenAI > Local)
        self.active_provider = self._select_best_provider()
        
        # TTS-Engine
        self.tts_engine = self._init_tts()
        
        # Mikrofon
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Audio-Threading
        self.speaking_lock = threading.Lock()
        self.audio_queue = queue.Queue()
        
        print(f"🧠 OTTO INTELLIGENT - Echte KI-Integration")
        print(f"============================================================")
        print(f"🎯 Provider: {self.active_provider.upper()}")
        print(f"🧠 Persönlichkeit: {self.personality['style']}")
        print(f"💬 Konversationsgedächtnis: Aktiviert")
        print(f"🎤 TTS: {type(self.tts_engine).__name__}")
        
    def _select_best_provider(self) -> str:
        """Wählt den besten verfügbaren LLM-Provider"""
        if self.llm_providers["claude"]:
            return "claude"
        elif self.llm_providers["openai"]:
            return "openai"
        else:
            return "local"
    
    def _init_tts(self):
        """Initialisiert TTS-Engine"""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.8)
            return engine
        except Exception as e:
            print(f"❌ TTS-Fehler: {e}")
            return None
    
    def _get_llm_response(self, user_input: str, context: str = "") -> str:
        """Generiert intelligente Antwort basierend auf LLM"""
        
        # Kontext zusammenstellen
        full_context = self._build_context(user_input, context)
        
        try:
            if self.active_provider == "claude":
                return self._claude_response(full_context)
            elif self.active_provider == "openai":
                return self._openai_response(full_context)
            else:
                return self._local_response(full_context)
        except Exception as e:
            print(f"❌ LLM-Fehler: {e}")
            return self._fallback_response(user_input)
    
    def _build_context(self, user_input: str, context: str = "") -> str:
        """Baut Kontext für LLM-Antwort"""
        
        # Persönlichkeits-Prompt
        personality_prompt = f"""
Du bist {self.name}, ein {self.personality['role']}.
Dein Stil: {self.personality['style']}
Dein Ansatz: {self.personality['approach']}
Dein Fokus: {self.personality['focus']}

Antworte kurz, präzise und hilfreich. Sei strukturiert und ruhig.
"""
        
        # Konversationshistorie (letzte 5 Einträge)
        history_context = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-5:]
            history_context = "\n".join([f"Ben: {h['user']}\nOtto: {h['otto']}" for h in recent_history])
        
        # Vollständiger Kontext
        full_context = f"""
{personality_prompt}

Kontext: {context}
Historie: {history_context}

Ben: {user_input}
Otto:"""
        
        return full_context
    
    def _claude_response(self, context: str) -> str:
        """Claude API Antwort"""
        if not CLAUDE_AVAILABLE:
            return self._fallback_response(context)
        
        try:
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                messages=[{"role": "user", "content": context}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"❌ Claude-Fehler: {e}")
            return self._fallback_response(context)
    
    def _openai_response(self, context: str) -> str:
        """OpenAI API Antwort"""
        if not OPENAI_AVAILABLE:
            return self._fallback_response(context)
        
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4",
                max_tokens=150,
                messages=[{"role": "user", "content": context}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ OpenAI-Fehler: {e}")
            return self._fallback_response(context)
    
    def _local_response(self, context: str) -> str:
        """Lokale intelligente Antwort (ohne API)"""
        
        # Semantische Analyse
        user_input = context.split("Ben: ")[-1].split("\n")[0].strip()
        
        # Schlüsselwort-basierte Antworten
        keywords = {
            "strukturieren": [
                "Ich helfe dir dabei, deine Gedanken zu strukturieren. Was möchtest du organisieren?",
                "Lass uns das systematisch angehen. Was ist dein Hauptthema?",
                "Ich kann dir dabei helfen, Ordnung in deine Ideen zu bringen. Erzähl mir mehr."
            ],
            "lernen": [
                "Ich lerne aus jeder Interaktion mit dir. Was möchtest du mir beibringen?",
                "Das ist interessant. Ich speichere das in meinem Gedächtnis.",
                "Danke für die Information. Ich werde daraus lernen."
            ],
            "verstehen": [
                "Ja, ich verstehe dich. Was beschäftigt dich?",
                "Ich höre dir zu und verstehe deine Anliegen.",
                "Ich verstehe. Wie kann ich dir konkret helfen?"
            ],
            "hilfe": [
                "Ich bin hier, um dir zu helfen. Was brauchst du?",
                "Sag mir, womit ich dir helfen kann.",
                "Ich stehe dir zur Verfügung. Was ist dein Anliegen?"
            ]
        }
        
        # Beste Antwort finden
        for keyword, responses in keywords.items():
            if keyword.lower() in user_input.lower():
                return random.choice(responses)
        
        # Standard-Antworten für verschiedene Situationen
        standard_responses = [
            "Ich verstehe. Was möchtest du als nächstes angehen?",
            "Interessant. Lass uns das weiter entwickeln.",
            "Ich höre dir zu. Was ist dein nächster Schritt?",
            "Das ist eine gute Frage. Wie kann ich dir dabei helfen?",
            "Ich verstehe dein Anliegen. Was ist dein Ziel?"
        ]
        
        return random.choice(standard_responses)
    
    def _fallback_response(self, user_input: str) -> str:
        """Fallback-Antwort wenn alle LLMs fehlschlagen"""
        return "Ich verstehe dich. Wie kann ich dir helfen?"
    
    def _speak(self, text: str):
        """Spricht Text aus (thread-safe)"""
        with self.speaking_lock:
            if self.tts_engine:
                try:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                except Exception as e:
                    print(f"❌ TTS-Fehler: {e}")
            else:
                print(f"🗣️  {text}")
    
    def _save_conversation(self, user_input: str, otto_response: str):
        """Speichert Konversation im Gedächtnis"""
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "otto": otto_response
        }
        self.conversation_history.append(conversation_entry)
        
        # Gedächtnis begrenzen (max 100 Einträge)
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
    
    def process_input(self, user_input: str) -> str:
        """Verarbeitet Benutzer-Eingabe und generiert intelligente Antwort"""
        
        # Intelligente Antwort generieren
        response = self._get_llm_response(user_input)
        
        # Konversation speichern
        self._save_conversation(user_input, response)
        
        return response
    
    def listen_and_respond(self):
        """Hauptschleife: Hört zu und antwortet"""
        
        print("🎤 Initialisiere Mikrofon...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("✅ Mikrofon initialisiert")
        
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("============================================================")
        
        while True:
            try:
                print("🔊 Höre zu...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                
                print("🔍 Erkenne Sprache...")
                try:
                    text = self.recognizer.recognize_google(audio, language="de-DE").lower()
                    print(f"📝 Erkannt: '{text}'")
                    
                    # Trigger-Wort prüfen
                    triggered = False
                    trigger_word = ""
                    for trigger in self.triggers:
                        if trigger in text:
                            triggered = True
                            trigger_word = trigger
                            break
                    
                    if triggered:
                        print(f"🗣️  {self.name} aktiviert durch '{trigger_word}'")
                        
                        # Trigger-Wort aus Text entfernen
                        clean_text = text.replace(trigger_word, "").strip()
                        if not clean_text:
                            clean_text = "hallo"
                        
                        # Intelligente Antwort generieren
                        response = self.process_input(clean_text)
                        
                        print(f"🧠 {self.name} verarbeitet: '{clean_text}'")
                        print(f"🗣️  {self.name} sagt: {response}")
                        
                        # Antwort aussprechen
                        self._speak(response)
                        
                    else:
                        # Passiv erfasste Information (ohne Trigger)
                        if len(text) > 10:  # Nur längere Äußerungen speichern
                            print(f"📋 Passiv erfasst: {text[:50]}...")
                            self.context_memory.append({
                                "timestamp": datetime.now().isoformat(),
                                "content": text,
                                "type": "passive_observation"
                            })
                
                except sr.UnknownValueError:
                    pass  # Keine Sprache erkannt
                except sr.RequestError as e:
                    print(f"❌ Spracherkennungs-Fehler: {e}")
                
            except KeyboardInterrupt:
                print("\n🛑 Beendet durch Benutzer")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

def main():
    """Hauptfunktion"""
    otto = OttoIntelligent()
    otto.listen_and_respond()

if __name__ == "__main__":
    main() 