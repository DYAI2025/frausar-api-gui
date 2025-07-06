"""
Unit-Tests für MedicationExtractor
"""

import pytest
import tempfile
import os
from pathlib import Path

from src.core.extractor import MedicationExtractor

class TestMedicationExtractor:
    """
    Test-Suite für MedicationExtractor
    """
    
    def setup_method(self):
        """
        Setup für jeden Test
        """
        self.extractor = MedicationExtractor(confidence_threshold=0.7)
        self.test_data_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """
        Cleanup nach jedem Test
        """
        # Aufräumen der temporären Dateien
        for file in self.test_data_dir.glob('*'):
            file.unlink()
        self.test_data_dir.rmdir()
    
    def test_process_file_with_valid_medications(self):
        """
        Test: Verarbeitung von gültigen Medikamenten-Daten
        """
        # Test-Datei erstellen
        test_file = self.test_data_dir / "test_meds.txt"
        test_content = [
            "Max Mustermann",
            "Tramadol 225mg 30x",
            "Ibuprofen 400mg 20 stück",
            "Musterstraße 123",
            "12345 Berlin"
        ]
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_content))
        
        # Verarbeitung (nicht-interaktiv)
        result = self.extractor.process_file(str(test_file), interactive=False)
        
        # Assertions
        assert result['success'] is True
        assert len(result['results']) == 2  # 2 Medikamente
        
        # Prüfe Statistiken
        stats = result['statistics']
        assert stats['input_lines'] == 5
        assert stats['medication_lines'] == 2
        assert stats['mapped_medications'] == 2
    
    def test_process_file_with_no_medications(self):
        """
        Test: Datei ohne Medikamenten-Daten
        """
        test_file = self.test_data_dir / "no_meds.txt"
        test_content = [
            "Max Mustermann",
            "Musterstraße 123", 
            "12345 Berlin",
            "Email: max@example.com"
        ]
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_content))
        
        result = self.extractor.process_file(str(test_file), interactive=False)
        
        assert result['success'] is False
        assert 'Keine Medikamenten-Daten' in result['error']
    
    def test_process_file_nonexistent(self):
        """
        Test: Nicht-existierende Datei
        """
        result = self.extractor.process_file("nonexistent.txt", interactive=False)
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_custom_mapping_functionality(self):
        """
        Test: Benutzerdefinierte Mappings
        """
        # Custom-Mapping hinzufügen
        self.extractor.add_custom_mapping("special_med 100", "Tramadol 225mg")
        
        # Test-Datei mit Custom-Mapping
        test_file = self.test_data_dir / "custom_mapping.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("special_med 100 5x")
        
        result = self.extractor.process_file(str(test_file), interactive=False)
        
        assert result['success'] is True
        assert len(result['results']) == 1
        assert result['results'][0]['Product'] == 'Tramadol 225mg'
        assert result['results'][0]['Quantity'] == 5
    
    def test_fuzzy_matching(self):
        """
        Test: Fuzzy-Matching für ähnliche Namen
        """
        test_file = self.test_data_dir / "fuzzy_test.txt"
        test_content = [
            "tramadol 225 mg 10x",  # Exakte Übereinstimmung mit Spaces
            "ibu 400 20x",          # Abkürzung 
            "xnx 3mg 5x"            # Fuzzy für Xanax
        ]
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_content))
        
        result = self.extractor.process_file(str(test_file), interactive=False)
        
        assert result['success'] is True
        # Mindestens 2 sollten gemappt werden (tramadol und ibu sicher)
        assert len(result['results']) >= 2
    
    def test_quantity_aggregation(self):
        """
        Test: Aggregation von Mengen für gleiche Medikamente
        """
        test_file = self.test_data_dir / "aggregation_test.txt"
        test_content = [
            "Tramadol 225mg 10x",
            "Trama 225 20x",  # Gleiche Medikament, andere Schreibweise
            "Ibuprofen 400mg 5 stück"
        ]
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_content))
        
        result = self.extractor.process_file(str(test_file), interactive=False)
        
        assert result['success'] is True
        
        # Finde Tramadol-Eintrag
        tramadol_entry = None
        for item in result['results']:
            if 'Tramadol 225mg' in item['Product']:
                tramadol_entry = item
                break
        
        assert tramadol_entry is not None
        assert tramadol_entry['Quantity'] == 30  # 10 + 20
    
    def test_processing_statistics(self):
        """
        Test: Verarbeitungsstatistiken
        """
        test_file = self.test_data_dir / "stats_test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Tramadol 225mg 10x\nIbuprofen 400mg 5x")
        
        self.extractor.process_file(str(test_file), interactive=False)
        stats = self.extractor.get_processing_statistics()
        
        assert 'file_read' in stats
        assert 'medication_filter' in stats
        assert stats['file_read']['total_lines'] == 2
    
    def test_confidence_threshold_effect(self):
        """
        Test: Auswirkung des Confidence-Thresholds
        """
        # Hoher Threshold (0.9) - streng
        strict_extractor = MedicationExtractor(confidence_threshold=0.9)
        
        # Niedriger Threshold (0.3) - permissiv
        permissive_extractor = MedicationExtractor(confidence_threshold=0.3)
        
        test_file = self.test_data_dir / "confidence_test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("xnx 3mg 5x")  # Sehr unsichere Übereinstimmung für Xanax
        
        strict_result = strict_extractor.process_file(str(test_file), interactive=False)
        permissive_result = permissive_extractor.process_file(str(test_file), interactive=False)
        
        # Permissiver Extraktor sollte mehr/bessere Mappings finden
        assert len(permissive_result.get('results', [])) >= len(strict_result.get('results', []))

class TestMedicationExtractorIntegration:
    """
    Integrations-Tests für komplette Workflows
    """
    
    def test_complete_workflow_with_export(self):
        """
        Test: Kompletter Workflow mit Export (ohne GUI)
        """
        extractor = MedicationExtractor()
        
        # Test-Datei
        test_file = Path(tempfile.mktemp(suffix='.txt'))
        test_content = [
            "Patient: Max Mustermann",
            "Tramadol 225mg 30x",
            "Ibuprofen 400mg 20x",
            "Xanax 3mg 10x"
        ]
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_content))
        
        try:
            # Verarbeitung
            result = extractor.process_file(str(test_file), interactive=False)
            
            assert result['success'] is True
            assert len(result['results']) == 3
            
            # Prüfe dass alle erwarteten Medikamente vorhanden sind
            product_names = [item['Product'] for item in result['results']]
            assert any('Tramadol' in name for name in product_names)
            assert any('Ibuprofen' in name for name in product_names)
            assert any('Xanax' in name for name in product_names)
            
        finally:
            # Cleanup
            if test_file.exists():
                test_file.unlink()

if __name__ == "__main__":
    pytest.main([__file__]) 