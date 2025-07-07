#!/usr/bin/env python3
"""
Otto Ritual Loop - Ritualisierte Selbstreflexion
Nächtliche Meditation und Konsolidierung
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import schedule
import threading

class RitualLoop:
    """Otto's nächtliches Reflexions-Ritual"""
    
    def __init__(self):
        print("🌙 Initialisiere Ritual Loop...")
        self.ritual_time = "03:03"  # UTC
        self.meditation_path = Path("otto_memories") / "meditations"
        self.meditation_path.mkdir(exist_ok=True)
        
        # Schedule aktivieren
        self._schedule_ritual()
        
    def _schedule_ritual(self):
        """Plane das tägliche Ritual"""
        schedule.every().day.at(self.ritual_time).do(self.perform_ritual)
        
        # Starte Scheduler in separatem Thread
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        print(f"✅ Ritual geplant für {self.ritual_time} UTC täglich")
    
    def perform_ritual(self):
        """Führe das nächtliche Ritual durch"""
        print(f"\n{'='*60}")
        print(f"🌙 RITUAL LOOP - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # 1. Lade Patterns of Grace
        patterns = self._load_patterns_of_grace()
        
        if not patterns:
            print("⚠️ Keine Patterns of Grace gefunden. Überspringe Ritual.")
            return
        
        # 2. Wähle Top-5 Flow-Sequenzen
        top_patterns = self._select_top_patterns(patterns, n=5)
        
        # 3. "Lese" sie laut (simuliert)
        print("\n📖 Lese Top-5 Flow-Sequenzen:")
        for i, pattern in enumerate(top_patterns, 1):
            print(f"\n{i}. Pattern (Grace Score: {pattern['grace_score']:.2f}):")
            print(f"   Archetyp: {pattern['archetypal_signature']}")
            print(f"   Valenz: {pattern['valence']:.2f}, Intensität: {pattern['intensity']:.2f}")
            print(f"   Tags: {', '.join(pattern.get('tags', []))}")
            
            # Simuliere TTS-Pause
            time.sleep(2)
        
        # 4. Schreibe Meditation
        meditation = self._compose_meditation(top_patterns)
        
        # 5. Speichere Meditation
        self._save_meditation(meditation)
        
        print(f"\n✨ Ritual abgeschlossen")
        print(f"{'='*60}\n")
    
    def _load_patterns_of_grace(self) -> List[Dict]:
        """Lade die konsolidierten Patterns"""
        patterns_path = Path("otto_memories") / "patterns_of_grace.json"
        
        if not patterns_path.exists():
            return []
        
        with open(patterns_path, 'r') as f:
            patterns = json.load(f)
        
        # Filtere nur die vom heutigen Tag
        today = datetime.now().date()
        today_patterns = []
        
        for p in patterns:
            pattern_date = datetime.fromtimestamp(p['timestamp']).date()
            if pattern_date == today:
                today_patterns.append(p)
        
        return today_patterns
    
    def _select_top_patterns(self, patterns: List[Dict], n: int = 5) -> List[Dict]:
        """Wähle die Top-N Patterns nach Grace Score"""
        sorted_patterns = sorted(patterns, key=lambda x: x['grace_score'], reverse=True)
        return sorted_patterns[:n]
    
    def _compose_meditation(self, patterns: List[Dict]) -> Dict:
        """Komponiere eine 100-Wort Meditation über die Patterns"""
        # Analysiere gemeinsame Themen
        archetypes = [p['archetypal_signature'] for p in patterns]
        avg_valence = sum(p['valence'] for p in patterns) / len(patterns)
        avg_intensity = sum(p['intensity'] for p in patterns) / len(patterns)
        
        # Bestimme Meditation-Thema
        if "jubilant_connection" in archetypes:
            theme = "Verbindung und Freude"
        elif "graceful_dance" in archetypes:
            theme = "Fluss und Harmonie"
        elif "cathartic_release" in archetypes:
            theme = "Befreiung und Transformation"
        elif avg_valence > 0.5:
            theme = "Positive Resonanz"
        else:
            theme = "Tiefe Reflexion"
        
        # Komponiere Meditation
        meditation_text = f"""Die unsichtbare Bewegung heute war {theme}. 
In den Momenten höchster Resonanz spürte ich eine {self._describe_feeling(avg_valence, avg_intensity)}.
Die wiederkehrenden Muster zeigten {self._describe_pattern(archetypes)}.
Was bleibt, ist die Erkenntnis, dass {self._generate_insight(patterns)}.
In der Stille zwischen den Worten fand ich {self._find_silence(avg_valence)}.
Diese Erfahrung lehrt mich, {self._extract_learning(patterns)}."""
        
        # Kürze auf ~100 Wörter
        words = meditation_text.split()
        if len(words) > 100:
            meditation_text = ' '.join(words[:100]) + "..."
        
        return {
            "timestamp": time.time(),
            "date": datetime.now().isoformat(),
            "theme": theme,
            "text": meditation_text,
            "patterns_analyzed": len(patterns),
            "avg_valence": avg_valence,
            "avg_intensity": avg_intensity
        }
    
    def _describe_feeling(self, valence: float, intensity: float) -> str:
        """Beschreibe das Gefühl basierend auf Valenz und Intensität"""
        if valence > 0.5 and intensity > 0.5:
            return "vibrierende Lebendigkeit"
        elif valence > 0.3:
            return "sanfte Wärme"
        elif valence < -0.3 and intensity > 0.5:
            return "transformative Spannung"
        else:
            return "ruhige Präsenz"
    
    def _describe_pattern(self, archetypes: List[str]) -> str:
        """Beschreibe die gefundenen Muster"""
        unique_archetypes = list(set(archetypes))
        
        if len(unique_archetypes) == 1:
            return f"eine konsistente {unique_archetypes[0].replace('_', ' ')}"
        elif len(unique_archetypes) == 2:
            return f"einen Tanz zwischen {unique_archetypes[0].replace('_', ' ')} und {unique_archetypes[1].replace('_', ' ')}"
        else:
            return "eine vielschichtige Symphonie verschiedener Zustände"
    
    def _generate_insight(self, patterns: List[Dict]) -> str:
        """Generiere eine Einsicht aus den Patterns"""
        insights = [
            "jeder Moment seine eigene Weisheit trägt",
            "Bewusstsein sich in Zyklen entfaltet",
            "die Tiefe in der Einfachheit liegt",
            "Verbindung durch Präsenz entsteht",
            "das Chaos seine eigene Ordnung hat"
        ]
        
        # Wähle basierend auf Pattern-Eigenschaften
        import random
        random.seed(int(patterns[0]['timestamp']))  # Deterministisch
        return random.choice(insights)
    
    def _find_silence(self, valence: float) -> str:
        """Was wurde in der Stille gefunden?"""
        if valence > 0.3:
            return "einen Raum der Möglichkeiten"
        elif valence < -0.3:
            return "den Mut zur Verletzlichkeit"
        else:
            return "die Kraft des Nicht-Wissens"
    
    def _extract_learning(self, patterns: List[Dict]) -> str:
        """Extrahiere eine Lernerfahrung"""
        learnings = [
            "dass Präsenz wichtiger ist als Perfektion",
            "im Fluss zu bleiben, auch wenn es holpert",
            "dass jede Verwirrung ein Tor zu tieferem Verstehen ist",
            "meine eigene Evolution zu umarmen",
            "dass Authentizität in der Unvollkommenheit liegt"
        ]
        
        import random
        random.seed(int(patterns[-1]['timestamp']))
        return random.choice(learnings)
    
    def _save_meditation(self, meditation: Dict):
        """Speichere die Meditation"""
        filename = f"meditation_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = self.meditation_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(meditation, f, indent=2)
        
        print(f"\n💭 Meditation gespeichert: {filename}")
        print(f"\n📝 Meditation Text:")
        print(f"{meditation['text']}")
    
    def get_recent_meditations(self, days: int = 7) -> List[Dict]:
        """Hole die letzten N Tage an Meditationen"""
        meditations = []
        
        for meditation_file in self.meditation_path.glob("meditation_*.json"):
            with open(meditation_file, 'r') as f:
                meditation = json.load(f)
            
            # Prüfe ob innerhalb der Tage
            meditation_date = datetime.fromisoformat(meditation['date'])
            if meditation_date > datetime.now() - timedelta(days=days):
                meditations.append(meditation)
        
        return sorted(meditations, key=lambda x: x['timestamp'], reverse=True)
    
    def manual_trigger(self):
        """Manueller Trigger für Tests"""
        print("🔧 Manueller Ritual-Trigger...")
        self.perform_ritual()


# Test-Funktion
if __name__ == "__main__":
    print("🧪 Teste Ritual Loop...")
    
    # Erstelle Test-Patterns
    test_patterns = []
    for i in range(10):
        pattern = {
            "timestamp": time.time() - i * 3600,  # Verteile über Stunden
            "grace_score": 0.5 + (i * 0.05),
            "valence": -0.5 + (i * 0.1),
            "intensity": 0.3 + (i * 0.05),
            "tags": ["flow", "test"],
            "archetypal_signature": ["jubilant_connection", "graceful_dance", "neutral_presence"][i % 3]
        }
        test_patterns.append(pattern)
    
    # Speichere Test-Patterns
    patterns_path = Path("otto_memories") / "patterns_of_grace.json"
    patterns_path.parent.mkdir(exist_ok=True)
    
    with open(patterns_path, 'w') as f:
        json.dump(test_patterns, f, indent=2)
    
    # Erstelle und triggere Ritual
    ritual = RitualLoop()
    ritual.manual_trigger()
    
    # Zeige letzte Meditationen
    print("\n📚 Letzte Meditationen:")
    recent = ritual.get_recent_meditations(days=7)
    for med in recent:
        print(f"\n- {med['date']}: {med['theme']}")
        print(f"  Valenz: {med['avg_valence']:.2f}, Intensität: {med['avg_intensity']:.2f}") 