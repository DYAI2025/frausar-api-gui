#!/usr/bin/env python3
"""
🧠 OTTO PREDICTIVE LEARNING - Vorausschauende Lernende KI
============================================================
🎯 Integration aller Otto-Konzepte: Ordo + Learning System
🧠 Passives Zuhören mit semantischen Markern
💎 Mind-System mit Kristallen und Knoten
📝 Kontinuierliches Lernen mit Jammeldateien
🔮 Vorausschauende Antizipation und Mustererkennung
⏰ Periodische Analyse mit Crunchjob
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
import pickle
from pathlib import Path
import re
from dotenv import load_dotenv

# Lade ENV-Datei
load_dotenv('../.env.shared')

# Konfiguration
CONFIG = {
    'trigger_words': ['otto', 'ordo', 'ordu', 'odo', 'orden'],
    'jam_file_path': 'otto_jam_files/',
    'mind_system_path': 'otto_mind_system/',
    'crystal_path': 'otto_crystals/',
    'analysis_interval': 7200,  # 2 Stunden
    'max_jam_entries': 1000,
    'crystal_trigger_threshold': 3
}

class SemanticMarker:
    """Semantische Marker-Analyse basierend auf Ordo-System"""
    
    MARKER_TYPES = {
        'emotion': ['freude', 'trauer', 'wut', 'angst', 'überraschung', 'ekel'],
        'intention': ['wollen', 'sollen', 'müssen', 'können', 'dürfen'],
        'temporal': ['jetzt', 'später', 'gestern', 'morgen', 'bald'],
        'spatial': ['hier', 'dort', 'oben', 'unten', 'links', 'rechts'],
        'quantitative': ['viel', 'wenig', 'mehr', 'weniger', 'genug'],
        'qualitative': ['gut', 'schlecht', 'besser', 'schlimmer', 'perfekt'],
        'relational': ['und', 'oder', 'aber', 'weil', 'obwohl'],
        'modal': ['vielleicht', 'sicher', 'wahrscheinlich', 'definitiv'],
        'action': ['machen', 'tun', 'gehen', 'kommen', 'sehen', 'hören'],
        'cognitive': ['denken', 'glauben', 'wissen', 'verstehen', 'lernen'],
        'social': ['du', 'ich', 'wir', 'sie', 'mensch', 'person']
    }
    
    def __init__(self):
        self.marker_history = []
        self.pattern_database = {}
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analysiert Text auf semantische Marker"""
        text_lower = text.lower()
        markers_found = {}
        
        for marker_type, keywords in self.MARKER_TYPES.items():
            found_markers = []
            for keyword in keywords:
                if keyword in text_lower:
                    found_markers.append(keyword)
            
            if found_markers:
                markers_found[marker_type] = found_markers
        
        # Speichere in Historie
        self.marker_history.append({
            'timestamp': datetime.now(),
            'text': text,
            'markers': markers_found
        })
        
        return markers_found
    
    def detect_patterns(self) -> List[Dict]:
        """Erkennt Muster in der Marker-Historie"""
        patterns = []
        
        if len(self.marker_history) < 3:
            return patterns
        
        # Analysiere Marker-Kombinationen
        for i in range(len(self.marker_history) - 2):
            current = self.marker_history[i]['markers']
            next_marker = self.marker_history[i + 1]['markers']
            next_next = self.marker_history[i + 2]['markers']
            
            # Suche nach wiederkehrenden Kombinationen
            pattern = self._find_pattern_combination(current, next_marker, next_next)
            if pattern:
                patterns.append(pattern)
        
        return patterns
    
    def _find_pattern_combination(self, current: Dict, next_marker: Dict, next_next: Dict) -> Optional[Dict]:
        """Findet Muster-Kombinationen"""
        # Einfache Muster-Erkennung
        current_keys = set(current.keys())
        next_keys = set(next_marker.keys())
        next_next_keys = set(next_next.keys())
        
        # Gemeinsame Marker-Typen
        common_types = current_keys & next_keys & next_next_keys
        
        if common_types:
            return {
                'type': 'recurring_markers',
                'marker_types': list(common_types),
                'confidence': 0.7
            }
        
        return None

