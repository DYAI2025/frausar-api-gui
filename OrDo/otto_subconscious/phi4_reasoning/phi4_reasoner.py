"""
Phi-4-Mini-Reasoning Interface für Otto's Unterbewusstsein
Integriert mit CoSD-Analyse für erweiterte Marker-Verarbeitung
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import yaml
from pathlib import Path

class Phi4Reasoner:
    """Phi-4-Mini-Reasoning Interface für Otto's Unterbewusstsein"""
    
    def __init__(self, model_name: str = "phi4-mini-reasoning"):
        self.model_name = model_name
        self.reasoning_history = []
        self.cognitive_patterns = []
        self.logical_chains = []
        
        # Reasoning-Modi für Otto
        self.reasoning_modes = {
            'deductive': 'logische_schlussfolgerung',
            'inductive': 'muster_erkennung',
            'abductive': 'hypothesen_bildung',
            'analogical': 'analogie_bildung',
            'creative': 'kreative_synthese'
        }
    
    def process_marker(self, marker_data: Dict, context: Dict = None) -> Dict:
        """Verarbeitet Marker mit Phi-4-Mini-Reasoning"""
        
        reasoning_result = {
            'timestamp': datetime.now().isoformat(),
            'marker_data': marker_data,
            'reasoning_mode': self._determine_reasoning_mode(marker_data),
            'cognitive_analysis': self._analyze_cognitive_patterns(marker_data),
            'logical_chain': self._build_logical_chain(marker_data, context),
            'insights': self._generate_insights(marker_data, context),
            'recommendations': self._generate_reasoning_recommendations(marker_data)
        }
        
        self.reasoning_history.append(reasoning_result)
        return reasoning_result
    
    def _determine_reasoning_mode(self, marker_data: Dict) -> str:
        """Bestimmt den optimalen Reasoning-Modus für den Marker"""
        
        marker_type = marker_data.get('type', 'unknown')
        marker_content = marker_data.get('content', '')
        
        # Reasoning-Modus basierend auf Marker-Typ
        if 'semantic' in marker_type.lower():
            return 'deductive'
        elif 'behavioral' in marker_type.lower():
            return 'inductive'
        elif 'emotional' in marker_type.lower():
            return 'analogical'
        elif 'cognitive' in marker_type.lower():
            return 'abductive'
        elif 'resonance' in marker_type.lower():
            return 'creative'
        else:
            return 'inductive'  # Standard-Modus
    
    def _analyze_cognitive_patterns(self, marker_data: Dict) -> Dict:
        """Analysiert kognitive Muster im Marker"""
        
        content = marker_data.get('content', '')
        
        cognitive_analysis = {
            'complexity_level': self._assess_complexity(content),
            'abstraction_level': self._assess_abstraction(content),
            'emotional_valence': self._assess_emotional_valence(content),
            'logical_structure': self._assess_logical_structure(content),
            'cognitive_load': self._estimate_cognitive_load(content)
        }
        
        return cognitive_analysis
    
    def _assess_complexity(self, content: str) -> str:
        """Bewertet Komplexität des Inhalts"""
        words = content.split()
        avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
        unique_words_ratio = len(set(words)) / max(len(words), 1)
        
        complexity_score = (avg_word_length * 0.4) + (unique_words_ratio * 0.6)
        
        if complexity_score > 0.7:
            return "HIGH"
        elif complexity_score > 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _assess_abstraction(self, content: str) -> str:
        """Bewertet Abstraktions-Level"""
        abstract_indicators = [
            'konzept', 'prinzip', 'theorie', 'modell', 'system',
            'struktur', 'muster', 'paradigma', 'framework', 'ansatz'
        ]
        
        abstract_count = sum(len(re.findall(rf'\b{indicator}\b', content.lower())) 
                           for indicator in abstract_indicators)
        
        if abstract_count > 2:
            return "HIGH"
        elif abstract_count > 0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _assess_emotional_valence(self, content: str) -> Dict:
        """Bewertet emotionale Valenz"""
        positive_indicators = [
            'positiv', 'gut', 'besser', 'verbessern', 'lösung',
            'erfolg', 'fortschritt', 'wachstum', 'entwicklung'
        ]
        
        negative_indicators = [
            'negativ', 'schlecht', 'problem', 'schwierigkeit',
            'konflikt', 'spannung', 'stress', 'angst'
        ]
        
        positive_score = sum(len(re.findall(rf'\b{indicator}\b', content.lower())) 
                           for indicator in positive_indicators)
        negative_score = sum(len(re.findall(rf'\b{indicator}\b', content.lower())) 
                           for indicator in negative_indicators)
        
        return {
            'positive_score': positive_score,
            'negative_score': negative_score,
            'overall_valence': 'positive' if positive_score > negative_score else 'negative' if negative_score > positive_score else 'neutral'
        }
    
    def _assess_logical_structure(self, content: str) -> Dict:
        """Bewertet logische Struktur"""
        logical_connectors = {
            'causal': ['weil', 'da', 'denn', 'wegen', 'daher', 'folglich'],
            'temporal': ['dann', 'später', 'zuerst', 'schließlich', 'während'],
            'conditional': ['wenn', 'falls', 'sofern', 'vorausgesetzt'],
            'contrastive': ['aber', 'jedoch', 'allerdings', 'hingegen', 'obwohl']
        }
        
        structure_analysis = {}
        for connector_type, connectors in logical_connectors.items():
            count = sum(len(re.findall(rf'\b{connector}\b', content.lower())) 
                      for connector in connectors)
            structure_analysis[connector_type] = count
        
        return structure_analysis
    
    def _estimate_cognitive_load(self, content: str) -> str:
        """Schätzt kognitive Belastung"""
        sentences = re.split(r'[.!?]+', content)
        avg_sentence_length = len(content.split()) / max(len(sentences), 1)
        
        complex_words = len([w for w in content.split() if len(w) > 6])
        complexity_ratio = complex_words / max(len(content.split()), 1)
        
        if avg_sentence_length > 20 or complexity_ratio > 0.3:
            return "HIGH"
        elif avg_sentence_length > 15 or complexity_ratio > 0.2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _build_logical_chain(self, marker_data: Dict, context: Dict = None) -> List[Dict]:
        """Baut logische Schlussfolgerungskette"""
        
        logical_chain = []
        content = marker_data.get('content', '')
        
        # Schritt 1: Marker-Identifikation
        logical_chain.append({
            'step': 1,
            'type': 'marker_identification',
            'description': f"Marker-Typ: {marker_data.get('type', 'unknown')}",
            'confidence': 0.9
        })
        
        # Schritt 2: Semantische Analyse
        semantic_analysis = self._analyze_semantics(content)
        logical_chain.append({
            'step': 2,
            'type': 'semantic_analysis',
            'description': f"Semantische Muster: {len(semantic_analysis)} erkannt",
            'confidence': 0.8,
            'details': semantic_analysis
        })
        
        # Schritt 3: Kontext-Integration
        if context:
            context_integration = self._integrate_context(marker_data, context)
            logical_chain.append({
                'step': 3,
                'type': 'context_integration',
                'description': "Kontext erfolgreich integriert",
                'confidence': 0.7,
                'details': context_integration
            })
        
        # Schritt 4: Schlussfolgerung
        conclusion = self._generate_conclusion(marker_data, logical_chain)
        logical_chain.append({
            'step': 4,
            'type': 'conclusion',
            'description': conclusion['description'],
            'confidence': conclusion['confidence'],
            'details': conclusion['details']
        })
        
        return logical_chain
    
    def _analyze_semantics(self, content: str) -> List[Dict]:
        """Analysiert semantische Muster"""
        semantic_patterns = [
            {'pattern': r'\b(problem|lösung)\b', 'type': 'problem_solution'},
            {'pattern': r'\b(ursache|wirkung)\b', 'type': 'causality'},
            {'pattern': r'\b(ähnlich|vergleich)\b', 'type': 'analogy'},
            {'pattern': r'\b(beispiel|fall)\b', 'type': 'exemplification'}
        ]
        
        found_patterns = []
        for pattern_info in semantic_patterns:
            matches = re.findall(pattern_info['pattern'], content.lower())
            if matches:
                found_patterns.append({
                    'type': pattern_info['type'],
                    'matches': matches,
                    'count': len(matches)
                })
        
        return found_patterns
    
    def _integrate_context(self, marker_data: Dict, context: Dict) -> Dict:
        """Integriert Kontext-Informationen"""
        context_integration = {
            'relevant_context': [],
            'context_consistency': 0.0,
            'context_gaps': []
        }
        
        # Vereinfachte Kontext-Integration
        if 'previous_markers' in context:
            context_integration['relevant_context'] = context['previous_markers'][-3:]  # Letzte 3 Marker
        
        return context_integration
    
    def _generate_conclusion(self, marker_data: Dict, logical_chain: List[Dict]) -> Dict:
        """Generiert Schlussfolgerung basierend auf logischer Kette"""
        
        marker_type = marker_data.get('type', 'unknown')
        content = marker_data.get('content', '')
        
        # Schlussfolgerung basierend auf Marker-Typ
        if 'semantic' in marker_type.lower():
            conclusion = {
                'description': "Semantische Drift erkannt - Lernmöglichkeit identifiziert",
                'confidence': 0.8,
                'details': {'learning_opportunity': True, 'drift_type': 'semantic'}
            }
        elif 'behavioral' in marker_type.lower():
            conclusion = {
                'description': "Verhaltensmuster erkannt - Anpassung erforderlich",
                'confidence': 0.7,
                'details': {'behavioral_pattern': True, 'adaptation_needed': True}
            }
        elif 'emotional' in marker_type.lower():
            conclusion = {
                'description': "Emotionale Resonanz erkannt - Empathie erforderlich",
                'confidence': 0.6,
                'details': {'emotional_resonance': True, 'empathy_needed': True}
            }
        else:
            conclusion = {
                'description': "Allgemeines Muster erkannt - Weitere Analyse empfohlen",
                'confidence': 0.5,
                'details': {'general_pattern': True, 'further_analysis': True}
            }
        
        return conclusion
    
    def _generate_insights(self, marker_data: Dict, context: Dict = None) -> List[str]:
        """Generiert Insights basierend auf Phi-4-Reasoning"""
        insights = []
        
        marker_type = marker_data.get('type', 'unknown')
        content = marker_data.get('content', '')
        
        # Insights basierend auf Marker-Typ und Inhalt
        if 'semantic' in marker_type.lower():
            insights.append("🧠 Semantische Evolution erkannt - Otto kann daraus lernen")
        
        if 'behavioral' in marker_type.lower():
            insights.append("🎯 Verhaltensmuster identifiziert - Anpassungsstrategie erforderlich")
        
        if 'emotional' in marker_type.lower():
            insights.append("💙 Emotionale Resonanz erkannt - Empathische Reaktion empfohlen")
        
        if len(content.split()) > 20:
            insights.append("📝 Komplexer Inhalt - Vertiefte Analyse lohnenswert")
        
        if not insights:
            insights.append("🔍 Standard-Marker erkannt - Kontinuierliche Beobachtung")
        
        return insights
    
    def _generate_reasoning_recommendations(self, marker_data: Dict) -> List[str]:
        """Generiert Reasoning-Empfehlungen"""
        recommendations = []
        
        marker_type = marker_data.get('type', 'unknown')
        
        if 'semantic' in marker_type.lower():
            recommendations.append("💡 Semantische Drift-Überwachung aktivieren")
            recommendations.append("📚 Lernmöglichkeit in Jammeldateien speichern")
        
        if 'behavioral' in marker_type.lower():
            recommendations.append("🎯 Verhaltensanpassung in Kristall-System integrieren")
        
        if 'emotional' in marker_type.lower():
            recommendations.append("💙 Empathische Reaktion in Antwort-Generierung einbauen")
        
        if not recommendations:
            recommendations.append("✅ Standard-Marker-Verarbeitung - Kontinuierliche Beobachtung")
        
        return recommendations
    
    def save_reasoning_history(self, filename: str = None):
        """Speichert Reasoning-Historie"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phi4_reasoning_{timestamp}.json"
        
        reasoning_data = {
            'reasoner_info': {
                'model': self.model_name,
                'version': '1.0',
                'created': datetime.now().isoformat()
            },
            'reasoning_history': self.reasoning_history,
            'cognitive_patterns': self.cognitive_patterns,
            'logical_chains': self.logical_chains
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reasoning_data, f, indent=2, ensure_ascii=False)
        
        return filename 