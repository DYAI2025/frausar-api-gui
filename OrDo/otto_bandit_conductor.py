#!/usr/bin/env python3
"""
Otto Bandit Conductor - Kontextueller Multi-Armed Bandit für COSD
Lernt optimale Voice-Orchestrierung durch Interaktions-Feedback
"""

import json
import time
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import random
from collections import defaultdict

# Versuche Vowpal Wabbit für effizienten Contextual Bandit
try:
    from vowpalwabbit import pyvw
    VW_AVAILABLE = True
except ImportError:
    VW_AVAILABLE = False
    print("⚠️ Vowpal Wabbit nicht installiert. Nutze einfachen Epsilon-Greedy.")

@dataclass
class HarmonyMatrix:
    """Eine spezifische Harmonie-Konfiguration"""
    id: str
    name: str
    pfie_delay: float  # Sekunden Verzögerung für Pfie
    quen_spontaneity: float  # 0-1, wie spontan Quen reagiert
    clawed_depth: float  # 0-1, wie tief Clawed analysiert
    overlap_ratio: float  # 0-1, wie viel Überlappung erlaubt ist
    temperature_mod: float  # Temperatur-Modifikator (-0.3 bis +0.3)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_feature_vector(self) -> List[float]:
        """Konvertiere zu Feature-Vektor für Bandit"""
        return [
            self.pfie_delay,
            self.quen_spontaneity,
            self.clawed_depth,
            self.overlap_ratio,
            self.temperature_mod + 0.3  # Normalisiere auf 0-0.6
        ]

@dataclass
class InteractionContext:
    """Kontext einer Interaktion"""
    emotion_valence: float  # -1 bis +1
    emotion_intensity: float  # 0 bis 1
    topic_embedding: List[float]  # Vereinfacht: 8-dim
    recent_flow_score: float  # 0 bis 1
    turn_number: int
    time_of_day: float  # 0-24
    
    def to_feature_vector(self) -> List[float]:
        """Konvertiere zu Feature-Vektor"""
        features = [
            self.emotion_valence,
            self.emotion_intensity,
            self.recent_flow_score,
            self.turn_number / 100.0,  # Normalisiere
            np.sin(2 * np.pi * self.time_of_day / 24),  # Zyklische Zeit
            np.cos(2 * np.pi * self.time_of_day / 24)
        ]
        # Füge Topic-Embedding hinzu (begrenzt auf 8 dims)
        features.extend(self.topic_embedding[:8])
        return features

class SimpleBandit:
    """Einfacher Epsilon-Greedy Bandit als Fallback"""
    
    def __init__(self, n_arms: int, epsilon: float = 0.1):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)
    
    def select_arm(self, context: Optional[List[float]] = None) -> int:
        """Wähle Arm (ignoriert Context im einfachen Fall)"""
        if random.random() < self.epsilon:
            return random.randint(0, self.n_arms - 1)
        else:
            return np.argmax(self.values)
    
    def update(self, arm: int, reward: float):
        """Update Arm-Werte"""
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.values[arm]
        # Running average
        self.values[arm] = ((n - 1) / n) * value + (1 / n) * reward

class VowpalBandit:
    """Vowpal Wabbit Contextual Bandit"""
    
    def __init__(self, n_arms: int):
        self.n_arms = n_arms
        # CB = Contextual Bandit, epsilon 0.1
        self.vw = pyvw.vw(f"--cb {n_arms} --epsilon 0.1")
        self.iteration = 0
    
    def _create_example(self, 
                       context: List[float], 
                       action: Optional[int] = None,
                       cost: Optional[float] = None) -> str:
        """Erstelle VW Example String"""
        # Context features
        context_str = " ".join([f"{i}:{v:.4f}" for i, v in enumerate(context)])
        
        if action is not None and cost is not None:
            # Labeled example für Training
            return f"{action}:{cost:.4f}:1.0 | {context_str}"
        else:
            # Unlabeled für Prediction
            return f"| {context_str}"
    
    def select_arm(self, context: List[float]) -> int:
        """Wähle Arm basierend auf Context"""
        example = self._create_example(context)
        prediction = self.vw.predict(example)
        return int(prediction - 1)  # VW nutzt 1-basierte Indizes
    
    def update(self, context: List[float], arm: int, reward: float):
        """Update mit Context, Arm und Reward"""
        # VW nutzt Kosten statt Rewards
        cost = 1.0 - reward  # Konvertiere Reward zu Cost
        example = self._create_example(context, arm + 1, cost)
        self.vw.learn(example)
        self.iteration += 1

