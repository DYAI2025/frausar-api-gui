#!/usr/bin/env python3
"""
OTTO - Intelligenter Task-Begleiter mit LLM-Integration
============================================================
🎯 Trigger-Wörter: otto, ordo, ordu, odo, orden
🧠 Echte LLM-Integration für dynamische Antworten
📋 Task-Management mit Kanban-System
🎤 Sprachsteuerung mit ElevenLabs oder pyttsx3
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
import json
import os
import yaml
from datetime import datetime
import requests
from typing import Optional, Dict, Any

class OttoIntelligentLLM:
    def __init__(self):
        self.trigger_words = ['otto', 'ordo', 'ordu', 'odo', 'orden']
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.conversation_history = []
        self.task_counter = 0
        self.tasks = {}
        
        # LLM-Konfiguration
        self.llm_endpoint = "http://localhost:11434/api/generate"  # Ollama
        self.fallback_responses = [
            "Ich verstehe. Lass mich das analysieren.",
            "Interessant. Was genau möchtest du damit erreichen?",
            "Das ist eine gute Frage. Lass mich nachdenken.",
            "Ich höre zu. Erzähl mir mehr.",
            "Verstehe. Wie kann ich dir dabei helfen?"
        ]
        
        # Konfiguration laden
        self.load_config()
        
    def load_config(self):
        """Lade Konfiguration aus YAML-Datei"""
        config_file = "otto_config.yaml"
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {
                'voice': {
                    'rate': 150,
                    'volume': 0.9
                },
                'llm': {
                    'model': 'qwen2.5:3b',
                    'temperature': 0.7,
                    'max_tokens': 200
                },
                'triggers': self.trigger_words
            }
            self.save_config()
    
    def save_config(self):
        """Speichere Konfiguration"""
        with open("otto_config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def setup_voice(self):
        """Konfiguriere Sprachausgabe"""
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        
        self.engine.setProperty('rate', self.config['voice']['rate'])
        self.engine.setProperty('volume', self.config['voice']['volume'])
    
    def speak(self, text: str):
        """Sprachausgabe mit Threading"""
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
        
        thread = threading.Thread(target=speak_thread)
        thread.start()
        return thread
    
    def get_llm_response(self, user_input: str) -> str:
        """Hole Antwort von lokalem LLM (Ollama)"""
        try:
            payload = {
                "model": self.config['llm']['model'],
                "prompt": f"""Du bist Otto, ein intelligenter, ruhiger Task-Begleiter. 
                Antworte kurz und hilfreich auf Deutsch.
                
                Benutzer: {user_input}
                Otto:""",
                "stream": False,
                "options": {
                    "temperature": self.config['llm']['temperature'],
                    "num_predict": self.config['llm']['max_tokens']
                }
            }
            
            response = requests.post(self.llm_endpoint, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return self.get_fallback_response()
                
        except Exception as e:
            print(f"❌ LLM-Fehler: {e}")
            return self.get_fallback_response()
    
    def get_fallback_response(self) -> str:
        """Fallback-Antwort wenn LLM nicht verfügbar"""
        import random
        return random.choice(self.fallback_responses)
    
    def process_command(self, text: str) -> str:
        """Verarbeite Benutzerbefehl intelligent"""
        text = text.lower().strip()
        
        # Spezielle Befehle erkennen
        if any(word in text for word in ['kanban', 'board', 'task', 'aufgabe']):
            return self.handle_task_management(text)
        elif any(word in text for word in ['struktur', 'organisier', 'ordne']):
            return self.handle_structure_request(text)
        elif any(word in text for word in ['erinner', 'speicher', 'lern']):
            return self.handle_memory_request(text)
        elif any(word in text for word in ['status', 'wie geht', 'funktioniert']):
            return self.handle_status_request(text)
        else:
            # Allgemeine Anfrage an LLM
            return self.get_llm_response(text)
    
    def handle_task_management(self, text: str) -> str:
        """Behandle Task-Management Befehle"""
        if 'erstellen' in text or 'hinzufügen' in text:
            self.task_counter += 1
            task_id = f"TASK_{self.task_counter:04d}"
            self.tasks[task_id] = {
                'title': text,
                'status': 'TODO',
                'created': datetime.now().isoformat()
            }
            return f"Task {task_id} erstellt: {text}"
        elif 'liste' in text or 'zeige' in text:
            if self.tasks:
                task_list = "\n".join([f"{k}: {v['title']} ({v['status']})" 
                                     for k, v in self.tasks.items()])
                return f"Aktuelle Tasks:\n{task_list}"
            else:
                return "Keine Tasks vorhanden."
        else:
            return self.get_llm_response(text)
    
    def handle_structure_request(self, text: str) -> str:
        """Behandle Strukturierungsanfragen"""
        return f"Ich helfe dir dabei, das zu strukturieren. Was genau soll ich organisieren?"
    
    def handle_memory_request(self, text: str) -> str:
        """Behandle Erinnerungsanfragen"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'input': text,
            'type': 'memory'
        })
        return "Ich habe das gespeichert und lerne daraus."
    
    def handle_status_request(self, text: str) -> str:
        """Behandle Status-Anfragen"""
        return f"Status: {len(self.tasks)} Tasks, {len(self.conversation_history)} Erinnerungen"
    
    def listen_for_trigger(self):
        """Höre nach Trigger-Wörtern"""
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
                        return text.replace(trigger, '').strip()
                
                return None
                
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print(f"❌ Spracherkennungsfehler: {e}")
                return None
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"❌ Mikrofon-Fehler: {e}")
            return None
    
    def run(self):
        """Hauptschleife"""
        print("🧠 OTTO - Intelligenter Task-Begleiter mit LLM")
        print("=" * 60)
        print(f"🎯 Trigger-Wörter: {', '.join(self.trigger_words)}")
        print("🧠 LLM-Integration: Aktiviert")
        print("📋 Task-Management: Aktiviert")
        print("🎤 Initialisiere Mikrofon...")
        
        self.setup_voice()
        print("✅ Mikrofon initialisiert")
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        self.is_listening = True
        
        while self.is_listening:
            try:
                print("🔊 Höre zu...")
                
                # Höre nach Trigger
                user_input = self.listen_for_trigger()
                
                if user_input:
                    print(f"🧠 Otto verarbeitet: '{user_input}'")
                    
                    # Verarbeite Befehl
                    response = self.process_command(user_input)
                    
                    # Sprachausgabe
                    print(f"🗣️  Otto sagt: {response}")
                    self.speak(response)
                    
                    # Speichere in Historie
                    self.conversation_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'input': user_input,
                        'response': response
                    })
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n⏹️  Otto wird beendet...")
                self.is_listening = False
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

if __name__ == "__main__":
    otto = OttoIntelligentLLM()
    otto.run() 