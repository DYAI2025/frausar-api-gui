"""
Unit-Tests für MedicationNormalizer
"""

import pytest
from src.core.normalizer import MedicationNormalizer

class TestMedicationNormalizer:
    """
    Test-Suite für MedicationNormalizer
    """
    
    def setup_method(self):
        """
        Setup für jeden Test
        """
        self.normalizer = MedicationNormalizer(confidence_threshold=0.7)
    
    def test_exact_abbreviation_matching(self):
        """
        Test: Exakte Abkürzungs-Mappings
        """
        result = self.normalizer.normalize_medication("trama 225 30x")
        
        assert result['normalized_name'] == "Tramadol 225mg"
        assert result['confidence'] == 1.0
        assert result['uncertainty'] is False
        assert result['quantity'] == 30
        assert result['mapping_method'] == 'exact_abbreviation'
    
    def test_dosage_extraction(self):
        """
        Test: Dosage-Extraktion aus verschiedenen Formaten
        """
        test_cases = [
            ("Tramadol 225mg 10x", "225mg"),
            ("Medication 50 mg 5x", "50 mg"),
            ("Drug 7.5mg 20x", "7.5mg"),
            ("Medicine 100 ml 15x", "100 ml")
        ]
        
        for input_text, expected_dosage in test_cases:
            result = self.normalizer.normalize_medication(input_text)
            assert result['dosage'] == expected_dosage
    
    def test_quantity_extraction(self):
        """
        Test: Mengen-Extraktion aus verschiedenen Formaten
        """
        test_cases = [
            ("Tramadol 225mg 30x", 30),
            ("Ibuprofen 400mg 20 stück", 20),
            ("Medicine 50mg 15 tablets", 15),
            ("Drug 100mg 5 pills", 5)
        ]
        
        for input_text, expected_quantity in test_cases:
            result = self.normalizer.normalize_medication(input_text)
            assert result['quantity'] == expected_quantity
    
    def test_fuzzy_matching(self):
        """
        Test: Fuzzy-Matching für ähnliche Namen
        """
        # Leichter Tippfehler
        result = self.normalizer.normalize_medication("tramadol 225 10x")
        
        assert result['normalized_name'] == "Tramadol 225mg"
        assert result['confidence'] > 0.8
        assert result['mapping_method'] == 'fuzzy_match'
    
    def test_custom_mapping(self):
        """
        Test: Benutzerdefinierte Mappings
        """
        # Custom-Mapping hinzufügen
        self.normalizer.add_custom_mapping("special_med", "Tramadol 225mg")
        
        result = self.normalizer.normalize_medication("special_med 10x")
        
        assert result['normalized_name'] == "Tramadol 225mg"
        assert result['confidence'] == 1.0
        assert result['mapping_method'] == 'custom'
    
    def test_uncertainty_detection(self):
        """
        Test: Erkennung unsicherer Mappings
        """
        # Sehr unsichere Eingabe
        result = self.normalizer.normalize_medication("xyz123 50mg 10x")
        
        assert result['uncertainty'] is True
        assert result['confidence'] < 0.7
    
    def test_no_match_scenario(self):
        """
        Test: Kein Match gefunden
        """
        result = self.normalizer.normalize_medication("completely_unknown_drug 100mg 5x")
        
        assert result['normalized_name'] is None
        assert result['confidence'] == 0.0
        assert result['uncertainty'] is True
        assert result['mapping_method'] == 'no_match'
    
    def test_batch_normalization(self):
        """
        Test: Batch-Normalisierung
        """
        input_texts = [
            "trama 225 30x",
            "ibu 400 20x", 
            "xanax 3mg 10x"
        ]
        
        results = self.normalizer.batch_normalize(input_texts)
        
        assert len(results) == 3
        assert all(r['normalized_name'] is not None for r in results)
        assert all(r['confidence'] > 0.8 for r in results)
    
    def test_quantity_aggregation(self):
        """
        Test: Mengen-Aggregation für identische Medikamente
        """
        normalization_results = [
            {
                'normalized_name': 'Tramadol 225mg',
                'quantity': 30,
                'confidence': 1.0,
                'original_text': 'trama 225 30x'
            },
            {
                'normalized_name': 'Tramadol 225mg', 
                'quantity': 20,
                'confidence': 1.0,
                'original_text': 'tramadol 225mg 20x'
            },
            {
                'normalized_name': 'Ibuprofen 400mg',
                'quantity': 15,
                'confidence': 1.0,
                'original_text': 'ibu 400 15x'
            }
        ]
        
        aggregated = self.normalizer.aggregate_quantities(normalization_results)
        
        assert len(aggregated) == 2  # 2 unterschiedliche Medikamente
        assert aggregated['Tramadol 225mg']['Quantity'] == 50  # 30 + 20
        assert aggregated['Ibuprofen 400mg']['Quantity'] == 15
    
    def test_uncertainty_log(self):
        """
        Test: Uncertainty-Logging
        """
        # Erzeuge unsichere Mappings
        self.normalizer.normalize_medication("uncertain_med 100mg 5x")
        self.normalizer.normalize_medication("another_unclear 50mg 10x")
        
        uncertainty_summary = self.normalizer.get_uncertainty_summary()
        
        assert len(uncertainty_summary) == 2
        assert all('input' in entry for entry in uncertainty_summary)
    
    def test_mapping_quality_validation(self):
        """
        Test: Validierung der Mapping-Qualität
        """
        results = [
            {'normalized_name': 'Tramadol 225mg', 'confidence': 1.0, 'uncertainty': False},
            {'normalized_name': 'Ibuprofen 400mg', 'confidence': 0.9, 'uncertainty': False},
            {'normalized_name': None, 'confidence': 0.0, 'uncertainty': True},
            {'normalized_name': 'Xanax bars 3mg', 'confidence': 0.6, 'uncertainty': True}
        ]
        
        quality = self.normalizer.validate_mapping_quality(results)
        
        assert quality['total'] == 4
        assert quality['mapped'] == 3
        assert quality['uncertain'] == 2
        assert quality['mapping_rate'] == 0.75
        assert quality['uncertainty_rate'] == 0.5
    
    def test_confidence_threshold_effect(self):
        """
        Test: Auswirkung verschiedener Confidence-Thresholds
        """
        # Niedrigerer Threshold
        permissive_normalizer = MedicationNormalizer(confidence_threshold=0.5)
        
        # Höherer Threshold  
        strict_normalizer = MedicationNormalizer(confidence_threshold=0.9)
        
        # Grenzfall-Input
        input_text = "xnx 3mg 5x"  # Unsicheres Mapping für Xanax
        
        permissive_result = permissive_normalizer.normalize_medication(input_text)
        strict_result = strict_normalizer.normalize_medication(input_text)
        
        # Permissiver sollte weniger Unsicherheit zeigen
        assert permissive_result['uncertainty'] <= strict_result['uncertainty']
    
    def test_multiple_dosage_formats(self):
        """
        Test: Verschiedene Dosage-Formate
        """
        test_cases = [
            "Medicine 100mg 10x",
            "Drug 50 mg 5x", 
            "Tablet 25mg 20x",
            "Solution 10ml 15x",
            "Powder 2g 8x"
        ]
        
        for input_text in test_cases:
            result = self.normalizer.normalize_medication(input_text)
            assert result['dosage'] is not None

class TestReferenceDataIntegration:
    """
    Tests für Integration mit Referenz-Daten
    """
    
    def test_all_reference_abbreviations(self):
        """
        Test: Alle Abkürzungen aus Referenzliste funktionieren
        """
        from src.data.reference_meds import REFERENCE_MEDICATIONS
        
        normalizer = MedicationNormalizer()
        
        for medication, data in REFERENCE_MEDICATIONS.items():
            for abbrev in data['abbreviations']:
                result = normalizer.normalize_medication(f"{abbrev} 10x")
                
                # Sollte gemappt werden auf das korrekte Medikament
                assert result['normalized_name'] == medication
                assert result['confidence'] >= 0.8

if __name__ == "__main__":
    pytest.main([__file__]) 