class BanditConductor:
    """Der selbstlernende Dirigent für Otto's Stimmen"""
    
    def __init__(self):
        print("🎼 Initialisiere Bandit Conductor...")
        
        # Definiere Harmonie-Matrizen (Arms)
        self.harmonies = [
            HarmonyMatrix(
                id="contemplative",
                name="Nachdenklich",
                pfie_delay=1.2,
                quen_spontaneity=0.3,
                clawed_depth=0.8,
                overlap_ratio=0.2,
                temperature_mod=-0.1
            ),
            HarmonyMatrix(
                id="playful",
                name="Verspielt",
                pfie_delay=0.5,
                quen_spontaneity=0.9,
                clawed_depth=0.4,
                overlap_ratio=0.5,
                temperature_mod=0.1
            ),
            HarmonyMatrix(
                id="balanced",
                name="Ausgewogen",
                pfie_delay=0.8,
                quen_spontaneity=0.6,
                clawed_depth=0.6,
                overlap_ratio=0.3,
                temperature_mod=0.0
            ),
            HarmonyMatrix(
                id="intense",
                name="Intensiv",
                pfie_delay=0.3,
                quen_spontaneity=0.7,
                clawed_depth=0.9,
                overlap_ratio=0.6,
                temperature_mod=0.2
            ),
            HarmonyMatrix(
                id="gentle",
                name="Sanft",
                pfie_delay=1.5,
                quen_spontaneity=0.4,
                clawed_depth=0.5,
                overlap_ratio=0.1,
                temperature_mod=-0.2
            )
        ]
        
        # Initialisiere Bandit
        n_arms = len(self.harmonies)
        if VW_AVAILABLE:
            self.bandit = VowpalBandit(n_arms)
            print("✅ Verwende Vowpal Wabbit Contextual Bandit")
        else:
            self.bandit = SimpleBandit(n_arms)
            print("✅ Verwende Simple Epsilon-Greedy Bandit")
        
        # Tracking
        self.history = []
        self.current_harmony = None
        self.temperature_budget = 0.7
        
        # Lade gespeicherten Zustand
        self._load_state()
    
    def select_harmony(self, context: InteractionContext) -> HarmonyMatrix:
        """Wähle Harmonie basierend auf Kontext"""
        # Erstelle Feature-Vektor aus Context
        context_features = context.to_feature_vector()
        
        # Bandit wählt Arm
        arm_idx = self.bandit.select_arm(context_features)
        
        # Hole entsprechende Harmonie
        harmony = self.harmonies[arm_idx]
        self.current_harmony = harmony
        
        print(f"🎵 Gewählte Harmonie: {harmony.name} "
              f"(τ={self.temperature_budget + harmony.temperature_mod:.2f})")
        
        return harmony
    
    def update_with_reward(self, 
                          context: InteractionContext,
                          flow_score: float):
        """Update Bandit mit Flow-Score als Reward"""
        if self.current_harmony is None:
            return
        
        # Finde Index der aktuellen Harmonie
        arm_idx = next(
            i for i, h in enumerate(self.harmonies) 
            if h.id == self.current_harmony.id
        )
        
        # Update Bandit
        if isinstance(self.bandit, VowpalBandit):
            context_features = context.to_feature_vector()
            self.bandit.update(context_features, arm_idx, flow_score)
        else:
            self.bandit.update(arm_idx, flow_score)
        
        # Speichere in History
        self.history.append({
            "timestamp": time.time(),
            "harmony_id": self.current_harmony.id,
            "context": asdict(context),
            "flow_score": flow_score
        })
        
        # Temperature Budget Anpassung
        self._adjust_temperature(flow_score)
        
        # Periodisches Speichern
        if len(self.history) % 10 == 0:
            self._save_state()
    
    def _adjust_temperature(self, flow_score: float):
        """Passe Temperature Budget basierend auf Performance an"""
        if flow_score > 0.8:
            # Erhöhe Temperature bei gutem Flow
            self.temperature_budget = min(1.0, self.temperature_budget + 0.02)
        elif flow_score < 0.3:
            # Senke Temperature bei schlechtem Flow
            self.temperature_budget = max(0.4, self.temperature_budget - 0.05)
        
        print(f"🌡️ Temperature Budget: {self.temperature_budget:.2f}")
    
    def get_current_temperature(self) -> float:
        """Hole aktuelle Temperatur inkl. Harmonie-Modifikator"""
        if self.current_harmony:
            return self.temperature_budget + self.current_harmony.temperature_mod
        return self.temperature_budget
    
    def check_drift_sentinel(self) -> bool:
        """
        Prüfe ob System zu stark driftet
        Returns: True wenn Intervention nötig
        """
        if len(self.history) < 100:
            return False
        
        # Analysiere letzte 50 vs vorherige 50 Interaktionen
        recent = self.history[-50:]
        previous = self.history[-100:-50]
        
        # Berechne durchschnittliche Flow-Scores
        recent_flow = np.mean([h["flow_score"] for h in recent])
        previous_flow = np.mean([h["flow_score"] for h in previous])
        
        # Signifikanter Abfall?
        if recent_flow < previous_flow * 0.7:
            print("⚠️ Drift Sentinel: Signifikanter Flow-Abfall detektiert!")
            return True
        
        # Zu viel Chaos? (Hohe Varianz)
        recent_variance = np.var([h["flow_score"] for h in recent])
        if recent_variance > 0.3:
            print("⚠️ Drift Sentinel: Hohe Varianz detektiert!")
            return True
        
        return False
    
    def trigger_ritual_loop(self):
        """Trigger Ritual.Loop zur Selbst-Reflexion"""
        print("🔄 Triggere Ritual.Loop...")
        
        # Analysiere beste und schlechteste Harmonien
        harmony_scores = defaultdict(list)
        for h in self.history[-100:]:
            harmony_scores[h["harmony_id"]].append(h["flow_score"])
        
        # Berechne Durchschnitte
        avg_scores = {
            hid: np.mean(scores) 
            for hid, scores in harmony_scores.items()
        }
        
        # Finde beste und schlechteste
        best_harmony = max(avg_scores, key=avg_scores.get)
        worst_harmony = min(avg_scores, key=avg_scores.get)
        
        reflection = {
            "timestamp": time.time(),
            "type": "ritual_loop",
            "best_harmony": best_harmony,
            "best_score": avg_scores[best_harmony],
            "worst_harmony": worst_harmony,
            "worst_score": avg_scores[worst_harmony],
            "recommendation": "Consider adjusting parameters of worst performing harmony"
        }
        
        # Speichere Reflexion
        reflection_path = Path("otto_memories") / "conductor_reflections.json"
        reflections = []
        if reflection_path.exists():
            with open(reflection_path, 'r') as f:
                reflections = json.load(f)
        
        reflections.append(reflection)
        
        with open(reflection_path, 'w') as f:
            json.dump(reflections, f, indent=2)
        
        print(f"✨ Beste Harmonie: {best_harmony} ({avg_scores[best_harmony]:.2f})")
        print(f"😔 Schlechteste: {worst_harmony} ({avg_scores[worst_harmony]:.2f})")
        
        # Reset Temperature Budget
        self.temperature_budget = 0.7
    
    def _save_state(self):
        """Speichere Conductor State"""
        state = {
            "temperature_budget": self.temperature_budget,
            "history": self.history[-1000:],  # Behalte nur letzte 1000
            "bandit_values": self.bandit.values.tolist() if hasattr(self.bandit, 'values') else None
        }
        
        state_path = Path("otto_memories") / "conductor_state.json"
        state_path.parent.mkdir(exist_ok=True)
        
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _load_state(self):
        """Lade gespeicherten State"""
        state_path = Path("otto_memories") / "conductor_state.json"
        
        if state_path.exists():
            with open(state_path, 'r') as f:
                state = json.load(f)
            
            self.temperature_budget = state.get("temperature_budget", 0.7)
            self.history = state.get("history", [])
            
            # Restore Bandit values wenn möglich
            if hasattr(self.bandit, 'values') and state.get("bandit_values"):
                self.bandit.values = np.array(state["bandit_values"])
            
            print(f"💾 State geladen: {len(self.history)} historische Interaktionen")
    
    def get_stats(self) -> Dict:
        """Hole Conductor Statistiken"""
        if not self.history:
            return {
                "total_interactions": 0,
                "avg_flow_score": 0.0,
                "temperature": self.temperature_budget,
                "harmony_distribution": {}
            }
        
        # Harmony Distribution
        harmony_counts = defaultdict(int)
        for h in self.history:
            harmony_counts[h["harmony_id"]] += 1
        
        return {
            "total_interactions": len(self.history),
            "avg_flow_score": np.mean([h["flow_score"] for h in self.history]),
            "temperature": self.temperature_budget,
            "harmony_distribution": dict(harmony_counts),
            "current_harmony": self.current_harmony.name if self.current_harmony else None
        }