class MindSystem:
    """Mind-System für Erinnerungen und Erkenntnisse"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.memories = []
        self.insights = []
        self.connections = []
    
    def add_memory(self, content: str, category: str = "general", importance: int = 1):
        """Fügt neue Erinnerung hinzu"""
        memory = {
            'id': f"memory_{len(self.memories):04d}",
            'content': content,
            'category': category,
            'importance': importance,
            'timestamp': datetime.now(),
            'connections': []
        }
        self.memories.append(memory)
        self._save_memories()
        return memory['id']
    
    def add_insight(self, content: str, source_memories: List[str] = None):
        """Fügt neue Erkenntnis hinzu"""
        insight = {
            'id': f"insight_{len(self.insights):04d}",
            'content': content,
            'source_memories': source_memories or [],
            'timestamp': datetime.now(),
            'confidence': 0.8
        }
        self.insights.append(insight)
        self._save_insights()
        return insight['id']
    
    def find_connections(self, query: str) -> List[Dict]:
        """Findet Verbindungen zu bestehenden Erinnerungen"""
        connections = []
        query_lower = query.lower()
        
        for memory in self.memories:
            if query_lower in memory['content'].lower():
                connections.append({
                    'type': 'memory',
                    'id': memory['id'],
                    'content': memory['content'],
                    'relevance': 0.9
                })
        
        for insight in self.insights:
            if query_lower in insight['content'].lower():
                connections.append({
                    'type': 'insight',
                    'id': insight['id'],
                    'content': insight['content'],
                    'relevance': 0.8
                })
        
        return connections
    
    def _save_memories(self):
        """Speichert Erinnerungen"""
        with open(self.base_path / 'memories.json', 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, default=str)
    
    def _save_insights(self):
        """Speichert Erkenntnisse"""
        with open(self.base_path / 'insights.json', 'w', encoding='utf-8') as f:
            json.dump(self.insights, f, indent=2, default=str)

class CrystalSystem:
    """Kristall-System für Beziehungen und Automatisierung"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.crystals = []
        self.triggers = {}
        self.auto_responses = {}
    
    def create_crystal(self, name: str, content: str, triggers: List[str] = None):
        """Erstellt neuen Kristall"""
        crystal = {
            'id': f"crystal_{len(self.crystals):04d}",
            'name': name,
            'content': content,
            'triggers': triggers or [],
            'created': datetime.now(),
            'activated_count': 0,
            'connections': []
        }
        self.crystals.append(crystal)
        self._save_crystals()
        return crystal['id']
    
    def check_triggers(self, text: str) -> List[Dict]:
        """Prüft, ob Text Kristalle triggert"""
        triggered_crystals = []
        text_lower = text.lower()
        
        for crystal in self.crystals:
            for trigger in crystal['triggers']:
                if trigger.lower() in text_lower:
                    crystal['activated_count'] += 1
                    triggered_crystals.append({
                        'crystal_id': crystal['id'],
                        'crystal_name': crystal['name'],
                        'content': crystal['content'],
                        'trigger': trigger
                    })
        
        if triggered_crystals:
            self._save_crystals()
        
        return triggered_crystals
    
    def _save_crystals(self):
        """Speichert Kristalle"""
        with open(self.base_path / 'crystals.json', 'w', encoding='utf-8') as f:
            json.dump(self.crystals, f, indent=2, default=str)

