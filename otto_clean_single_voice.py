#!/usr/bin/env python3
"""
OTTO - Saubere Version mit lokaler LLM-Integration
============================================================
🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden
🧠 Lokales LLM auf http://192.168.178.47:1234
🎤 Nur eine Stimme (pyttsx3)
📋 Intelligente Antworten basierend auf LLM
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any

class OttoCleanSingleVoice:
    def __init__(self):
        self.trigger_words = ['otto', 'ordo', 'ordu', 'odo', 'orden']
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.conversation_history = []
        self.llm_url = "http://192.168.178.47:1234/v1/chat/completions"
        
        # Konfiguriere Stimme
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)
        
        # Teste LLM-Verbindung
        self.test_llm_connection()
    
    def test_llm_connection(self):
        """Testet die Verbindung zum lokalen LLM"""
        try:
            test_prompt = {
                "model": "llama3.1:8b",
                "messages": [{"role": "user", "content": "Hallo"}],
                "max_tokens": 50,
                "temperature": 0.7
            }
            response = requests.post(self.llm_url, json=test_prompt, timeout=5)
            if response.status_code == 200:
                print("✅ LLM-Verbindung erfolgreich")
            else:
                print("⚠️  LLM-Verbindung fehlgeschlagen")
        except Exception as e:
            print(f"❌ LLM-Verbindungsfehler: {e}")
    
    def speak(self, text: str):
        """Spricht Text aus (nur eine Stimme)"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ Sprachfehler: {e}")
    
    def get_llm_response(self, user_input: str) -> str:
        """Holt Antwort vom lokalen LLM"""
        try:
            # Erstelle Kontext aus Gesprächsverlauf
            messages = [
                {"role": "system", "content": "Du bist Otto, ein hilfreicher und intelligenter Assistent. Antworte kurz und präzise auf Deutsch."}
            ]
            
            # Füge letzten Kontext hinzu
            if self.conversation_history:
                messages.extend(self.conversation_history[-2:])  # Nur letzte 2 Nachrichten
            
            messages.append({"role": "user", "content": user_input})
            
            payload = {
                "model": "llama3.1:8b",
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(self.llm_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    llm_response = result['choices'][0]['message']['content'].strip()
                    
                    # Speichere in Gesprächsverlauf
                    self.conversation_history.append({"role": "user", "content": user_input})
                    self.conversation_history.append({"role": "assistant", "content": llm_response})
                    
                    # Begrenze Verlauf
                    if len(self.conversation_history) > 6:
                        self.conversation_history = self.conversation_history[-6:]
                    
                    return llm_response
                else:
                    return "Entschuldigung, ich konnte das nicht verarbeiten."
            else:
                return "Ich habe Probleme mit der Verbindung zum LLM."
                
        except Exception as e:
            print(f"❌ LLM-Fehler: {e}")
            return "Entschuldigung, ich kann das gerade nicht verarbeiten."
    
    def process_command(self, text: str) -> str:
        """Verarbeitet Benutzerbefehle"""
        text = text.lower().strip()
        
        # Entferne Trigger-Wort
        for trigger in self.trigger_words:
            text = text.replace(trigger, '').strip()
        
        if not text:
            return "Ja, ich höre dich. Wie kann ich dir helfen?"
        
        # Hole Antwort vom LLM
        return self.get_llm_response(text)
    
    def listen_for_trigger(self):
        """Hört nach Trigger-Wörtern"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
            try:
                text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                print(f"📝 Erkannt: '{text}'")
                
                # Prüfe auf Trigger-Wörter
                for trigger in self.trigger_words:
                    if trigger in text:
                        print(f"🗣️  Otto aktiviert durch '{trigger}'")
                        response = self.process_command(text)
                        print(f"🧠 Otto sagt: {response}")
                        self.speak(response)
                        return True
                
                return False
                
            except sr.UnknownValueError:
                return False
            except sr.RequestError as e:
                print(f"❌ Spracherkennungsfehler: {e}")
                return False
                
        except Exception as e:
            return False
    
    def run(self):
        """Hauptschleife"""
        print("🧠 OTTO - Saubere Version mit lokaler LLM-Integration")
        print("=" * 60)
        print("🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden")
        print("🧠 Lokales LLM auf http://192.168.178.47:1234")
        print("🎤 Nur eine Stimme (pyttsx3)")
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        self.is_listening = True
        
        while self.is_listening:
            try:
                print("🔊 Höre zu...")
                self.listen_for_trigger()
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n🛑 Otto wird beendet...")
                self.is_listening = False
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

if __name__ == "__main__":
    otto = OttoCleanSingleVoice()
    otto.run() 