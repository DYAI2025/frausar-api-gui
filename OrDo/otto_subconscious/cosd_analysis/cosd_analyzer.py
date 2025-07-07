"""
Co-Energente Semantik Drift (CoSD) Analyzer für Otto's Unterbewusstsein
Integriert mit Phi-4-Mini-Reasoning für erweiterte Marker-Analyse
"""

import json
import re
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import yaml
from pathlib import Path

class CoSDAnalyzer:
    """Co-Energente Semantik Drift Analyzer für Otto's Unterbewusstsein"""
    
    def __init__(self, phi4_model_name: str = "phi4-mini-reasoning"):
        self.phi4_model = phi4_model_name
        self.analysis_history = []
        self.drift_patterns = []
        self.emergence_clusters = []
        
        # Marker-Kategorien für Otto
        self.marker_categories = {
            'semantic': ['concept_drift', 'semantic_shift', 'meaning_evolution'],
            'behavioral': ['pattern_change', 'habit_shift', 'response_modification'],
            'emotional': ['mood_shift', 'affect_change', 'emotional_resonance'],
            'cognitive': ['thought_pattern', 'reasoning_shift', 'belief_change'],
            'resonance': ['frequency_match', 'harmonic_shift', 'vibrational_change']
        }
    
    def analyze_text(self, text: str, context: Dict = None) -> Dict:
        """Analysiert Text auf CoSD-Muster mit Phi-4-Mini-Reasoning"""
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'text': text,
            'risk_level': self._calculate_risk_level(text),
            'drift_velocity': self._calculate_drift_velocity(text),
            'emergence_clusters': self._detect_emergence_clusters(text),
            'resonance_patterns': self._analyze_resonance(text),
            'phi4_insights': self._get_phi4_insights(text, context),
            'recommendations': self._generate_recommendations(text)
        }
        
        self.analysis_history.append(analysis)
        return analysis
    
    def _calculate_risk_level(self, text: str) -> str:
        """Berechnet Risiko-Level basierend auf Drift-Indikatoren"""
        risk_indicators = [
            'abrupt', 'sudden', 'drastic', 'radical', 'extreme',
            'unexpected', 'unpredictable', 'chaotic', 'disruptive'
        ]
        
        risk_score = 0
        for indicator in risk_indicators:
            risk_score += len(re.findall(rf'\b{indicator}\b', text.lower()))
        
        if risk_score > 5:
            return "HIGH"
        elif risk_score > 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_drift_velocity(self, text: str) -> float:
        """Berechnet Drift-Geschwindigkeit (semantische Veränderungsrate)"""
        # Vereinfachte Drift-Berechnung
        words = text.lower().split()
        unique_words = len(set(words))
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        # Drift-Velocity basierend auf Lexikalischer Vielfalt
        drift_velocity = unique_words / total_words
        
        # Normalisierung auf 0-1 Skala
        return min(drift_velocity * 2, 1.0)
    
    def _detect_emergence_clusters(self, text: str) -> List[Dict]:
        """Erkennt emergente Cluster in Text"""
        clusters = []
        
        # Semantische Cluster-Erkennung
        semantic_patterns = [
            r'\b(neue?|emergente?|aufkommende?)\s+(idee|konzept|muster)\b',
            r'\b(evolution|entwicklung|wachstum)\b',
            r'\b(verbindung|vernetzung|integration)\b'
        ]
        
        for pattern in semantic_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                clusters.append({
                    'type': 'semantic_emergence',
                    'pattern': pattern,
                    'matches': matches,
                    'strength': len(matches)
                })
        
        return clusters
    
    def _analyze_resonance(self, text: str) -> Dict:
        """Analysiert Resonanz-Muster im Text"""
        resonance_indicators = {
            'harmonic': ['harmonie', 'einklang', 'resonanz', 'schwingung'],
            'dissonant': ['dissonanz', 'konflikt', 'spannung', 'widerspruch'],
            'rhythmic': ['rhythmus', 'puls', 'beat', 'tempo']
        }
        
        resonance_scores = {}
        for category, indicators in resonance_indicators.items():
            score = 0
            for indicator in indicators:
                score += len(re.findall(rf'\b{indicator}\b', text.lower()))
            resonance_scores[category] = score
        
        return resonance_scores
    
    def _get_phi4_insights(self, text: str, context: Dict = None) -> Dict:
        """Simuliert Phi-4-Mini-Reasoning Insights"""
        insights = {
            'reasoning_pattern': self._analyze_reasoning_pattern(text),
            'logical_flow': self._analyze_logical_flow(text),
            'cognitive_load': self._estimate_cognitive_load(text),
            'abstraction_level': self._analyze_abstraction_level(text)
        }
        
        if context:
            insights['context_integration'] = self._integrate_context(text, context)
        
        return insights
    
    def _analyze_reasoning_pattern(self, text: str) -> str:
        """Analysiert Reasoning-Muster mit Phi-4-Logik"""
        reasoning_patterns = {
            'deductive': ['daher', 'folglich', 'also', 'somit'],
            'inductive': ['beispiel', 'fall', 'instanz', 'typisch'],
            'abductive': ['wahrscheinlich', 'möglicherweise', 'scheint'],
            'analogical': ['ähnlich', 'wie', 'vergleich', 'analog']
        }
        
        pattern_scores = {}
        for pattern_type, indicators in reasoning_patterns.items():
            score = sum(len(re.findall(rf'\b{indicator}\b', text.lower())) 
                      for indicator in indicators)
            pattern_scores[pattern_type] = score
        
        # Bestimme dominantes Reasoning-Muster
        dominant_pattern = max(pattern_scores.items(), key=lambda x: x[1])
        return dominant_pattern[0] if dominant_pattern[1] > 0 else 'mixed'
    
    def _analyze_logical_flow(self, text: str) -> Dict:
        """Analysiert logischen Fluss mit Phi-4-Logik"""
        logical_connectors = {
            'causal': ['weil', 'da', 'denn', 'wegen'],
            'temporal': ['dann', 'später', 'zuerst', 'schließlich'],
            'conditional': ['wenn', 'falls', 'sofern', 'vorausgesetzt'],
            'contrastive': ['aber', 'jedoch', 'allerdings', 'hingegen']
        }
        
        flow_analysis = {}
        for flow_type, connectors in logical_connectors.items():
            count = sum(len(re.findall(rf'\b{connector}\b', text.lower())) 
                      for connector in connectors)
            flow_analysis[flow_type] = count
        
        return flow_analysis
    
    def _estimate_cognitive_load(self, text: str) -> str:
        """Schätzt kognitive Belastung"""
        words = text.split()
        sentence_count = len(re.split(r'[.!?]+', text))
        
        avg_sentence_length = len(words) / max(sentence_count, 1)
        complex_words = len([w for w in words if len(w) > 6])
        complexity_ratio = complex_words / max(len(words), 1)
        
        if avg_sentence_length > 20 or complexity_ratio > 0.3:
            return "HIGH"
        elif avg_sentence_length > 15 or complexity_ratio > 0.2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _analyze_abstraction_level(self, text: str) -> str:
        """Analysiert Abstraktions-Level"""
        abstract_indicators = [
            'konzept', 'prinzip', 'theorie', 'modell', 'system',
            'struktur', 'muster', 'paradigma', 'framework'
        ]
        
        abstract_count = sum(len(re.findall(rf'\b{indicator}\b', text.lower())) 
                           for indicator in abstract_indicators)
        
        if abstract_count > 3:
            return "HIGH"
        elif abstract_count > 1:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _integrate_context(self, text: str, context: Dict) -> Dict:
        """Integriert Kontext-Informationen"""
        context_integration = {
            'context_relevance': 0.0,
            'context_consistency': 0.0,
            'context_gaps': []
        }
        
        # Vereinfachte Kontext-Integration
        if 'previous_analysis' in context:
            context_integration['context_relevance'] = 0.8
        
        return context_integration
    
    def _generate_recommendations(self, text: str) -> List[str]:
        """Generiert Empfehlungen basierend auf CoSD-Analyse"""
        recommendations = []
        
        risk_level = self._calculate_risk_level(text)
        drift_velocity = self._calculate_drift_velocity(text)
        
        if risk_level == "HIGH":
            recommendations.append("⚠️ Hohe Drift-Geschwindigkeit erkannt - Überwachung empfohlen")
        
        if drift_velocity > 0.7:
            recommendations.append("🚀 Starke semantische Evolution - Lernmöglichkeit identifiziert")
        
        if len(self._detect_emergence_clusters(text)) > 0:
            recommendations.append("💎 Emergente Cluster erkannt - Vertiefte Analyse empfohlen")
        
        if not recommendations:
            recommendations.append("✅ Stabile semantische Struktur - Kontinuierliche Beobachtung")
        
        return recommendations
    
    def save_analysis(self, filename: str = None):
        """Speichert Analyse-Ergebnisse"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cosd_analysis_{timestamp}.json"
        
        analysis_data = {
            'analyzer_info': {
                'model': self.phi4_model,
                'version': '1.0',
                'created': datetime.now().isoformat()
            },
            'analysis_history': self.analysis_history,
            'drift_patterns': self.drift_patterns,
            'emergence_clusters': self.emergence_clusters
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        return filename 