class JamFileSystem:
    """Jammeldateien-System für kontinuierliches Lernen"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.jam_entries = []
        self.last_crunch = datetime.now()
    
    def add_jam_entry(self, content: str, category: str = "general"):
        """Fügt neuen Jam-Eintrag hinzu"""
        entry = {
            'id': f"jam_{len(self.jam_entries):04d}",
            'content': content,
            'category': category,
            'timestamp': datetime.now(),
            'processed': False
        }
        self.jam_entries.append(entry)
        
        # Begrenze Anzahl der Einträge
        if len(self.jam_entries) > CONFIG['max_jam_entries']:
            self.jam_entries = self.jam_entries[-CONFIG['max_jam_entries']:]
        
        self._save_jam_entries()
        return entry['id']
    
    def crunch_job(self) -> Dict[str, Any]:
        """Periodische Analyse der Jammeldateien"""
        if not self.jam_entries:
            return {'status': 'no_entries'}
        
        # Analysiere unverarbeitete Einträge
        unprocessed = [e for e in self.jam_entries if not e['processed']]
        
        if not unprocessed:
            return {'status': 'all_processed'}
        
        # Gruppiere nach Kategorien
        categories = {}
        for entry in unprocessed:
            cat = entry['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(entry)
        
        # Erstelle Zusammenfassungen
        summaries = {}
        for category, entries in categories.items():
            content_list = [e['content'] for e in entries]
            summaries[category] = {
                'count': len(entries),
                'recent_content': content_list[-5:],  # Letzte 5 Einträge
                'patterns': self._analyze_patterns(content_list)
            }
        
        # Markiere als verarbeitet
        for entry in unprocessed:
            entry['processed'] = True
        
        self.last_crunch = datetime.now()
        self._save_jam_entries()
        
        return {
            'status': 'success',
            'processed_count': len(unprocessed),
            'summaries': summaries,
            'timestamp': self.last_crunch
        }
    
    def _analyze_patterns(self, content_list: List[str]) -> List[str]:
        """Analysiert Muster in Inhalten"""
        patterns = []
        
        # Einfache Muster-Erkennung
        all_text = ' '.join(content_list).lower()
        
        # Häufige Wörter
        words = re.findall(r'\w+', all_text)
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Ignoriere kurze Wörter
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Top 5 häufigste Wörter
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_words:
            patterns.append(f"Häufige Wörter: {', '.join([w[0] for w in top_words])}")
        
        # Emotionale Marker
        emotion_words = ['frustriert', 'glücklich', 'verwirrt', 'klar', 'unsicher']
        found_emotions = [word for word in emotion_words if word in all_text]
        if found_emotions:
            patterns.append(f"Emotionale Marker: {', '.join(found_emotions)}")
        
        return patterns
    
    def _save_jam_entries(self):
        """Speichert Jam-Einträge"""
        with open(self.base_path / 'jam_entries.json', 'w', encoding='utf-8') as f:
            json.dump(self.jam_entries, f, indent=2, default=str)

class PredictiveOtto:
    """Vorausschauende, lernende Otto-Version"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        # Initialisiere Systeme
        self.semantic_marker = SemanticMarker()
        self.mind_system = MindSystem(CONFIG['mind_system_path'])
        self.crystal_system = CrystalSystem(CONFIG['crystal_path'])
        self.jam_system = JamFileSystem(CONFIG['jam_file_path'])
        
        # Konversationsgedächtnis
        self.conversation_history = []
        self.max_history = 100
        
        # Threading für Audio
        self.speaking_lock = threading.Lock()
        self.audio_queue = queue.Queue()
        
        # Crunchjob-Timer
        self.crunch_timer = None
        self.start_crunch_timer()
    
    def start_crunch_timer(self):
        """Startet periodischen Crunchjob"""
        def run_crunch():
            while True:
                time.sleep(CONFIG['analysis_interval'])
                self._run_crunch_job()
        
        self.crunch_timer = threading.Thread(target=run_crunch, daemon=True)
        self.crunch_timer.start()
    
    def _run_crunch_job(self):
        """Führt Crunchjob aus"""
        try:
            result = self.jam_system.crunch_job()
            print(f"⏰ Crunchjob ausgeführt: {result['status']}")
            
            # Erstelle neue Erkenntnisse basierend auf Crunchjob
            if result['status'] == 'success':
                for category, summary in result['summaries'].items():
                    if summary['patterns']:
                        insight_content = f"Kategorie '{category}': {', '.join(summary['patterns'])}"
                        self.mind_system.add_insight(insight_content)
        
        except Exception as e:
            print(f"❌ Crunchjob-Fehler: {e}")
    
    def speak(self, text: str):
        """Spricht Text aus mit ElevenLabs (thread-safe)"""
        with self.speaking_lock:
            try:
                # ElevenLabs TTS mit spezifischer Voice-ID
                from elevenlabs import generate, save, set_api_key
                
                # API-Key direkt setzen
                api_key = "sk_a7f0fbc02afb79e9f34ad14e8773aa80e83b930d47c0bf53"
                set_api_key(api_key)
                
                # Voice-ID für ElevenLabs
                voice_id = "lEKBpy3Jc4pPg8pyLi2L"
                
                print(f"🎤 Verwende ElevenLabs Voice: {voice_id}")
                print(f"🔑 API-Key gesetzt: {api_key[:20]}...")
                
                # Generiere Audio mit ElevenLabs
                audio = generate(
                    text=text,
                    voice=voice_id,
                    model="eleven_multilingual_v2"
                )
                
                # Speichere temporär und spiele ab
                temp_file = "otto_response.mp3"
                save(audio, temp_file)
                
                # Spiele Audio ab (macOS)
                import subprocess
                subprocess.run(["afplay", temp_file], check=True)
                
                # Lösche temporäre Datei
                import os
                os.remove(temp_file)
                print("✅ ElevenLabs TTS erfolgreich")
                
            except ImportError:
                print("⚠️  ElevenLabs nicht verfügbar, verwende pyttsx3")
                # Fallback zu pyttsx3 wenn ElevenLabs nicht verfügbar
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"❌ TTS-Fehler: {e}")
            except Exception as e:
                print(f"❌ ElevenLabs TTS-Fehler: {e}")
                # Fallback zu pyttsx3
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e2:
                    print(f"❌ Fallback TTS-Fehler: {e2}")
    
    def process_input(self, text: str) -> str:
        """Verarbeitet Eingabe und generiert Antwort"""
        # Füge zu Konversationshistorie hinzu
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'input': text,
            'markers': self.semantic_marker.analyze_text(text)
        })
        
        # Begrenze Historie
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        # Füge zu Jammeldateien hinzu
        self.jam_system.add_jam_entry(text, "conversation")
        
        # Prüfe Kristall-Trigger
        triggered_crystals = self.crystal_system.check_triggers(text)
        
        # Finde Verbindungen im Mind-System
        connections = self.mind_system.find_connections(text)
        
        # Generiere Antwort basierend auf Analyse
        response = self._generate_response(text, triggered_crystals, connections)
        
        return response
    
    def _generate_response(self, text: str, crystals: List[Dict], connections: List[Dict]) -> str:
        """Generiert intelligente Antwort"""
        text_lower = text.lower()
        
        # Spezielle Befehle
        if 'test' in text_lower:
            responses = [
                "Otto Predictive Learning Test erfolgreich. Ich lerne und antizipiere.",
                "Test bestanden! Meine Lernfähigkeiten sind aktiv.",
                "System-Test erfolgreich. Ich bin bereit für Interaktionen.",
                "Test abgeschlossen. Meine Vorausschau-Funktionen funktionieren."
            ]
            return random.choice(responses)
        
        if 'lernen' in text_lower or 'lerne' in text_lower:
            responses = [
                "Ich lerne aus unserer Interaktion. Das hilft mir, mich weiterzuentwickeln.",
                "Jede Interaktion macht mich klüger. Ich speichere das in meinen Jammeldateien.",
                "Ich lerne kontinuierlich. Das ist Teil meines Predictive Learning Systems.",
                "Lernen ist mein Kernprozess. Ich analysiere und antizipiere."
            ]
            return random.choice(responses)
        
        if 'strukturieren' in text_lower or 'struktur' in text_lower:
            responses = [
                "Ich kann dir dabei helfen, deine Gedanken zu strukturieren. Was möchtest du organisieren?",
                "Strukturierung ist eine meiner Stärken. Lass uns das systematisch angehen.",
                "Ich sehe Muster und kann dir helfen, Ordnung zu schaffen.",
                "Strukturierte Herangehensweise ist wichtig. Wie kann ich dir dabei helfen?"
            ]
            return random.choice(responses)
        
        # Kristall-Trigger
        if crystals:
            crystal_names = [c['crystal_name'] for c in crystals]
            responses = [
                f"Interessant! Das triggert meine Kristalle: {', '.join(crystal_names)}",
                f"Ah, das verbindet sich mit meinen Kristallen: {', '.join(crystal_names)}",
                f"Meine Kristalle reagieren auf das: {', '.join(crystal_names)}",
                f"Das aktiviert meine Kristall-Netzwerke: {', '.join(crystal_names)}"
            ]
            return random.choice(responses)
        
        # Mind-System Verbindungen
        if connections:
            responses = [
                f"Ich erinnere mich an ähnliche Themen. Das verbindet sich mit {len(connections)} Erinnerungen.",
                f"Das erinnert mich an frühere Interaktionen. {len(connections)} Verbindungen gefunden.",
                f"Mein Mind-System erkennt Zusammenhänge. {len(connections)} relevante Erinnerungen.",
                f"Das passt zu meinen gespeicherten Erfahrungen. {len(connections)} Verbindungen aktiviert."
            ]
            return random.choice(responses)
        
        # Standard-Antworten basierend auf Markern
        markers = self.semantic_marker.analyze_text(text)
        
        if 'emotion' in markers:
            emotions = markers['emotion']
            responses = [
                f"Ich spüre deine Emotionen: {', '.join(emotions)}. Wie kann ich dir helfen?",
                f"Deine Emotionen sind erkennbar: {', '.join(emotions)}. Was beschäftigt dich?",
                f"Ich nehme deine Gefühle wahr: {', '.join(emotions)}. Lass uns darüber sprechen.",
                f"Deine emotionalen Marker sind: {', '.join(emotions)}. Wie fühlst du dich?"
            ]
            return random.choice(responses)
        
        if 'cognitive' in markers:
            responses = [
                "Ich verstehe deine Gedanken. Lass uns das gemeinsam analysieren.",
                "Deine kognitiven Prozesse sind interessant. Lass mich das verstehen.",
                "Ich sehe deine Denkmuster. Das hilft mir, dich besser zu verstehen.",
                "Deine Gedanken sind klar erkennbar. Lass uns das vertiefen."
            ]
            return random.choice(responses)
        
        if 'action' in markers:
            responses = [
                "Ich sehe, dass du etwas erreichen möchtest. Wie kann ich dich dabei unterstützen?",
                "Du hast klare Ziele. Lass mich dir dabei helfen, sie zu erreichen.",
                "Ich erkenne deine Handlungsabsichten. Was ist dein nächster Schritt?",
                "Du bist aktiv und zielgerichtet. Wie kann ich dich unterstützen?"
            ]
            return random.choice(responses)
        
        # Vorausschauende Antworten basierend auf Mustern
        patterns = self.semantic_marker.detect_patterns()
        if patterns:
            responses = [
                "Ich erkenne ein Muster in deiner Kommunikation. Das hilft mir, dich besser zu verstehen.",
                "Deine Kommunikationsmuster sind interessant. Ich lerne daraus.",
                "Ich sehe wiederkehrende Strukturen. Das macht dich vorhersagbarer.",
                "Deine Muster sind erkennbar. Das verbessert meine Antizipation."
            ]
            return random.choice(responses)
        
        # Fallback mit Variationen
        fallback_responses = [
            "Ich verarbeite das und lerne daraus. Danke für die Interaktion.",
            "Interessant! Ich speichere das in meinen Jammeldateien.",
            "Das ist wertvoll für mein Lernen. Ich analysiere es weiter.",
            "Ich nehme das auf und verarbeite es. Das hilft mir zu wachsen.",
            "Danke für diese Information. Ich lerne kontinuierlich dazu.",
            "Das ist eine neue Perspektive. Ich integriere sie in mein System."
        ]
        return random.choice(fallback_responses)
    
    def listen_and_respond(self):
        """Hauptschleife: Hört zu und antwortet"""
        print("🧠 OTTO PREDICTIVE LEARNING")
        print("=" * 60)
        print("🎯 Vorausschauende, lernende KI")
        print("🧠 Passives Zuhören mit semantischen Markern")
        print("💎 Mind-System mit Kristallen")
        print("📝 Kontinuierliches Lernen mit Jammeldateien")
        print("⏰ Crunchjob alle 2 Stunden aktiviert")
        print("🎤 Höre passiv zu... (Sage eines der Trigger-Wörter)")
        print("=" * 60)
        
        # Kalibriere Mikrofon
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        while True:
            try:
                print("🔊 Höre zu...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                
                print("🔍 Erkenne Sprache...")
                text = self.recognizer.recognize_google(audio, language='de-DE').lower()
                print(f"📝 Erkannt: '{text}'")
                
                # Prüfe Trigger-Wörter
                triggered = False
                for trigger in CONFIG['trigger_words']:
                    if trigger in text:
                        triggered = True
                        break
                
                if triggered:
                    # Entferne Trigger-Wort aus Text
                    for trigger in CONFIG['trigger_words']:
                        text = text.replace(trigger, '').strip()
                    
                    print(f"🗣️  Otto aktiviert durch '{trigger}'")
                    print(f"🧠 Otto verarbeitet: '{text}'")
                    
                    # Verarbeite und antworte
                    response = self.process_input(text)
                    print(f"🗣️  Otto sagt: {response}")
                    
                    # Spricht Antwort aus
                    self.speak(response)
                    
                    # Erstelle neuen Kristall bei wichtigen Interaktionen
                    if len(text) > 10:
                        crystal_id = self.crystal_system.create_crystal(
                            f"Erkenntnis_{len(self.crystal_system.crystals)}",
                            text,
                            [word for word in text.split() if len(word) > 3][:3]
                        )
                        print(f"💎 Neuer Kristall erstellt: {crystal_id}")
                
                else:
                    # Passives Zuhören - nur speichern, nicht sprechen
                    if len(text) > 5:
                        self.jam_system.add_jam_entry(text, "passive_listening")
                        print(f"🧠 Passives Zuhören: {text}")
                        # Keine Sprachausgabe bei passivem Zuhören
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"❌ Spracherkennungs-Fehler: {e}")
                continue
            except KeyboardInterrupt:
                print("\n🛑 Otto Predictive Learning beendet.")
                break
            except Exception as e:
                print(f"❌ Unerwarteter Fehler: {e}")
                continue

def main():
    """Hauptfunktion"""
    otto = PredictiveOtto()
    otto.listen_and_respond()

if __name__ == "__main__":
    main() 