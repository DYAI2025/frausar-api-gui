"""
Otto's Unterbewusstsein - Integriertes CoSD + Phi-4-Mini-Reasoning System
Verarbeitet Marker mit erweiterter semantischer Drift-Analyse
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Import der Unterbewusstsein-Module
sys.path.append(str(Path(__file__).parent))

from cosd_analysis.cosd_analyzer import CoSDAnalyzer
from phi4_reasoning.phi4_reasoner import Phi4Reasoner

class OttoSubconscious:
    """Otto's integriertes Unterbewusstsein mit CoSD + Phi-4-Mini-Reasoning"""
    
    def __init__(self):
        self.cosd_analyzer = CoSDAnalyzer()
        self.phi4_reasoner = Phi4Reasoner()
        self.processing_history = []
        self.marker_cache = {}
        
        # Unterbewusstsein-Konfiguration
        self.config = {
            'enable_cosd': True,
            'enable_phi4_reasoning': True,
            'enable_marker_caching': True,
            'max_cache_size': 1000,
            'processing_threshold': 0.5  # Mindest-Confidence für Verarbeitung
        }
        
        print("🧠 Otto's Unterbewusstsein initialisiert")
        print(f"   CoSD-Analyzer: {'✅' if self.config['enable_cosd'] else '❌'}")
        print(f"   Phi-4-Reasoning: {'✅' if self.config['enable_phi4_reasoning'] else '❌'}")
    
    def process_input(self, text: str, context: Dict = None) -> Dict:
        """Verarbeitet Input durch Otto's Unterbewusstsein"""
        
        print(f"🧠 Unterbewusstsein verarbeitet: '{text[:50]}...'")
        
        # Schritt 1: CoSD-Analyse
        cosd_result = None
        if self.config['enable_cosd']:
            cosd_result = self.cosd_analyzer.analyze_text(text, context)
            print(f"   📊 CoSD-Risiko: {cosd_result['risk_level']}")
            print(f"   🚀 Drift-Velocity: {cosd_result['drift_velocity']:.2f}")
        
        # Schritt 2: Marker-Extraktion
        markers = self._extract_markers(text, cosd_result)
        
        # Schritt 3: Phi-4-Mini-Reasoning für jeden Marker
        reasoning_results = []
        if self.config['enable_phi4_reasoning'] and markers:
            for marker in markers:
                reasoning_result = self.phi4_reasoner.process_marker(marker, context)
                reasoning_results.append(reasoning_result)
                print(f"   🎯 Marker verarbeitet: {marker['type']}")
        
        # Schritt 4: Integration und Synthese
        subconscious_result = self._synthesize_results(
            text, cosd_result, markers, reasoning_results, context
        )
        
        # Schritt 5: Cache-Update
        if self.config['enable_marker_caching']:
            self._update_cache(text, subconscious_result)
        
        # Schritt 6: Historie speichern
        self.processing_history.append({
            'timestamp': datetime.now().isoformat(),
            'input': text,
            'result': subconscious_result
        })
        
        return subconscious_result
    
    def _extract_markers(self, text: str, cosd_result: Dict = None) -> List[Dict]:
        """Extrahiert Marker aus Text basierend auf CoSD-Analyse"""
        
        markers = []
        
        # Marker-Kategorien basierend auf CoSD-Ergebnissen
        if cosd_result:
            risk_level = cosd_result.get('risk_level', 'LOW')
            drift_velocity = cosd_result.get('drift_velocity', 0.0)
            
            # Semantische Marker bei hoher Drift-Velocity
            if drift_velocity > 0.6:
                markers.append({
                    'type': 'semantic_drift',
                    'content': text,
                    'confidence': drift_velocity,
                    'cosd_analysis': cosd_result
                })
            
            # Risiko-Marker bei hohem Risiko
            if risk_level == 'HIGH':
                markers.append({
                    'type': 'risk_alert',
                    'content': text,
                    'confidence': 0.8,
                    'risk_level': risk_level
                })
        
        # Standard-Marker-Extraktion
        marker_patterns = {
            'emotional': [
                r'\b(freude|trauer|wut|angst|liebe|hass)\b',
                r'\b(glücklich|traurig|wütend|ängstlich)\b'
            ],
            'cognitive': [
                r'\b(denken|überlegen|analysieren|verstehen)\b',
                r'\b(logisch|rational|vernünftig)\b'
            ],
            'behavioral': [
                r'\b(handeln|reagieren|antworten|verhalten)\b',
                r'\b(muster|gewohnheit|routine)\b'
            ],
            'resonance': [
                r'\b(resonanz|schwingung|harmonie|einklang)\b',
                r'\b(frequenz|rhythmus|puls)\b'
            ]
        }
        
        for marker_type, patterns in marker_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text.lower())
                if matches:
                    markers.append({
                        'type': marker_type,
                        'content': text,
                        'confidence': len(matches) / len(text.split()),
                        'matches': matches
                    })
        
        return markers
    
    def _synthesize_results(self, text: str, cosd_result: Dict, 
                          markers: List[Dict], reasoning_results: List[Dict], 
                          context: Dict = None) -> Dict:
        """Synthetisiert alle Ergebnisse zu einer kohärenten Antwort"""
        
        synthesis = {
            'timestamp': datetime.now().isoformat(),
            'input_text': text,
            'cosd_analysis': cosd_result,
            'markers_detected': len(markers),
            'reasoning_applied': len(reasoning_results),
            'subconscious_insights': [],
            'recommendations': [],
            'confidence_score': 0.0
        }
        
        # Insights aus CoSD-Analyse
        if cosd_result:
            synthesis['subconscious_insights'].extend(cosd_result.get('recommendations', []))
            
            # Drift-basierte Insights
            drift_velocity = cosd_result.get('drift_velocity', 0.0)
            if drift_velocity > 0.7:
                synthesis['subconscious_insights'].append("🚀 Starke semantische Evolution erkannt")
            elif drift_velocity > 0.4:
                synthesis['subconscious_insights'].append("📈 Moderate semantische Veränderung")
        
        # Insights aus Phi-4-Reasoning
        for reasoning_result in reasoning_results:
            synthesis['subconscious_insights'].extend(reasoning_result.get('insights', []))
            synthesis['recommendations'].extend(reasoning_result.get('recommendations', []))
        
        # Confidence-Score berechnen
        confidence_factors = []
        if cosd_result:
            confidence_factors.append(cosd_result.get('drift_velocity', 0.0))
        
        for marker in markers:
            confidence_factors.append(marker.get('confidence', 0.0))
        
        if confidence_factors:
            synthesis['confidence_score'] = sum(confidence_factors) / len(confidence_factors)
        
        # Finale Empfehlungen
        if synthesis['confidence_score'] > 0.7:
            synthesis['recommendations'].append("💎 Hochwertige Lernmöglichkeit - Vertiefte Analyse empfohlen")
        elif synthesis['confidence_score'] > 0.4:
            synthesis['recommendations'].append("📚 Standard-Lernmöglichkeit - Kontinuierliche Beobachtung")
        else:
            synthesis['recommendations'].append("🔍 Niedrige Konfidenz - Weitere Daten erforderlich")
        
        return synthesis
    
    def _update_cache(self, text: str, result: Dict):
        """Aktualisiert Marker-Cache"""
        
        # Cache-Größe begrenzen
        if len(self.marker_cache) >= self.config['max_cache_size']:
            # Entferne älteste Einträge
            oldest_keys = sorted(self.marker_cache.keys())[:100]
            for key in oldest_keys:
                del self.marker_cache[key]
        
        # Neuen Eintrag hinzufügen
        cache_key = hash(text) % 10000
        self.marker_cache[cache_key] = {
            'text': text,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_subconscious_summary(self) -> Dict:
        """Gibt Zusammenfassung des Unterbewusstseins"""
        
        return {
            'total_processed': len(self.processing_history),
            'cache_size': len(self.marker_cache),
            'cosd_analyses': len(self.cosd_analyzer.analysis_history),
            'phi4_reasonings': len(self.phi4_reasoner.reasoning_history),
            'last_processing': self.processing_history[-1]['timestamp'] if self.processing_history else None
        }
    
    def save_subconscious_state(self, filename: str = None):
        """Speichert Zustand des Unterbewusstseins"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"otto_subconscious_{timestamp}.json"
        
        subconscious_state = {
            'subconscious_info': {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'config': self.config
            },
            'processing_history': self.processing_history,
            'marker_cache': self.marker_cache,
            'cosd_analyses': self.cosd_analyzer.analysis_history,
            'phi4_reasonings': self.phi4_reasoner.reasoning_history
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(subconscious_state, f, indent=2, ensure_ascii=False)
        
        return filename

# Test-Funktion
def test_subconscious():
    """Testet Otto's Unterbewusstsein"""
    
    subconscious = OttoSubconscious()
    
    test_texts = [
        "Ich fühle mich heute sehr glücklich und voller Energie",
        "Das Problem liegt in der semantischen Drift der Kommunikation",
        "Die Resonanz zwischen uns ist harmonisch und tiefgreifend"
    ]
    
    for text in test_texts:
        print(f"\n🧠 Teste Unterbewusstsein mit: '{text}'")
        result = subconscious.process_input(text)
        
        print(f"   📊 Konfidenz: {result['confidence_score']:.2f}")
        print(f"   🎯 Marker erkannt: {result['markers_detected']}")
        print(f"   💡 Insights: {len(result['subconscious_insights'])}")
        print(f"   📋 Empfehlungen: {len(result['recommendations'])}")
    
    # Speichere Zustand
    filename = subconscious.save_subconscious_state()
    print(f"\n💾 Unterbewusstsein-Zustand gespeichert: {filename}")
    
    # Zusammenfassung
    summary = subconscious.get_subconscious_summary()
    print(f"\n📊 Unterbewusstsein-Zusammenfassung:")
    print(f"   Verarbeitete Inputs: {summary['total_processed']}")
    print(f"   Cache-Größe: {summary['cache_size']}")
    print(f"   CoSD-Analysen: {summary['cosd_analyses']}")
    print(f"   Phi-4-Reasonings: {summary['phi4_reasonings']}")

if __name__ == "__main__":
    test_subconscious() 