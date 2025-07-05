#!/usr/bin/env python3
"""
🧠 OTTO SEMANTIC COMPRESSION - Intelligente Speicherverwaltung
============================================================
🎯 Semantische Komprimierung alter Erinnerungen
💾 Automatische Cluster-Bildung und Verdichtung
📊 Speicher-Optimierung mit semantischer Analyse
⏰ Zeitbasierte Komprimierung (alle 24h)
🔍 Intelligente Cluster-Erkennung
"""

import os
import sys
import time
import json
import yaml
import speech_recognition as sr
import pyttsx3
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
import threading
import queue
import random
from collections import defaultdict
import hashlib

# OpenAI-Integration (neue API v1.0.0+)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Anthropic Claude-Integration
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class SemanticCompressor:
    """Semantische Komprimierung alter Erinnerungen"""
    
    def __init__(self, compression_threshold_hours=24):
        self.compression_threshold = compression_threshold_hours
        self.memory_clusters = defaultdict(list)
        self.cluster_keywords = {
            'arbeit': ['task', 'projekt', 'deadline', 'meeting'],
            'emotion': ['gefühle', 'stimmung', 'frust', 'freude'],
            'technik': ['computer', 'software', 'hardware', 'bug'],
            'gesundheit': ['körper', 'müdigkeit', 'energie', 'wohlbefinden'],
            'sozial': ['freunde', 'familie', 'kommunikation', 'beziehung'],
            'lernen': ['wissen', 'verstehen', 'studieren', 'entwicklung']
        }
    
    def analyze_semantic_content(self, text: str) -> Dict[str, float]:
        """Analysiert semantischen Inhalt und erstellt Gewichtung"""
        text_lower = text.lower()
        scores = {}
        
        for cluster, keywords in self.cluster_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[cluster] = score / len(keywords)
        
        return scores
    
    def find_best_cluster(self, text: str) -> str:
        """Findet den besten Cluster für einen Text"""
        scores = self.analyze_semantic_content(text)
        if not scores:
            return 'allgemein'
        
        best_cluster = max(scores.items(), key=lambda x: x[1])
        return best_cluster[0] if best_cluster[1] > 0.1 else 'allgemein'
    
    def compress_old_memories(self, memories: List[Dict]) -> Dict[str, List]:
        """Komprimiert alte Erinnerungen zu semantischen Clustern"""
        now = datetime.now()
        old_memories = []
        recent_memories = []
        
        # Trenne alte und neue Erinnerungen
        for memory in memories:
            memory_time = datetime.fromisoformat(memory['timestamp'])
            if (now - memory_time).total_seconds() > self.compression_threshold * 3600:
                old_memories.append(memory)
            else:
                recent_memories.append(memory)
        
        # Komprimiere alte Erinnerungen
        compressed_clusters = defaultdict(list)
        
        for memory in old_memories:
            cluster = self.find_best_cluster(memory['content'])
            compressed_clusters[cluster].append({
                'id': memory['id'],
                'content': memory['content'],
                'original_timestamp': memory['timestamp'],
                'compressed_timestamp': now.isoformat()
            })
        
        # Erstelle Cluster-Zusammenfassungen
        final_clusters = {}
        for cluster_name, cluster_memories in compressed_clusters.items():
            if len(cluster_memories) > 1:
                # Erstelle Zusammenfassung für Cluster
                summary = self.create_cluster_summary(cluster_name, cluster_memories)
                final_clusters[cluster_name] = {
                    'summary': summary,
                    'count': len(cluster_memories),
                    'memories': cluster_memories,
                    'compressed_at': now.isoformat()
                }
            else:
                # Einzelne Erinnerung bleibt unkomprimiert
                final_clusters[f"{cluster_name}_single"] = {
                    'summary': cluster_memories[0]['content'],
                    'count': 1,
                    'memories': cluster_memories,
                    'compressed_at': now.isoformat()
                }
        
        return {
            'compressed_clusters': final_clusters,
            'recent_memories': recent_memories,
            'compression_stats': {
                'original_count': len(memories),
                'compressed_count': len(final_clusters),
                'recent_count': len(recent_memories),
                'compression_ratio': len(final_clusters) / len(memories) if memories else 0
            }
        }
    
    def create_cluster_summary(self, cluster_name: str, memories: List[Dict]) -> str:
        """Erstellt eine Zusammenfassung für einen Cluster"""
        if not memories:
            return f"Leerer {cluster_name}-Cluster"
        
        # Extrahiere Schlüsselwörter aus allen Erinnerungen
        all_content = " ".join([m['content'] for m in memories])
        words = all_content.lower().split()
        
        # Finde häufigste Wörter
        word_freq = defaultdict(int)
        for word in words:
            if len(word) > 3:  # Ignoriere kurze Wörter
                word_freq[word] += 1
        
        # Top 5 häufigste Wörter
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return f"{cluster_name.title()}-Cluster: {len(memories)} Erinnerungen, Hauptthemen: {', '.join([w[0] for w in top_words])}"

