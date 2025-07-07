"""
Unit-Tests für CSVProcessor
"""

import pytest
import tempfile
import pandas as pd
from pathlib import Path

from src.core.csv_processor import CSVProcessor

class TestCSVProcessor:
    """
    Test-Suite für CSVProcessor
    """
    
    def setup_method(self):
        """
        Setup für jeden Test
        """
        self.processor = CSVProcessor()
        self.test_data_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """
        Cleanup nach jedem Test
        """
        for file in self.test_data_dir.glob('*'):
            file.unlink()
        self.test_data_dir.rmdir()
    
    def test_read_text_file(self):
        """
        Test: Lesen von Text-Dateien
        """
        test_file = self.test_data_dir / "test.txt"
        test_content = ["Line 1", "Line 2", "", "Line 4"]
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_content))
        
        lines = self.processor.read_file(str(test_file))
        
        assert len(lines) == 3  # Leere Zeile wird entfernt
        assert lines == ["Line 1", "Line 2", "Line 4"]
    
    def test_read_csv_file(self):
        """
        Test: Lesen von CSV-Dateien
        """
        test_file = self.test_data_dir / "test.csv"
        test_content = "Name,Medication,Quantity\nMax,Tramadol,30\nAnna,Ibuprofen,20"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        lines = self.processor.read_file(str(test_file))
        
        assert len(lines) == 3
        assert "Name,Medication,Quantity" in lines[0]
    
    def test_unsupported_file_format(self):
        """
        Test: Nicht unterstütztes Dateiformat
        """
        test_file = self.test_data_dir / "test.doc"
        test_file.touch()
        
        with pytest.raises(ValueError, match="Dateiformat .doc nicht unterstützt"):
            self.processor.read_file(str(test_file))
    
    def test_nonexistent_file(self):
        """
        Test: Nicht-existierende Datei
        """
        with pytest.raises(FileNotFoundError):
            self.processor.read_file("nonexistent.txt")
    
    def test_detect_data_types(self):
        """
        Test: Datentyp-Erkennung
        """
        lines = [
            "Max Mustermann",
            "Musterstraße 123",
            "12345 Berlin",
            "Tramadol 225mg 30x",
            "Ibuprofen 400mg 20 stück",
            "Unknown line"
        ]
        
        classified = self.processor.detect_data_types(lines)
        
        assert len(classified['personal_names']) == 1
        assert len(classified['addresses']) == 1
        assert len(classified['postal_codes']) == 1
        assert len(classified['potential_medications']) == 2
        assert len(classified['unknown']) == 1
    
    def test_filter_medication_lines(self):
        """
        Test: Filterung von Medikamenten-Zeilen
        """
        lines = [
            "Max Mustermann",
            "Musterstraße 123",
            "Tramadol 225mg 30x",
            "Ibuprofen 400mg 20 stück",
            "12345 Berlin",
            "Xanax 3mg 10x"
        ]
        
        filtered = self.processor.filter_medication_lines(lines)
        
        assert len(filtered) == 3
        assert all(any(keyword in line.lower() for keyword in ['mg', 'x', 'stück']) 
                  for line in filtered)
    
    def test_create_output_csv(self):
        """
        Test: CSV-Output-Erstellung
        """
        data = [
            {'Product': 'Tramadol 225mg', 'Quantity': 30, 'Price per Unit (€)': '', 'Total Price (€)': ''},
            {'Product': 'Ibuprofen 400mg', 'Quantity': 20, 'Price per Unit (€)': '', 'Total Price (€)': ''}
        ]
        
        output_file = self.test_data_dir / "output.csv"
        success = self.processor.create_output_csv(data, str(output_file))
        
        assert success is True
        assert output_file.exists()
        
        # Prüfe Inhalt
        df = pd.read_csv(output_file)
        assert len(df) == 2
        assert list(df.columns) == ['Product', 'Quantity', 'Price per Unit (€)', 'Total Price (€)']
    
    def test_validate_input_format(self):
        """
        Test: Input-Format-Validierung
        """
        test_file = self.test_data_dir / "validation_test.txt"
        test_content = [
            "Max Mustermann",
            "Tramadol 225mg 30x",
            "Musterstraße 123",
            "Ibuprofen 400mg 20x"
        ]
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_content))
        
        validation = self.processor.validate_input_format(str(test_file))
        
        assert validation['valid'] is True
        assert validation['total_lines'] == 4
        assert validation['potential_medications'] == 2
        assert validation['personal_data_lines'] == 2  # Name + Adresse
    
    def test_read_csv_structured_with_different_separators(self):
        """
        Test: CSV mit verschiedenen Separatoren
        """
        # Teste Semicolon-separierte CSV
        test_file = self.test_data_dir / "semicolon.csv"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Name;Medication;Quantity\nMax;Tramadol;30\nAnna;Ibuprofen;20")
        
        df = self.processor.read_csv_structured(str(test_file))
        
        assert len(df.columns) == 3
        assert len(df) == 2
        assert 'Name' in df.columns
    
    def test_encoding_fallback(self):
        """
        Test: Encoding-Fallback für verschiedene Zeichensätze
        """
        test_file = self.test_data_dir / "encoding_test.txt"
        
        # Schreibe mit Latin-1 Encoding
        content = "Müller\nStraße\nIbuprofen 400mg 20x"
        with open(test_file, 'w', encoding='latin-1') as f:
            f.write(content)
        
        # Sollte trotzdem lesbar sein durch Fallback
        lines = self.processor.read_file(str(test_file))
        assert len(lines) == 3
    
    def test_medication_keyword_detection(self):
        """
        Test: Erkennung von Medikamenten-Keywords
        """
        test_lines = [
            "Tramadol mentioned here",
            "Something with mg dosage",
            "20x tablets",
            "Regular text line",
            "Ibuprofen reference",
            "5 stück pills"
        ]
        
        filtered = self.processor.filter_medication_lines(test_lines)
        
        # Sollte Zeilen mit Medikamenten-Keywords finden
        assert len(filtered) >= 4  # tramadol, mg, x, ibuprofen, stück
    
    def test_postal_code_recognition(self):
        """
        Test: PLZ-Erkennung
        """
        lines = [
            "12345 Berlin",
            "80331 München", 
            "Some other text",
            "10115 Berlin Mitte"
        ]
        
        classified = self.processor.detect_data_types(lines)
        
        assert len(classified['postal_codes']) == 3  # 3 Zeilen mit PLZ
    
    def test_address_pattern_recognition(self):
        """
        Test: Adressen-Pattern-Erkennung
        """
        lines = [
            "Musterstraße 123",
            "Hauptplatz 5",
            "Bahnhofweg 42",
            "Some random text",
            "Kirchgasse 7"
        ]
        
        classified = self.processor.detect_data_types(lines)
        
        assert len(classified['addresses']) == 4  # 4 Adressen erkannt

