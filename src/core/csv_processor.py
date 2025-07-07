"""
CSV und Text-Datei Processor für Medikamenten-Daten
"""

import pandas as pd
import csv
import re
from typing import List, Dict, Any, Optional, Union
from pathlib import Path

class CSVProcessor:
    """
    Verarbeitet CSV- und Text-Dateien mit Medikamenten-Daten
    """
    
    def __init__(self):
        self.supported_formats = ['.csv', '.txt', '.tsv']
        
    def read_file(self, file_path: str) -> List[str]:
        """
        Liest Datei und gibt Zeilen als Liste zurück
        
        Args:
            file_path: Pfad zur Datei
            
        Returns:
            List[str]: Liste aller Zeilen
            
        Raises:
            FileNotFoundError: Wenn Datei nicht existiert
            ValueError: Wenn Format nicht unterstützt wird
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
            
        if file_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Dateiformat {file_path.suffix} nicht unterstützt. "
                           f"Unterstützte Formate: {self.supported_formats}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            # Leere Zeilen und Whitespace entfernen
            return [line.strip() for line in lines if line.strip()]
            
        except UnicodeDecodeError:
            # Fallback für andere Encodings
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    lines = file.readlines()
                return [line.strip() for line in lines if line.strip()]
            except Exception as e:
                raise ValueError(f"Fehler beim Lesen der Datei: {e}")
    
    def read_csv_structured(self, file_path: str) -> pd.DataFrame:
        """
        Liest CSV-Datei als strukturiertes DataFrame
        
        Args:
            file_path: Pfad zur CSV-Datei
            
        Returns:
            pd.DataFrame: Strukturierte Daten
        """
        try:
            # Versuche verschiedene Separatoren
            separators = [',', ';', '\t']
            
            for sep in separators:
                try:
                    df = pd.read_csv(file_path, sep=sep, encoding='utf-8')
                    if len(df.columns) > 1:  # Erfolgreich geparst
                        return df
                except:
                    continue
                    
            # Fallback: Als einspaltige Daten lesen
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file.readlines() if line.strip()]
                
            return pd.DataFrame({'text': lines})
            
        except Exception as e:
            raise ValueError(f"Fehler beim Parsen der CSV-Datei: {e}")
    
    def detect_data_types(self, lines: List[str]) -> Dict[str, List[str]]:
        """
        Klassifiziert Zeilen nach Datentyp (Name, Adresse, Medikament, etc.)
        
        Args:
            lines: Liste der Textzeilen
            
        Returns:
            Dict[str, List[str]]: Klassifizierte Daten
        """
        result = {
            'potential_medications': [],
            'personal_names': [],
            'addresses': [],
            'postal_codes': [],
            'unknown': []
        }
        
        # Regex-Pattern für verschiedene Datentypen
        postal_code_pattern = re.compile(r'\b\d{5}\b')  # Deutsche PLZ
        address_pattern = re.compile(r'(straße|str\.|platz|weg|allee|gasse)', re.IGNORECASE)
        medication_pattern = re.compile(r'(\d+\s*(mg|ml|g|x|stück|tablets?))', re.IGNORECASE)
        name_pattern = re.compile(r'^[A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+$')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # PLZ erkennen
            if postal_code_pattern.search(line):
                result['postal_codes'].append(line)
                
            # Adressen erkennen
            elif address_pattern.search(line):
                result['addresses'].append(line)
                
            # Potentielle Medikamente (enthalten Dosage-Informationen)
            elif medication_pattern.search(line):
                result['potential_medications'].append(line)
                
            # Namen erkennen (Vor- und Nachname, beginnend mit Großbuchstaben)
            elif name_pattern.match(line):
                result['personal_names'].append(line)
                
            # Alles andere als unbekannt markieren
            else:
                result['unknown'].append(line)
                
        return result
    
    def filter_medication_lines(self, lines: List[str]) -> List[str]:
        """
        Filtert Zeilen, die wahrscheinlich Medikamente enthalten
        
        Args:
            lines: Alle Textzeilen
            
        Returns:
            List[str]: Gefilterte Medikamenten-Zeilen
        """
        medication_keywords = [
            'mg', 'ml', 'gram', 'tablet', 'pill', 'stück', 'x',
            'tramadol', 'ibuprofen', 'xanax', 'alprazolam', 'methylphenidate',
            'paracetamol', 'aspirin', 'zopiclon'
        ]
        
        filtered_lines = []
        
        for line in lines:
            line_lower = line.lower()
            
            # Überspringe offensichtliche Namen und Adressen
            if any(word in line_lower for word in ['straße', 'str.', 'platz', 'weg']):
                continue
                
            if re.match(r'^\d{5}\s', line):  # Beginnt mit PLZ
                continue
                
            # Prüfe auf Medikamenten-Keywords
            if any(keyword in line_lower for keyword in medication_keywords):
                filtered_lines.append(line)
                
        return filtered_lines
    
    def create_output_csv(self, data: List[Dict[str, Any]], output_path: str) -> bool:
        """
        Erstellt Output-CSV mit standardisiertem Format
        
        Args:
            data: Liste von Medikamenten-Daten
            output_path: Pfad für Output-Datei
            
        Returns:
            bool: True wenn erfolgreich
        """
        try:
            df = pd.DataFrame(data)
            
            # Standardisiere Spalten-Reihenfolge
            standard_columns = ['Product', 'Quantity', 'Price per Unit (€)', 'Total Price (€)']
            
            # Füge fehlende Spalten hinzu
            for col in standard_columns:
                if col not in df.columns:
                    df[col] = '' if col != 'Quantity' else 0
                    
            # Sortiere nach Standard-Reihenfolge
            df = df[standard_columns]
            
            # Speichere CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            return True
            
        except Exception as e:
            print(f"Fehler beim Erstellen der Output-CSV: {e}")
            return False
    
    def validate_input_format(self, file_path: str) -> Dict[str, Any]:
        """
        Validiert Input-Format und gibt Statistiken zurück
        
        Args:
            file_path: Pfad zur Input-Datei
            
        Returns:
            Dict[str, Any]: Validierungs-Ergebnisse
        """
        try:
            lines = self.read_file(file_path)
            classified_data = self.detect_data_types(lines)
            
            return {
                'valid': True,
                'total_lines': len(lines),
                'potential_medications': len(classified_data['potential_medications']),
                'personal_data_lines': len(classified_data['personal_names']) + 
                                     len(classified_data['addresses']) + 
                                     len(classified_data['postal_codes']),
                'unknown_lines': len(classified_data['unknown']),
                'classification': classified_data
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            } 