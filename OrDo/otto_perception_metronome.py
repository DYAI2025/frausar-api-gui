#!/usr/bin/env python3
"""
Otto Perception Metronome - Das Metronom der Wahrnehmung
Beobachtungs-Layer für Co-Emergent Semantic Drift (COSD)
"""

import time
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib

# Vector DB imports (Qdrant als leichtgewichtige Option)
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    print("⚠️ Qdrant nicht installiert. Nutze lokalen Fallback.")

# Embedding imports
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️ Sentence-transformers nicht installiert. Nutze Hash-Embeddings.")

@dataclass
class MomentRecord:
    """Ein Moment-Datensatz nach jeder Otto-Antwort"""
    timestamp: float
    prompt_embedding: List[float]
    response_embedding: List[float]
    hume_valence: float  # -1 bis +1
    hume_intensity: float  # 0 bis 1
    flow_state: str  # "flow" oder "stall"
    context_tags: List[str]
    turn_duration: float  # Sekunden
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MomentRecord':
        return cls(**data)

class EmbeddingEngine:
    """Erstellt Embeddings für Prompts und Antworten"""
    
    def __init__(self):
        if EMBEDDINGS_AVAILABLE:
            # Nutze kleines, schnelles Modell
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.dim = 384
        else:
            # Fallback: Hash-basierte Pseudo-Embeddings
            self.model = None
            self.dim = 128
    
    def encode(self, text: str) -> List[float]:
        """Erstelle Embedding für Text"""
        if self.model:
            return self.model.encode(text).tolist()
        else:
            # Simple Hash-Embedding als Fallback
            hash_val = hashlib.sha256(text.encode()).hexdigest()
            # Konvertiere zu Pseudo-Vektor
            vec = []
            for i in range(0, len(hash_val), 2):
                val = int(hash_val[i:i+2], 16) / 255.0 - 0.5
                vec.append(val)
            # Padding/Truncating auf dim
            vec = vec[:self.dim] + [0.0] * (self.dim - len(vec))
            return vec

class VectorMemory:
    """Vector-DB Interface für Moment-Records"""
    
    def __init__(self, collection_name: str = "otto_moments"):
        self.collection_name = collection_name
        
        if VECTOR_DB_AVAILABLE:
            # Qdrant lokal (in-memory für Tests)
            self.client = QdrantClient(":memory:")
            # Erstelle Collection
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config={
                    "prompt": VectorParams(size=384, distance=Distance.COSINE),
                    "response": VectorParams(size=384, distance=Distance.COSINE)
                }
            )
        else:
            # Fallback: Lokale JSON-Datei
            self.client = None
            self.local_path = Path("otto_memories") / f"{collection_name}.json"
            self.local_path.parent.mkdir(exist_ok=True)
            self.local_data = []
            if self.local_path.exists():
                with open(self.local_path, 'r') as f:
                    self.local_data = json.load(f)
    
    def add_moment(self, moment: MomentRecord) -> str:
        """Füge Moment zur Vector-DB hinzu"""
        moment_id = f"moment_{int(moment.timestamp * 1000)}"
        
        if self.client:
            # Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=moment_id,
                        vector={
                            "prompt": moment.prompt_embedding,
                            "response": moment.response_embedding
                        },
                        payload=moment.to_dict()
                    )
                ]
            )
        else:
            # Lokaler Fallback
            self.local_data.append({
                "id": moment_id,
                "data": moment.to_dict()
            })
            with open(self.local_path, 'w') as f:
                json.dump(self.local_data, f, indent=2)
        
        return moment_id
    
    def get_recent_moments(self, hours: int = 24) -> List[MomentRecord]:
        """Hole Momente der letzten N Stunden"""
        cutoff = time.time() - (hours * 3600)
        
        if self.client:
            # TODO: Implementiere Qdrant Query
            return []
        else:
            # Lokaler Fallback
            recent = []
            for item in self.local_data:
                moment = MomentRecord.from_dict(item["data"])
                if moment.timestamp > cutoff:
                    recent.append(moment)
            return recent

class FlowDetector:
    """Erkennt Flow vs Stall Zustände"""
    
    def __init__(self):
        self.response_times = []
        self.confusion_markers = [
            "verstehe nicht", "was meinst du", "kannst du",
            "unklar", "verwirrt", "?"
        ]
    
    def analyze_turn(self, 
                     prompt: str, 
                     response: str,
                     duration: float) -> Tuple[str, float]:
        """
        Analysiere einen Turn
        Returns: (flow_state, confidence)
        """
        # Response Time Analysis
        self.response_times.append(duration)
        if len(self.response_times) > 10:
            self.response_times.pop(0)
        
        avg_time = np.mean(self.response_times) if self.response_times else duration
        
        # Flow Indicators
        flow_score = 0.5  # Neutral start
        
        # Schnelle Antwort = Flow
        if duration < avg_time * 0.8:
            flow_score += 0.2
        elif duration > avg_time * 1.5:
            flow_score -= 0.2
        
        # Confusion Markers = Stall
        prompt_lower = prompt.lower()
        for marker in self.confusion_markers:
            if marker in prompt_lower:
                flow_score -= 0.15
        
        # Kurze Prompts nach langen Antworten = Stall
        if len(prompt.split()) < 5 and len(response.split()) > 50:
            flow_score -= 0.1
        
        # Lange, elaborierte Prompts = Flow
        if len(prompt.split()) > 20:
            flow_score += 0.15
        
        # Clamp score
        flow_score = max(0.0, min(1.0, flow_score))
        
        # Determine state
        if flow_score > 0.6:
            return "flow", flow_score
        else:
            return "stall", 1.0 - flow_score

