#!/usr/bin/env python3
"""
OTTO - Lokaler LLM-Begleiter mit Llama 3
============================================================
🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden
🧠 Lokales Llama 3-Modell auf http://192.168.178.47:1234
🎤 Sprachsteuerung mit pyttsx3
📋 Intelligente Antworten basierend auf lokaler LLM-Integration
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
import json
import os
import requests
from datetime import datetime
from typing import Optional, Dict, Any

class OttoLocalLLM:
    def __init__(self):
        self.trigger_words = ['otto', 'ordo', 'ordu', 'odo', 'orden']
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.conversation_history = []
        self.llm_endpoint = "http://192.168.178.47:1234/v1/chat/completions"
        
        # Konfiguriere Stimme
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Teste LLM-Verbindung
        self.test_llm_connection()
    
    def test_llm_connection(self):
        """Testet die Verbindung zum lokalen LLM"""
        try:
            test_prompt = {
                "model": "llama3",
                "messages": [
                    {"role": "user", "content": "Hallo, bist du da?"}
                ],
                "max_tokens": 50,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.llm_endpoint,
                json=test_prompt,
                timeout=5
            )
            
            if response.status_code == 200:
                print("✅ LLM-Verbindung erfolgreich")
                return True
            else:
                print(f"❌ LLM-Fehler: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ LLM-Verbindung fehlgeschlagen: {e}")
            return False
    
    def get_llm_response(self, user_input: str) -> str:
        """Holt eine Antwort vom lokalen LLM"""
        try:
            # Erstelle Kontext aus Gesprächsverlauf
            messages = [
                {"role": "system", "content": "Du bist Otto, ein hilfreicher, ruhiger und strukturierter Assistent. Antworte kurz und präzise auf Deutsch."}
            ]
            
            # Füge letzten Kontext hinzu
            if self.conversation_history:
                recent_history = self.conversation_history[-3:]  # Letzte 3 Nachrichten
                for msg in recent_history:
                    messages.append(msg)
            
            # Füge aktuelle Anfrage hinzu
            messages.append({"role": "user", "content": user_input})
            
            payload = {
                "model": "llama3",
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(
                self.llm_endpoint,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    llm_response = result['choices'][0]['message']['content'].strip()
                    
                    # Speichere in Gesprächsverlauf
                    self.conversation_history.append({"role": "user", "content": user_input})
                    self.conversation_history.append({"role": "assistant", "content": llm_response})
                    
                    # Begrenze Verlauf
                    if len(self.conversation_history) > 10:
                        self.conversation_history = self.conversation_history[-10:]
                    
                    return llm_response
                else:
                    return "Entschuldigung, ich konnte keine Antwort generieren."
            else:
                print(f"❌ LLM-Fehler: {response.status_code}")
                return "Entschuldigung, ich habe Probleme mit der Verbindung."
                
        except Exception as e:
            print(f"❌ LLM-Fehler: {e}")
            return "Entschuldigung, ich kann das gerade nicht verarbeiten."
    
    def speak(self, text: str):
        """Spricht den Text aus"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ Sprachfehler: {e}")
    
    def process_command(self, command: str) -> str:
        """Verarbeitet Befehle und gibt Antworten"""
        command_lower = command.lower().strip()
        
        # Einfache Befehle
        if any(word in command_lower for word in ['hallo', 'hi', 'hey']):
            return "Hallo! Ich bin Otto, dein lokaler Begleiter. Wie kann ich dir helfen?"
        
        elif any(word in command_lower for word in ['test', 'funktioniert']):
            return "Test erfolgreich! Ich bin bereit und verbunden."
        
        elif any(word in command_lower for word in ['status', 'zustand']):
            return "Ich bin online und verbunden mit dem lokalen LLM."
        
        elif any(word in command_lower for word in ['hilfe', 'help']):
            return "Ich kann dir bei Fragen helfen, Aufgaben strukturieren und mit dir sprechen. Was brauchst du?"
        
        # Komplexere Anfragen an LLM weiterleiten
        else:
            return self.get_llm_response(command)
    
    def listen_for_trigger(self):
        """Hört nach Trigger-Wörtern"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🔊 Höre zu...")
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                    print(f"📝 Erkannt: '{text}'")
                    
                    # Prüfe auf Trigger-Wörter
                    for trigger in self.trigger_words:
                        if trigger in text:
                            print(f"🗣️  Otto aktiviert durch '{trigger}'")
                            
                            # Entferne Trigger-Wort aus Text
                            clean_text = text.replace(trigger, '').strip()
                            if clean_text:
                                response = self.process_command(clean_text)
                            else:
                                response = "Ja, ich höre dich. Was kann ich für dich tun?"
                            
                            print(f"🗣️  Otto sagt: {response}")
                            self.speak(response)
                            return True
                    
                    return False
                    
                except sr.UnknownValueError:
                    return False
                except sr.RequestError as e:
                    print(f"❌ Spracherkennungsfehler: {e}")
                    return False
                    
        except Exception as e:
            print(f"❌ Hörfehler: {e}")
            return False
    
    def run(self):
        """Hauptschleife"""
        print("🧠 OTTO - Lokaler LLM-Begleiter")
        print("=" * 60)
        print("🎯 Trigger-Wörter:", ", ".join(self.trigger_words))
        print("🧠 Lokales Llama 3-Modell aktiviert")
        print("🎤 Initialisiere Mikrofon...")
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ Mikrofon initialisiert")
        except Exception as e:
            print(f"❌ Mikrofon-Fehler: {e}")
            return
        
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        self.is_listening = True
        
        while self.is_listening:
            try:
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
    otto = OttoLocalLLM()
    otto.run() 