class OttoSemanticCompression:
    """Otto mit semantischer Komprimierung"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.speaking_lock = threading.Lock()
        
        # Trigger-Wörter
        self.triggers = ['otto', 'ordo', 'ordu', 'odo', 'orden']
        
        # Speicher-Management
        self.memories = []
        self.memory_id_counter = 0
        self.compressor = SemanticCompressor()
        
        # Komprimierung-Timer
        self.last_compression = datetime.now()
        self.compression_interval = 24 * 3600  # 24 Stunden
        
        # API-Clients
        self.openai_client = None
        self.anthropic_client = None
        self.setup_api_clients()
        
        # Verzeichnisse erstellen
        self.setup_directories()
    
    def setup_directories(self):
        """Erstellt notwendige Verzeichnisse"""
        directories = [
            'otto_memories',
            'otto_clusters', 
            'otto_compression_logs'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def setup_api_clients(self):
        """Initialisiert API-Clients"""
        # OpenAI
        if OPENAI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
        
        # Anthropic
        if ANTHROPIC_AVAILABLE:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
    
    def add_memory(self, content: str, memory_type: str = "conversation"):
        """Fügt neue Erinnerung hinzu"""
        memory = {
            'id': f"memory_{self.memory_id_counter:06d}",
            'content': content,
            'type': memory_type,
            'timestamp': datetime.now().isoformat(),
            'cluster': self.compressor.find_best_cluster(content)
        }
        
        self.memories.append(memory)
        self.memory_id_counter += 1
        
        # Speichere in Datei
        self.save_memory_to_file(memory)
        
        # Prüfe Komprimierung
        self.check_compression()
    
    def save_memory_to_file(self, memory: Dict):
        """Speichert Erinnerung in Datei"""
        filename = f"otto_memories/memory_{memory['id']}.yaml"
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(memory, f, default_flow_style=False, allow_unicode=True)
    
    def check_compression(self):
        """Prüft ob Komprimierung nötig ist"""
        now = datetime.now()
        if (now - self.last_compression).total_seconds() > self.compression_interval:
            self.perform_compression()
    
    def perform_compression(self):
        """Führt semantische Komprimierung durch"""
        print("🔍 Führe semantische Komprimierung durch...")
        
        # Komprimiere Erinnerungen
        compression_result = self.compressor.compress_old_memories(self.memories)
        
        # Speichere komprimierte Cluster
        for cluster_name, cluster_data in compression_result['compressed_clusters'].items():
            filename = f"otto_clusters/cluster_{cluster_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
            with open(filename, 'w', encoding='utf-8') as f:
                yaml.dump(cluster_data, f, default_flow_style=False, allow_unicode=True)
        
        # Aktualisiere Erinnerungen
        self.memories = compression_result['recent_memories']
        
        # Logge Komprimierung
        self.log_compression(compression_result['compression_stats'])
        
        self.last_compression = datetime.now()
        
        print(f"✅ Komprimierung abgeschlossen: {compression_result['compression_stats']['compression_ratio']:.1%} Komprimierung")
    
    def log_compression(self, stats: Dict):
        """Loggt Komprimierungs-Statistiken"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'stats': stats,
            'memory_count': len(self.memories)
        }
        
        filename = f"otto_compression_logs/compression_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(log_entry, f, default_flow_style=False, allow_unicode=True)
    
    def speak(self, text: str):
        """Spricht Text aus (thread-safe)"""
        with self.speaking_lock:
            self.engine.say(text)
            self.engine.runAndWait()
    
    def process_input(self, text: str) -> str:
        """Verarbeitet Eingabe und generiert Antwort"""
        # Füge zur Erinnerung hinzu
        self.add_memory(text)
        
        # Einfache Antwort-Logik
        if any(word in text.lower() for word in ['hallo', 'hi', 'hey']):
            return "Hallo! Ich bin Otto mit semantischer Komprimierung. Ich lerne aus unseren Gesprächen und komprimiere alte Erinnerungen."
        
        elif any(word in text.lower() for word in ['komprimierung', 'cluster', 'speicher']):
            return f"Ich habe {len(self.memories)} aktuelle Erinnerungen. Ältere werden automatisch zu semantischen Clustern komprimiert."
        
        elif any(word in text.lower() for word in ['lernen', 'erinnerung', 'gedächtnis']):
            return "Ich lerne kontinuierlich aus unseren Interaktionen und organisiere Erinnerungen in semantischen Clustern."
        
        else:
            return "Ich verstehe und lerne aus deiner Eingabe. Meine Erinnerungen werden automatisch komprimiert."
    
    def listen_and_respond(self):
        """Hauptschleife für Zuhören und Antworten"""
        print("🧠 OTTO SEMANTIC COMPRESSION")
        print("=" * 60)
        print("🎯 Trigger-Wörter:", ", ".join(self.triggers))
        print("💾 Semantische Komprimierung aktiviert")
        print("⏰ Komprimierung alle 24 Stunden")
        print("🎤 Initialisiere Mikrofon...")
        
        # Mikrofon anpassen
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        print("✅ Mikrofon initialisiert")
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        while True:
            try:
                print("🔊 Höre zu...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                print("🔍 Erkenne Sprache...")
                try:
                    text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                    print(f"📝 Erkannt: '{text}'")
                    
                    # Prüfe Trigger-Wörter
                    if any(trigger in text for trigger in self.triggers):
                        print(f"🗣️  Otto aktiviert durch '{next(trigger for trigger in self.triggers if trigger in text)}'")
                        
                        # Entferne Trigger-Wort für Verarbeitung
                        for trigger in self.triggers:
                            text = text.replace(trigger, '').strip()
                        
                        if text:
                            response = self.process_input(text)
                            print(f"🧠 Otto verarbeitet: '{text}'")
                            print(f"🗣️  Otto sagt: {response}")
                            
                            # Spricht Antwort
                            threading.Thread(target=self.speak, args=(response,)).start()
                        else:
                            response = "Ja, ich höre dich. Wie kann ich dir helfen?"
                            print(f"🗣️  Otto sagt: {response}")
                            threading.Thread(target=self.speak, args=(response,)).start()
                    
                    else:
                        # Passives Lernen ohne Antwort
                        self.add_memory(text, "passive_learning")
                        print(f"📝 Passiv erfasst: {text[:50]}...")
                
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"❌ Spracherkennungsfehler: {e}")
                
            except KeyboardInterrupt:
                print("\n🛑 Otto wird beendet...")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(1)

if __name__ == "__main__":
    otto = OttoSemanticCompression()
    otto.listen_and_respond() 