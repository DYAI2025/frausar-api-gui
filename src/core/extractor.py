"""
Haupt-Medikamenten-Extraktor - Orchestriert kompletten Workflow
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from .csv_processor import CSVProcessor
from .normalizer import MedicationNormalizer
from ..security.password_manager import PasswordManager
from ..gui.password_dialog import PasswordDialog

class MedicationExtractor:
    """
    Haupt-Klasse für Medikamenten-Extraktion und Normalisierung
    """
    
    def __init__(self, confidence_threshold: float = 0.7):
        """
        Initialisiert den Extraktor
        
        Args:
            confidence_threshold: Mindest-Confidence für automatisches Mapping
        """
        self.csv_processor = CSVProcessor()
        self.normalizer = MedicationNormalizer(confidence_threshold)
        self.password_manager = PasswordManager()
        self.processing_log = []
        
    def process_file(self, file_path: str, interactive: bool = True) -> Dict[str, Any]:
        """
        Verarbeitet Input-Datei komplett durch den Workflow
        
        Args:
            file_path: Pfad zur Input-Datei
            interactive: Ob User-Feedback bei Unsicherheiten eingeholt werden soll
            
        Returns:
            Dict: Vollständige Verarbeitungsergebnisse
        """
        try:
            # 1. Datei validieren und einlesen
            print(f"📄 Lese Datei: {file_path}")
            validation_result = self.csv_processor.validate_input_format(file_path)
            
            if not validation_result['valid']:
                raise ValueError(f"Datei-Validierung fehlgeschlagen: {validation_result['error']}")
            
            lines = self.csv_processor.read_file(file_path)
            self._log_processing_step("file_read", {
                'total_lines': len(lines),
                'validation': validation_result
            })
            
            # 2. Medikamenten-Zeilen extrahieren
            print(f"🔍 Filtere {len(lines)} Zeilen nach Medikamenten...")
            medication_lines = self.csv_processor.filter_medication_lines(lines)
            
            self._log_processing_step("medication_filter", {
                'input_lines': len(lines),
                'filtered_lines': len(medication_lines)
            })
            
            if not medication_lines:
                return {
                    'success': False,
                    'error': 'Keine Medikamenten-Daten in der Datei gefunden',
                    'suggestions': 'Überprüfen Sie, ob die Datei Dosage-Informationen (mg, ml) oder Medikamenten-Namen enthält'
                }
            
            # 3. Normalisierung durchführen
            print(f"🧠 Normalisiere {len(medication_lines)} Medikamenten-Einträge...")
            normalization_results = self.normalizer.batch_normalize(medication_lines)
            
            # 4. Interactive Feedback bei Unsicherheiten
            if interactive:
                uncertainty_summary = self.normalizer.get_uncertainty_summary()
                if uncertainty_summary:
                    print(f"❓ {len(uncertainty_summary)} unsichere Mappings gefunden - hole User-Feedback...")
                    self._handle_uncertainties(uncertainty_summary)
                    
                    # Re-normalisierung nach User-Feedback
                    normalization_results = self.normalizer.batch_normalize(medication_lines)
            
            # 5. Aggregation
            print("📊 Aggregiere Mengen...")
            aggregated_data = self.normalizer.aggregate_quantities(normalization_results)
            
            # 6. Qualitäts-Validierung
            quality_metrics = self.normalizer.validate_mapping_quality(normalization_results)
            
            self._log_processing_step("normalization_complete", {
                'total_processed': len(normalization_results),
                'successfully_mapped': quality_metrics['mapped'],
                'quality_score': quality_metrics['quality_score']
            })
            
            # 7. Ergebnisse strukturieren
            final_results = list(aggregated_data.values())
            
            return {
                'success': True,
                'results': final_results,
                'statistics': {
                    'input_lines': len(lines),
                    'medication_lines': len(medication_lines),
                    'mapped_medications': len(final_results),
                    'quality_metrics': quality_metrics
                },
                'processing_log': self.processing_log
            }
            
        except Exception as e:
            error_msg = f"Fehler bei der Verarbeitung: {str(e)}"
            self._log_processing_step("error", {'error': error_msg})
            return {
                'success': False,
                'error': error_msg,
                'processing_log': self.processing_log
            }
    
    def export_secure_csv(self, processing_result: Dict[str, Any], output_path: str) -> bool:
        """
        Exportiert Ergebnisse als passwortgeschützte CSV
        
        Args:
            processing_result: Verarbeitungsergebnisse
            output_path: Pfad für Output-Datei
            
        Returns:
            bool: True wenn erfolgreich
        """
        try:
            if not processing_result['success']:
                print(f"❌ Kann nicht exportieren - Verarbeitung war nicht erfolgreich")
                return False
            
            # 1. Temporäre CSV erstellen
            temp_csv_path = output_path.replace('.csv', '_temp.csv')
            success = self.csv_processor.create_output_csv(
                processing_result['results'], 
                temp_csv_path
            )
            
            if not success:
                print("❌ Fehler beim Erstellen der temporären CSV")
                return False
            
            # 2. Passwort-Dialog anzeigen
            password_dialog = PasswordDialog()
            password = password_dialog.get_password()
            
            if not password:
                print("❌ Kein Passwort eingegeben - Export abgebrochen")
                os.remove(temp_csv_path)
                return False
            
            # 3. CSV verschlüsseln
            encrypted_path = output_path.replace('.csv', '.encrypted')
            success = self.password_manager.encrypt_csv_file(temp_csv_path, encrypted_path, password)
            
            if success:
                # Aufräumen
                os.remove(temp_csv_path)
                print(f"✅ Passwortgeschützte Datei erstellt: {encrypted_path}")
                print(f"📊 {len(processing_result['results'])} Medikamente exportiert")
                return True
            else:
                print("❌ Fehler bei der Verschlüsselung")
                os.remove(temp_csv_path)
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Export: {e}")
            return False
    
    def add_custom_mapping(self, input_text: str, medication_name: str):
        """
        Fügt benutzerdefiniertes Mapping hinzu
        
        Args:
            input_text: Original-Text
            medication_name: Gemappter Medikamenten-Name
        """
        self.normalizer.add_custom_mapping(input_text, medication_name)
        print(f"✅ Custom-Mapping hinzugefügt: '{input_text}' → '{medication_name}'")
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """
        Gibt detaillierte Verarbeitungsstatistiken zurück
        
        Returns:
            Dict: Statistiken des letzten Verarbeitungslaufs
        """
        if not self.processing_log:
            return {'message': 'Noch keine Verarbeitung durchgeführt'}
        
        stats = {}
        for entry in self.processing_log:
            stats[entry['step']] = entry['data']
        
        return stats
    
    def _handle_uncertainties(self, uncertainties: List[Dict[str, Any]]):
        """
        Behandelt unsichere Mappings mit User-Interaction
        
        Args:
            uncertainties: Liste unsicherer Mappings
        """
        print("\n" + "="*60)
        print("🤔 UNSICHERE MAPPINGS - BITTE BESTÄTIGEN:")
        print("="*60)
        
        for i, uncertainty in enumerate(uncertainties, 1):
            input_text = uncertainty['input']
            suggested_match = uncertainty['suggested_match']
            confidence = uncertainty['confidence']
            
            print(f"\n[{i}/{len(uncertainties)}] Input: '{input_text}'")
            
            if suggested_match:
                print(f"Vorschlag: '{suggested_match}' (Confidence: {confidence:.2f})")
                response = input("Ist dieses Mapping korrekt? (j/n/andere): ").lower().strip()
                
                if response in ['j', 'ja', 'y', 'yes']:
                    self.add_custom_mapping(input_text, suggested_match)
                elif response in ['n', 'nein', 'no']:
                    new_mapping = input("Bitte geben Sie den korrekten Medikamenten-Namen ein: ").strip()
                    if new_mapping:
                        self.add_custom_mapping(input_text, new_mapping)
                else:
                    # User hat eine andere Option eingegeben
                    self.add_custom_mapping(input_text, response)
            else:
                print("Kein Vorschlag gefunden.")
                new_mapping = input("Bitte geben Sie den Medikamenten-Namen ein (oder Enter zum Überspringen): ").strip()
                if new_mapping:
                    self.add_custom_mapping(input_text, new_mapping)
        
        print("\n✅ User-Feedback verarbeitet. Führe Re-Normalisierung durch...")
    
    def _log_processing_step(self, step: str, data: Dict[str, Any]):
        """
        Loggt Verarbeitungsschritt
        
        Args:
            step: Name des Schritts
            data: Zugehörige Daten
        """
        import datetime
        self.processing_log.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'step': step,
            'data': data
        })
    
    def clear_processing_log(self):
        """
        Löscht Verarbeitungslog
        """
        self.processing_log.clear()
        self.normalizer.clear_uncertainty_log() 