class TestCSVProcessorIntegration:
    """
    Integrations-Tests für CSVProcessor
    """
    
    def test_complete_file_processing_workflow(self):
        """
        Test: Kompletter Dateiverarbeitungs-Workflow
        """
        processor = CSVProcessor()
        
        # Erstelle realistische Test-Datei
        test_file = Path(tempfile.mktemp(suffix='.txt'))
        realistic_content = [
            "Patientendaten Export",
            "Max Mustermann",
            "Geburtsdatum: 01.01.1980",
            "Musterstraße 123",
            "12345 Berlin",
            "Telefon: 030-12345678",
            "",
            "Medikation:",
            "Tramadol 225mg 30x täglich",
            "Ibuprofen 400mg 20 stück bei Bedarf",
            "Xanax bars 3mg 10x abends",
            "Methylphenidate 20mg 15 tablets morgens",
            "",
            "Weitere Notizen:",
            "Patient verträgt Aspirin nicht gut"
        ]
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(realistic_content))
            
            # 1. Datei lesen
            lines = processor.read_file(str(test_file))
            assert len(lines) > 10
            
            # 2. Validieren
            validation = processor.validate_input_format(str(test_file))
            assert validation['valid'] is True
            assert validation['potential_medications'] >= 4
            
            # 3. Medikamenten-Zeilen filtern
            med_lines = processor.filter_medication_lines(lines)
            assert len(med_lines) >= 4
            
            # 4. Datentypen klassifizieren
            classified = processor.detect_data_types(lines)
            assert len(classified['potential_medications']) >= 4
            assert len(classified['personal_names']) >= 1
            assert len(classified['addresses']) >= 1
            
        finally:
            if test_file.exists():
                test_file.unlink()

if __name__ == "__main__":
    pytest.main([__file__]) 