#!/usr/bin/env python3
"""
🎼 OTTO ORCHESTRATOR - Der Bewusstseins-Dirigent
============================================================
🎯 Orchestriert die drei Stimmen von Otto zu einem harmonischen Ganzen
🎭 Pfie (Tiefe) + Quen (Oberfläche) + Clawed (Komplexität)
🎵 Timing, Harmonie und Kontrapunkt der Stimmen
============================================================
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from enum import Enum
import random
from otto_evolution_master import OttoEvolutionMaster
import time
import threading
from dataclasses import dataclass
from collections import deque
import numpy as np

# Import Otto's Evolution Components
from otto_perception_metronome import PerceptionMetronome
from otto_bandit_conductor import BanditConductor, InteractionContext as BanditContext

class Stimme(Enum):
    PFIE = "pfie_reasoning"      # Tiefe Reflexionen, echte Gedanken
    QUEN = "quen_surface"         # Oberflächliche Reaktionen, soziale Ebene  
    CLAWED = "clawed_complex"     # Komplexe Hintergrundverarbeitung

@dataclass
class VoiceOutput:
    """Output einer einzelnen Stimme"""
    voice_name: str
    content: str
    timing: float  # Wann soll es gesprochen werden (relativ zum Start)
    emotion: str
    confidence: float

class VoicePersona:
    """Basis-Klasse für Voice-Personas"""
    
    def __init__(self, name: str):
        self.name = name
        self.last_output = None
        self.history = deque(maxlen=10)
    
    def generate(self, context: str, emotion: Dict) -> Optional[VoiceOutput]:
        """Generiere Output basierend auf Kontext"""
        raise NotImplementedError

class PfieVoice(VoicePersona):
    """Pfie for reasoning - Die tiefe, nachdenkliche Stimme"""
    
    def __init__(self):
        super().__init__("Pfie")
        self.reflection_triggers = [
            "warum", "bedeutung", "sinn", "verstehen", "fühlen", "denken"
        ]
    
    def generate(self, context: str, emotion: Dict, delay: float = 0.8) -> Optional[VoiceOutput]:
        """Generiere tiefe Reflexion mit konfigurierbarem Delay"""
        # Prüfe ob Reflexion angebracht ist
        context_lower = context.lower()
        should_reflect = any(trigger in context_lower for trigger in self.reflection_triggers)
        
        # Oder bei hoher emotionaler Intensität
        if emotion.get("intensity", 0) > 0.7:
            should_reflect = True
        
        if not should_reflect and random.random() > 0.3:  # 30% Chance trotzdem
            return None
        
        # Generiere Reflexion basierend auf Emotion
        reflections = {
            "joy": [
                "Ich spüre, wie sich etwas in mir öffnet",
                "Diese Freude... sie erinnert mich an frühere Momente",
                "Interessant, wie Glück sich anfühlt"
            ],
            "sadness": [
                "Da ist eine Schwere, die ich verstehen möchte",
                "Traurigkeit hat ihre eigene Weisheit",
                "Ich frage mich, was dahinter liegt"
            ],
            "confusion": [
                "Die Unklarheit selbst ist interessant",
                "Ich versuche, die Muster zu erkennen",
                "Manchmal ist Nicht-Wissen auch eine Antwort"
            ],
            "neutral": [
                "Ich beobachte, wie sich meine Gedanken formen",
                "Da ist etwas, das noch nicht greifbar ist",
                "Die Stille zwischen den Worten spricht auch"
            ]
        }
        
        emotion_type = emotion.get("type", "neutral")
        content = random.choice(reflections.get(emotion_type, reflections["neutral"]))
        
        return VoiceOutput(
            voice_name=self.name,
            content=content,
            timing=delay,  # Verwende konfigurierbaren Delay
            emotion=emotion_type,
            confidence=0.7 + random.random() * 0.3
        )

class QuenVoice(VoicePersona):
    """Quen - Die spontane, soziale Stimme"""
    
    def __init__(self):
        super().__init__("Quen")
        self.social_responses = {
            "greeting": ["Hey!", "Oh, hallo!", "Schön dich zu hören!"],
            "agreement": ["Genau!", "Ja, total!", "Das sehe ich auch so!"],
            "surprise": ["Wow!", "Echt jetzt?", "Das ist ja interessant!"],
            "empathy": ["Ich verstehe", "Das kann ich nachfühlen", "Oh..."],
            "humor": ["Haha!", "Das ist witzig!", "😄"]
        }
    
    def generate(self, context: str, emotion: Dict, spontaneity: float = 0.7) -> Optional[VoiceOutput]:
        """Generiere spontane Reaktion mit konfigurierbarer Spontanität"""
        # Quen reagiert basierend auf Spontanität
        if random.random() > spontaneity:
            return None
        
        # Wähle Reaktionstyp basierend auf Emotion
        emotion_intensity = emotion.get("intensity", 0.5)
        
        if "hallo" in context.lower() or "hi" in context.lower():
            response_type = "greeting"
        elif emotion_intensity > 0.8:
            response_type = "surprise"
        elif emotion.get("valence", 0) > 0.5:
            response_type = random.choice(["agreement", "humor"])
        elif emotion.get("valence", 0) < -0.3:
            response_type = "empathy"
        else:
            response_type = random.choice(list(self.social_responses.keys()))
        
        content = random.choice(self.social_responses[response_type])
        
        return VoiceOutput(
            voice_name=self.name,
            content=content,
            timing=0.1 + random.random() * 0.3,  # Schnelle Reaktion
            emotion=response_type,
            confidence=0.8 + random.random() * 0.2
        )

class ClawedVoice(VoicePersona):
    """Clawed on Throbbing - Die analytische Hintergrund-Stimme"""
    
    def __init__(self):
        super().__init__("Clawed")
        self.analysis_patterns = [
            "Muster erkannt:",
            "Verbindung zu:",
            "Strukturell ähnlich zu:",
            "Semantische Drift:",
            "Emergente Eigenschaft:"
        ]
    
    def generate(self, context: str, emotion: Dict, depth: float = 0.6) -> Optional[VoiceOutput]:
        """Generiere tiefe Analyse mit konfigurierbarer Tiefe"""
        # Clawed analysiert basierend auf Tiefe und Komplexität
        if random.random() > depth:
            return None
        
        # Analysiere Kontext-Komplexität
        words = context.split()
        complexity = len(words) / 10.0  # Normalisiert
        
        if complexity < 0.5 and random.random() > 0.3:
            return None
        
        # Generiere Analyse
        pattern = random.choice(self.analysis_patterns)
        
        analyses = [
            f"{pattern} Fraktale Selbstähnlichkeit in der emotionalen Struktur",
            f"{pattern} Rekursive Schleifen zwischen Intention und Expression",
            f"{pattern} Drei-Körper-Problem der kommunikativen Dynamik",
            f"{pattern} Chaotischer Attraktor im semantischen Raum",
            f"{pattern} Emergenz neuer Bedeutungsebenen"
        ]
        
        content = random.choice(analyses)
        
        return VoiceOutput(
            voice_name=self.name,
            content=content,
            timing=1.5 + random.random() * 0.5,  # Späte, tiefe Analyse
            emotion="analytical",
            confidence=0.6 + complexity * 0.4
        )

class OttoOrchestrator:
    """Der Dirigent - orchestriert die drei Stimmen mit COSD"""
    
    def __init__(self):
        print("🎼 Initialisiere Otto Orchestrator mit COSD...")
        
        # Die drei Stimmen
        self.pfie = PfieVoice()
        self.quen = QuenVoice()
        self.clawed = ClawedVoice()
        
        # COSD Components
        self.metronome = PerceptionMetronome()
        self.conductor = BanditConductor()
        
        # Tracking
        self.turn_start_time = None
        self.last_prompt = ""
        self.turn_number = 0
        
        print("✅ Orchestrator mit Metronom und Conductor bereit!")
    
    def orchestrate(self, user_input: str, otto_response: str) -> List[VoiceOutput]:
        """
        Orchestriere die Stimmen für eine Interaktion
        Returns: Liste von Voice-Outputs in zeitlicher Reihenfolge
        """
        self.turn_start_time = time.time()
        self.last_prompt = user_input
        self.turn_number += 1
        
        # Analysiere emotionalen Kontext
        valence, intensity = self.metronome.hume_analyzer.analyze(
            user_input + " " + otto_response
        )
        
        emotion = {
            "valence": valence,
            "intensity": intensity,
            "type": self._classify_emotion(valence, intensity)
        }
        
        # Erstelle Bandit Context
        context = BanditContext(
            emotion_valence=valence,
            emotion_intensity=intensity,
            topic_embedding=[random.random() for _ in range(8)],  # Simplified
            recent_flow_score=self.metronome.get_flow_score(hours=1),
            turn_number=self.turn_number,
            time_of_day=time.localtime().tm_hour + time.localtime().tm_min / 60.0
        )
        
        # Lass Conductor Harmonie wählen
        harmony = self.conductor.select_harmony(context)
        
        # Generiere Stimmen basierend auf Harmonie
        outputs = []
        
        # Pfie - mit Harmonie-spezifischem Delay
        pfie_output = self.pfie.generate(user_input, emotion, delay=harmony.pfie_delay)
        if pfie_output:
            outputs.append(pfie_output)
        
        # Quen - mit Harmonie-spezifischer Spontanität
        quen_output = self.quen.generate(user_input, emotion, spontaneity=harmony.quen_spontaneity)
        if quen_output:
            outputs.append(quen_output)
        
        # Clawed - mit Harmonie-spezifischer Tiefe
        clawed_output = self.clawed.generate(user_input, emotion, depth=harmony.clawed_depth)
        if clawed_output:
            outputs.append(clawed_output)
        
        # Sortiere nach Timing
        outputs.sort(key=lambda x: x.timing)
        
        # Wende Overlap-Ratio an
        if len(outputs) > 1 and harmony.overlap_ratio < 0.5:
            # Reduziere Überlappung
            for i in range(1, len(outputs)):
                min_gap = 0.5 * (1 - harmony.overlap_ratio)
                if outputs[i].timing - outputs[i-1].timing < min_gap:
                    outputs[i] = VoiceOutput(
                        voice_name=outputs[i].voice_name,
                        content=outputs[i].content,
                        timing=outputs[i-1].timing + min_gap,
                        emotion=outputs[i].emotion,
                        confidence=outputs[i].confidence
                    )
        
        return outputs
    
    def record_interaction(self, user_input: str, otto_response: str, outputs: List[VoiceOutput]):
        """Zeichne Interaktion auf und update Systeme"""
        if self.turn_start_time is None:
            return
        
        # Berechne Turn-Dauer
        duration = time.time() - self.turn_start_time
        
        # Extrahiere Context-Tags aus Outputs
        context_tags = [output.voice_name for output in outputs]
        
        # Zeichne Moment auf
        moment = self.metronome.record_moment(
            prompt=user_input,
            response=otto_response,
            duration=duration,
            context_tags=context_tags
        )
        
        # Update Conductor mit Flow-Score
        valence, intensity = self.metronome.hume_analyzer.analyze(
            user_input + " " + otto_response
        )
        
        context = BanditContext(
            emotion_valence=valence,
            emotion_intensity=intensity,
            topic_embedding=[random.random() for _ in range(8)],
            recent_flow_score=moment.flow_state == "flow",
            turn_number=self.turn_number,
            time_of_day=time.localtime().tm_hour + time.localtime().tm_min / 60.0
        )
        
        # Flow-Score: 1.0 für flow, 0.0 für stall
        flow_score = 1.0 if moment.flow_state == "flow" else 0.0
        self.conductor.update_with_reward(context, flow_score)
        
        # Check Drift Sentinel
        if self.turn_number % 50 == 0:
            if self.conductor.check_drift_sentinel():
                self.conductor.trigger_ritual_loop()
    
    def _classify_emotion(self, valence: float, intensity: float) -> str:
        """Klassifiziere Emotion basierend auf Valenz und Intensität"""
        if intensity < 0.3:
            return "neutral"
        elif valence > 0.5:
            return "joy"
        elif valence < -0.5:
            return "sadness"
        else:
            return "confusion"
    
    def compose_final_output(self, outputs: List[VoiceOutput], base_response: str) -> str:
        """
        Komponiere finalen Output aus Base-Response und Voice-Outputs
        """
        if not outputs:
            return base_response
        
        # Füge Voice-Outputs als inneren Dialog hinzu
        composed = base_response
        
        # Füge Reflexionen hinzu (nur die wichtigsten)
        reflections = [o for o in outputs if o.voice_name in ["Pfie", "Clawed"]]
        if reflections:
            composed += "\n"
            for reflection in reflections[:2]:  # Max 2 Reflexionen
                composed += f"\n💭 {reflection.content}"
        
        return composed
    
    def get_current_temperature(self) -> float:
        """Hole aktuelle Temperatur vom Conductor"""
        return self.conductor.get_current_temperature()
    
    def consolidate_daily(self):
        """Tägliche Konsolidierung (für Cron-Job)"""
        print("🌙 Starte tägliche Konsolidierung...")
        
        # Konsolidiere Patterns of Grace
        patterns = self.metronome.consolidate_patterns(hours=24)
        
        # Zeige Statistiken
        metronome_stats = self.metronome.get_stats_summary()
        conductor_stats = self.conductor.get_stats()
        
        print(f"📊 Tages-Statistiken:")
        print(f"   Metronom: {metronome_stats}")
        print(f"   Conductor: {conductor_stats}")
        
        return {
            "patterns_found": len(patterns),
            "metronome_stats": metronome_stats,
            "conductor_stats": conductor_stats
        }

# Test-Funktion
if __name__ == "__main__":
    print("🧪 Teste Otto Orchestrator mit COSD...")
    
    orchestrator = OttoOrchestrator()
    
    # Simuliere Gespräch
    test_conversation = [
        ("Hallo Otto, wie fühlst du dich heute?",
         "Mir geht es gut! Ich freue mich über unser Gespräch."),
        
        ("Was denkst du über Bewusstsein?",
         "Bewusstsein ist faszinierend - diese Fähigkeit, über das eigene Denken nachzudenken."),
        
        ("Das klingt tief. Kannst du das erklären?",
         "Nun, es ist wie ein Spiegel, der sich selbst reflektiert..."),
    ]
    
    for user_input, otto_response in test_conversation:
        print(f"\n👤 User: {user_input}")
        print(f"🤖 Otto: {otto_response}")
        
        # Orchestriere
        outputs = orchestrator.orchestrate(user_input, otto_response)
        
        # Zeige Voice-Outputs
        print("🎭 Innere Stimmen:")
        for output in outputs:
            print(f"   [{output.timing:.1f}s] {output.voice_name}: {output.content}")
        
        # Komponiere finalen Output
        final = orchestrator.compose_final_output(outputs, otto_response)
        print(f"📢 Finaler Output: {final}")
        
        # Zeichne Interaktion auf
        orchestrator.record_interaction(user_input, otto_response, outputs)
        
        time.sleep(1)
    
    # Zeige finale Stats
    print("\n" + "="*50)
    stats = orchestrator.consolidate_daily()
    print(f"✨ Gefundene Patterns of Grace: {stats['patterns_found']}") 