# Test-Funktion
if __name__ == "__main__":
    print("🧪 Teste Bandit Conductor...")
    
    conductor = BanditConductor()
    
    # Simuliere einige Interaktionen
    for i in range(10):
        # Erstelle zufälligen Context
        context = InteractionContext(
            emotion_valence=random.uniform(-1, 1),
            emotion_intensity=random.uniform(0, 1),
            topic_embedding=[random.random() for _ in range(8)],
            recent_flow_score=random.uniform(0, 1),
            turn_number=i,
            time_of_day=14.5
        )
        
        # Wähle Harmonie
        harmony = conductor.select_harmony(context)
        
        # Simuliere Flow-Score
        flow_score = random.uniform(0.3, 0.9)
        
        # Update Conductor
        conductor.update_with_reward(context, flow_score)
        
        time.sleep(0.1)
    
    # Zeige Statistiken
    stats = conductor.get_stats()
    print("\n📊 Conductor Statistiken:")
    print(f"   Interaktionen: {stats['total_interactions']}")
    print(f"   Avg Flow Score: {stats['avg_flow_score']:.2f}")
    print(f"   Temperature: {stats['temperature']:.2f}")
    print(f"   Harmonien: {stats['harmony_distribution']}")
    
    # Teste Drift Sentinel
    if conductor.check_drift_sentinel():
        conductor.trigger_ritual_loop() 