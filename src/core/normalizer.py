"""
Medikamenten-Normalizer für intelligentes Mapping und Fuzzy-Matching
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from Levenshtein import distance as levenshtein_distance
from src.data.reference_meds import (
    REFERENCE_MEDICATIONS, 
    get_medication_by_abbreviation,
    extract_dosage_from_text,
    extract_quantity_from_text
)

class MedicationNormalizer:
    """
    Normalisiert und mappt Medikamenten-Namen auf Referenzliste
    """
    
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initialisiert Normalizer
        
        Args:
            confidence_threshold: Mindest-Confidence für automatisches Mapping (0.0-1.0)
        """
        self.confidence_threshold = confidence_threshold
        self.custom_mappings = {}  # User-definierte Mappings
        self.uncertainty_log = []  # Log für unsichere Mappings
        
    def add_custom_mapping(self, input_text: str, medication_name: str):
        """
        Fügt benutzerdefiniertes Mapping hinzu
        
        Args:
            input_text: Original-Text aus Input
            medication_name: Gemappter Medikamenten-Name
        """
        self.custom_mappings[input_text.lower().strip()] = medication_name
        
    def normalize_medication(self, input_text: str) -> Dict[str, Any]:
        """
        Normalisiert Medikamenten-Text und gibt Mapping-Ergebnis zurück
        
        Args:
            input_text: Roher Input-Text
            
        Returns:
            Dict mit normalized_name, confidence, dosage, quantity, uncertainty
        """
        input_text = input_text.strip()
        input_lower = input_text.lower()
        
        # 1. Prüfe benutzerdefinierte Mappings
        if input_lower in self.custom_mappings:
            return {
                'original_text': input_text,
                'normalized_name': self.custom_mappings[input_lower],
                'confidence': 1.0,
                'dosage': extract_dosage_from_text(input_text),
                'quantity': extract_quantity_from_text(input_text),
                'uncertainty': False,
                'mapping_method': 'custom'
            }
        
        # 2. Versuche exakte Abkürzungs-Mappings
        exact_match = get_medication_by_abbreviation(input_text)
        if exact_match:
            return {
                'original_text': input_text,
                'normalized_name': exact_match,
                'confidence': 1.0,
                'dosage': extract_dosage_from_text(input_text),
                'quantity': extract_quantity_from_text(input_text),
                'uncertainty': False,
                'mapping_method': 'exact_abbreviation'
            }
        
        # 3. Fuzzy-Matching mit Levenshtein-Distanz
        best_match = self._fuzzy_match(input_text)
        
        if best_match:
            medication_name, confidence = best_match
            is_uncertain = confidence < self.confidence_threshold
            
            if is_uncertain:
                self.uncertainty_log.append({
                    'input': input_text,
                    'suggested_match': medication_name,
                    'confidence': confidence
                })
            
            return {
                'original_text': input_text,
                'normalized_name': medication_name,
                'confidence': confidence,
                'dosage': extract_dosage_from_text(input_text),
                'quantity': extract_quantity_from_text(input_text),
                'uncertainty': is_uncertain,
                'mapping_method': 'fuzzy_match'
            }
        
        # 4. Kein Match gefunden
        self.uncertainty_log.append({
            'input': input_text,
            'suggested_match': None,
            'confidence': 0.0
        })
        
        return {
            'original_text': input_text,
            'normalized_name': None,
            'confidence': 0.0,
            'dosage': extract_dosage_from_text(input_text),
            'quantity': extract_quantity_from_text(input_text),
            'uncertainty': True,
            'mapping_method': 'no_match'
        }
    
    def _fuzzy_match(self, input_text: str) -> Optional[Tuple[str, float]]:
        """
        Führt Fuzzy-Matching gegen Referenzliste durch
        
        Args:
            input_text: Input-Text für Matching
            
        Returns:
            Tuple aus (medication_name, confidence) oder None
        """
        input_lower = input_text.lower()
        best_match = None
        best_confidence = 0.0
        
        # Entferne Zahlen und Sonderzeichen für besseres Matching
        input_clean = re.sub(r'[\d\s\-\.\,\(\)]+', ' ', input_lower).strip()
        
        for medication, data in REFERENCE_MEDICATIONS.items():
            # Teste gegen Medikamenten-Namen
            med_clean = re.sub(r'[\d\s\-\.\,\(\)mg]+', ' ', medication.lower()).strip()
            
            # Levenshtein-Distanz für Hauptname
            distance = levenshtein_distance(input_clean, med_clean)
            max_length = max(len(input_clean), len(med_clean))
            if max_length > 0:
                confidence = 1.0 - (distance / max_length)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = medication
            
            # Teste gegen alle Abkürzungen
            for abbrev in data['abbreviations']:
                abbrev_clean = re.sub(r'[\d\s\-\.\,\(\)]+', ' ', abbrev.lower()).strip()
                
                # Exakte Substring-Übereinstimmung
                if abbrev_clean in input_clean or input_clean in abbrev_clean:
                    if len(abbrev_clean) > 2:  # Mindestlänge für Substring-Match
                        confidence = 0.9
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_match = medication
                
                # Levenshtein für Abkürzungen
                distance = levenshtein_distance(input_clean, abbrev_clean)
                max_length = max(len(input_clean), len(abbrev_clean))
                if max_length > 0:
                    confidence = 1.0 - (distance / max_length)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = medication
        
        return (best_match, best_confidence) if best_match and best_confidence > 0.3 else None
    
    def get_uncertainty_summary(self) -> List[Dict[str, Any]]:
        """
        Gibt Zusammenfassung aller unsicheren Mappings zurück
        
        Returns:
            List[Dict]: Unsichere Mappings für User-Review
        """
        return self.uncertainty_log.copy()
    
    def clear_uncertainty_log(self):
        """
        Löscht Log der unsicheren Mappings
        """
        self.uncertainty_log.clear()
    
    def batch_normalize(self, input_texts: List[str]) -> List[Dict[str, Any]]:
        """
        Normalisiert Liste von Medikamenten-Texten
        
        Args:
            input_texts: Liste von Input-Texten
            
        Returns:
            List[Dict]: Normalisierungs-Ergebnisse
        """
        results = []
        for text in input_texts:
            result = self.normalize_medication(text)
            results.append(result)
        return results
    
    def aggregate_quantities(self, normalized_results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Aggregiert Mengen für identische Medikamente
        
        Args:
            normalized_results: Liste der Normalisierungs-Ergebnisse
            
        Returns:
            Dict: Aggregierte Daten nach Medikament
        """
        aggregated = {}
        
        for result in normalized_results:
            if not result['normalized_name']:
                continue
                
            medication = result['normalized_name']
            quantity = result['quantity'] or 1  # Default zu 1 wenn keine Menge angegeben
            
            if medication not in aggregated:
                aggregated[medication] = {
                    'Product': medication,
                    'Quantity': 0,
                    'Price per Unit (€)': '',
                    'Total Price (€)': '',
                    'original_inputs': [],
                    'confidence_scores': []
                }
            
            aggregated[medication]['Quantity'] += quantity
            aggregated[medication]['original_inputs'].append(result['original_text'])
            aggregated[medication]['confidence_scores'].append(result['confidence'])
        
        return aggregated
    
    def validate_mapping_quality(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validiert Qualität der Mapping-Ergebnisse
        
        Args:
            results: Normalisierungs-Ergebnisse
            
        Returns:
            Dict: Qualitäts-Metriken
        """
        if not results:
            return {'total': 0, 'mapped': 0, 'uncertain': 0, 'quality_score': 0.0}
        
        total = len(results)
        mapped = sum(1 for r in results if r['normalized_name'])
        uncertain = sum(1 for r in results if r['uncertainty'])
        avg_confidence = sum(r['confidence'] for r in results) / total
        
        return {
            'total': total,
            'mapped': mapped,
            'uncertain': uncertain,
            'mapping_rate': mapped / total,
            'uncertainty_rate': uncertain / total,
            'average_confidence': avg_confidence,
            'quality_score': (mapped / total) * avg_confidence
        } 