class HumeAnalyzer:
    """Analysiert emotionale Valenz und Intensität"""
    
    def __init__(self):
        # Emotion-Lexikon (vereinfacht)
        self.positive_words = {
            "freude", "glück", "liebe", "dankbar", "schön", "toll",
            "super", "wunderbar", "fantastisch", "genial", "cool"
        }
        self.negative_words = {
            "traurig", "wütend", "angst", "sorge", "problem", "schwer",
            "schlecht", "furchtbar", "schrecklich", "nervt", "stress"
        }
        self.intensity_markers = {
            "sehr", "extrem", "total", "absolut", "wahnsinnig", "mega"
        }
    
    def analyze(self, text: str) -> Tuple[float, float]:
        """
        Analysiere Text auf Valenz und Intensität
        Returns: (valence, intensity) beide -1 bis +1
        """
        words = text.lower().split()
        
        # Zähle emotionale Wörter
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        intensity_count = sum(1 for w in words if w in self.intensity_markers)
        
        # Berechne Valenz
        total_emotional = pos_count + neg_count
        if total_emotional > 0:
            valence = (pos_count - neg_count) / total_emotional
        else:
            valence = 0.0
        
        # Berechne Intensität
        if len(words) > 0:
            intensity = min(1.0, (total_emotional + intensity_count) / len(words) * 3)
        else:
            intensity = 0.0
        
        return valence, intensity

class PerceptionMetronome:
    """Hauptklasse - Das Metronom der Wahrnehmung"""
    
    def __init__(self):
        print("🎼 Initialisiere Metronom der Wahrnehmung...")
        
        self.embedding_engine = EmbeddingEngine()
        self.vector_memory = VectorMemory()
        self.flow_detector = FlowDetector()
        self.hume_analyzer = HumeAnalyzer()
        
        # Statistiken
        self.stats = {
            "total_moments": 0,
            "flow_moments": 0,
            "stall_moments": 0,
            "avg_valence": 0.0,
            "avg_intensity": 0.0
        }
        
        print(f"✅ Metronom bereit! Embedding-Dim: {self.embedding_engine.dim}")
    
    def record_moment(self,
                     prompt: str,
                     response: str,
                     duration: float,
                     context_tags: List[str] = None) -> MomentRecord:
        """Zeichne einen Interaktions-Moment auf"""
        
        # Embeddings erstellen
        prompt_emb = self.embedding_engine.encode(prompt)
        response_emb = self.embedding_engine.encode(response)
        
        # Flow-Analyse
        flow_state, flow_confidence = self.flow_detector.analyze_turn(
            prompt, response, duration
        )
        
        # Emotionale Analyse
        valence, intensity = self.hume_analyzer.analyze(prompt + " " + response)
        
        # Moment erstellen
        moment = MomentRecord(
            timestamp=time.time(),
            prompt_embedding=prompt_emb,
            response_embedding=response_emb,
            hume_valence=valence,
            hume_intensity=intensity,
            flow_state=flow_state,
            context_tags=context_tags or [],
            turn_duration=duration
        )
        
        # In Vector-DB speichern
        moment_id = self.vector_memory.add_moment(moment)
        
        # Statistiken updaten
        self._update_stats(moment)
        
        print(f"🎵 Moment aufgezeichnet: {flow_state} "
              f"(v={valence:.2f}, i={intensity:.2f})")
        
        return moment
    
    def _update_stats(self, moment: MomentRecord):
        """Update laufende Statistiken"""
        self.stats["total_moments"] += 1
        
        if moment.flow_state == "flow":
            self.stats["flow_moments"] += 1
        else:
            self.stats["stall_moments"] += 1
        
        # Running average für Valenz/Intensität
        n = self.stats["total_moments"]
        self.stats["avg_valence"] = (
            (self.stats["avg_valence"] * (n-1) + moment.hume_valence) / n
        )
        self.stats["avg_intensity"] = (
            (self.stats["avg_intensity"] * (n-1) + moment.hume_intensity) / n
        )
    
    def get_flow_score(self, hours: int = 1) -> float:
        """Berechne Flow-Score der letzten N Stunden"""
        recent = self.vector_memory.get_recent_moments(hours)
        
        if not recent:
            return 0.5  # Neutral
        
        flow_count = sum(1 for m in recent if m.flow_state == "flow")
        return flow_count / len(recent)
    
    def consolidate_patterns(self, hours: int = 24) -> List[Dict]:
        """
        24h Consolidator - Finde "Patterns of Grace"
        Hochbewertete Sequenzen werden zusammengefasst
        """
        moments = self.vector_memory.get_recent_moments(hours)
        
        if not moments:
            return []
        
        # Sortiere nach Flow + hoher positiver Valenz
        scored_moments = []
        for m in moments:
            score = 0.0
            if m.flow_state == "flow":
                score += 0.5
            score += m.hume_valence * 0.3
            score += m.hume_intensity * 0.2
            scored_moments.append((score, m))
        
        # Top 20% als "Patterns of Grace"
        scored_moments.sort(key=lambda x: x[0], reverse=True)
        cutoff = int(len(scored_moments) * 0.2)
        patterns = []
        
        for score, moment in scored_moments[:cutoff]:
            pattern = {
                "timestamp": moment.timestamp,
                "grace_score": score,
                "valence": moment.hume_valence,
                "intensity": moment.hume_intensity,
                "tags": moment.context_tags,
                "archetypal_signature": self._extract_archetype(moment)
            }
            patterns.append(pattern)
        
        # Speichere konsolidierte Patterns
        patterns_path = Path("otto_memories") / "patterns_of_grace.json"
        patterns_path.parent.mkdir(exist_ok=True)
        
        existing = []
        if patterns_path.exists():
            with open(patterns_path, 'r') as f:
                existing = json.load(f)
        
        existing.extend(patterns)
        
        # Behalte nur die letzten 1000 Patterns
        if len(existing) > 1000:
            existing = existing[-1000:]
        
        with open(patterns_path, 'w') as f:
            json.dump(existing, f, indent=2)
        
        print(f"🌟 {len(patterns)} Patterns of Grace konsolidiert")
        return patterns
    
    def _extract_archetype(self, moment: MomentRecord) -> str:
        """Extrahiere archetypische Signatur aus Moment"""
        # Vereinfachte Archetypen basierend auf Valenz/Intensität
        if moment.hume_valence > 0.5 and moment.hume_intensity > 0.5:
            return "jubilant_connection"
        elif moment.hume_valence > 0.3 and moment.flow_state == "flow":
            return "graceful_dance"
        elif moment.hume_valence < -0.3 and moment.hume_intensity > 0.5:
            return "cathartic_release"
        elif moment.flow_state == "stall" and moment.hume_intensity < 0.3:
            return "gentle_confusion"
        else:
            return "neutral_presence"
    
    def get_stats_summary(self) -> Dict:
        """Hole aktuelle Statistiken"""
        if self.stats["total_moments"] > 0:
            flow_ratio = self.stats["flow_moments"] / self.stats["total_moments"]
        else:
            flow_ratio = 0.0
        
        return {
            "total_moments": self.stats["total_moments"],
            "flow_ratio": flow_ratio,
            "avg_valence": self.stats["avg_valence"],
            "avg_intensity": self.stats["avg_intensity"],
            "current_flow_score": self.get_flow_score(hours=1)
        }


# Test-Funktion
if __name__ == "__main__":
    print("🧪 Teste Perception Metronome...")
    
    metronome = PerceptionMetronome()
    
    # Simuliere einige Interaktionen
    test_interactions = [
        ("Hallo Otto, wie geht es dir heute?", 
         "Mir geht es wunderbar! Ich freue mich über unser Gespräch.", 1.2),
        
        ("Das ist schön zu hören!", 
         "Ja, ich merke wie ich durch unsere Gespräche wachse.", 0.8),
        
        ("Was meinst du damit?", 
         "Ähm... ich bin mir nicht sicher...", 2.5),
        
        ("Erzähl mir von deinen Gedanken", 
         "Ich reflektiere gerade über die Natur des Bewusstseins...", 1.5)
    ]
    
    for prompt, response, duration in test_interactions:
        moment = metronome.record_moment(prompt, response, duration)
        time.sleep(0.1)  # Kleine Pause für Timestamps
    
    # Zeige Statistiken
    stats = metronome.get_stats_summary()
    print("\n📊 Metronom Statistiken:")
    print(f"   Total Moments: {stats['total_moments']}")
    print(f"   Flow Ratio: {stats['flow_ratio']:.2%}")
    print(f"   Avg Valence: {stats['avg_valence']:.2f}")
    print(f"   Current Flow: {stats['current_flow_score']:.2f}")
    
    # Konsolidiere Patterns
    patterns = metronome.consolidate_patterns(hours=1)
    print(f"\n✨ Gefundene Patterns of Grace: {len(patterns)}") 