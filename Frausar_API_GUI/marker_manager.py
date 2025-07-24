#!/usr/bin/env python3
"""
MARKER MANAGER
==============

Zentrale Verwaltung für Marker-Formate und Kategorisierung
- Multi-Format-Support (.txt, .py, .json, .yaml, .yml)
- Icon-basierte Kategorisierung
- Format-Erkennung und Validierung
"""

import os
import re
import yaml
import json
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class MarkerManager:
    """Zentrale Klasse für Marker-Verwaltung und Format-Handling."""
    
    def __init__(self):
        """Initialisiert den MarkerManager."""
        self.supported_formats = ['.txt', '.py', '.json', '.yaml', '.yml']
        self.format_icons = {
            '.txt': '📄', '.py': '🐍', '.json': '📊', 
            '.yaml': '📊', '.yml': '📊', 'folder': '📁'
        }
        
        # Format-spezifische Parser
        self.parsers = {
            '.txt': self._parse_txt_marker,
            '.py': self._parse_py_marker,
            '.json': self._parse_json_marker,
            '.yaml': self._parse_yaml_marker,
            '.yml': self._parse_yaml_marker
        }
        
        # Validierungsregeln
        self.validation_rules = {
            'required_fields': ['id', 'level', 'description'],
            'optional_fields': ['category', 'examples', 'tags'],
            'field_types': {
                'id': str,
                'level': int,
                'description': str,
                'category': str,
                'examples': list,
                'tags': list
            }
        }
    
    def get_file_icon(self, filename: str) -> str:
        """Gibt das passende Icon für eine Datei zurück."""
        if os.path.isdir(filename):
            return self.format_icons['folder']
        
        ext = Path(filename).suffix.lower()
        return self.format_icons.get(ext, '📄')
    
    def is_supported_format(self, filename: str) -> bool:
        """Prüft ob das Dateiformat unterstützt wird."""
        ext = Path(filename).suffix.lower()
        return ext in self.supported_formats
    
    def parse_marker_content(self, content: str, filename: str) -> Dict[str, Any]:
        """Parst Marker-Inhalt basierend auf Dateiformat."""
        ext = Path(filename).suffix.lower()
        
        if ext not in self.parsers:
            raise ValueError(f"Nicht unterstütztes Format: {ext}")
        
        try:
            return self.parsers[ext](content, filename)
        except Exception as e:
            return self._create_error_marker(content, filename, str(e))
    
    def _parse_txt_marker(self, content: str, filename: str) -> Dict[str, Any]:
        """Parst TXT-Marker mit Regex-basierter Extraktion."""
        marker_data = {
            'id': Path(filename).stem,
            'level': 1,
            'description': '',
            'category': 'general',
            'examples': [],
            'source_file': filename,
            'format': 'txt'
        }
        
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # ID-Extraktion (erste Zeile in Großbuchstaben)
            if not marker_data['id'] or marker_data['id'] == Path(filename).stem:
                if line.upper() == line and len(line) > 3 and not ':' in line:
                    marker_data['id'] = line
                    continue
            
            # Level-Extraktion
            if 'level' in line.lower():
                level_match = re.search(r'level\s*:?\s*(\d+)', line.lower())
                if level_match:
                    marker_data['level'] = int(level_match.group(1))
            
            # Beschreibung-Extraktion
            elif 'beschreibung' in line.lower() or 'description' in line.lower():
                desc_match = re.search(r'(?:beschreibung|description)\s*:?\s*(.+)', line.lower())
                if desc_match:
                    marker_data['description'] = desc_match.group(1).strip()
            
            # Kategorie-Extraktion
            elif 'kategorie' in line.lower() or 'category' in line.lower():
                cat_match = re.search(r'(?:kategorie|category)\s*:?\s*(.+)', line.lower())
                if cat_match:
                    marker_data['category'] = cat_match.group(1).strip()
            
            # Beispiele-Extraktion
            elif line.startswith('-') or line.startswith('*'):
                example = line[1:].strip()
                if example:
                    marker_data['examples'].append(example)
        
        # Fallback-Beschreibung
        if not marker_data['description']:
            marker_data['description'] = f"Marker {marker_data['id']}"
        
        return marker_data
    
    def _parse_py_marker(self, content: str, filename: str) -> Dict[str, Any]:
        """Parst Python-Marker mit AST-Analyse."""
        marker_data = {
            'id': Path(filename).stem,
            'level': 1,
            'description': '',
            'category': 'python',
            'examples': [],
            'source_file': filename,
            'format': 'py'
        }
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    marker_data['id'] = node.name
                    if node.docstring:
                        marker_data['description'] = node.docstring
                elif isinstance(node, ast.FunctionDef):
                    if not marker_data['description'] and node.docstring:
                        marker_data['description'] = node.docstring
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id.lower() in ['level', 'description', 'category']:
                                if isinstance(node.value, ast.Constant):
                                    if target.id.lower() == 'level':
                                        marker_data['level'] = int(node.value.value)
                                    elif target.id.lower() == 'description':
                                        marker_data['description'] = str(node.value.value)
                                    elif target.id.lower() == 'category':
                                        marker_data['category'] = str(node.value.value)
            
        except SyntaxError:
            # Fallback auf Text-Parsing
            return self._parse_txt_marker(content, filename)
        
        # Fallback-Beschreibung
        if not marker_data['description']:
            marker_data['description'] = f"Python Marker {marker_data['id']}"
        
        return marker_data
    
    def _parse_json_marker(self, content: str, filename: str) -> Dict[str, Any]:
        """Parst JSON-Marker."""
        try:
            marker_data = json.loads(content)
            marker_data['source_file'] = filename
            marker_data['format'] = 'json'
            
            # Standardwerte setzen
            if 'id' not in marker_data:
                marker_data['id'] = Path(filename).stem
            if 'level' not in marker_data:
                marker_data['level'] = 1
            if 'category' not in marker_data:
                marker_data['category'] = 'general'
            if 'examples' not in marker_data:
                marker_data['examples'] = []
            
            return marker_data
            
        except json.JSONDecodeError as e:
            return self._create_error_marker(content, filename, f"JSON-Fehler: {str(e)}")
    
    def _parse_yaml_marker(self, content: str, filename: str) -> Dict[str, Any]:
        """Parst YAML-Marker."""
        try:
            marker_data = yaml.safe_load(content)
            if marker_data is None:
                marker_data = {}
            
            marker_data['source_file'] = filename
            marker_data['format'] = 'yaml'
            
            # Standardwerte setzen
            if 'id' not in marker_data:
                marker_data['id'] = Path(filename).stem
            if 'level' not in marker_data:
                marker_data['level'] = 1
            if 'category' not in marker_data:
                marker_data['category'] = 'general'
            if 'examples' not in marker_data:
                marker_data['examples'] = []
            
            return marker_data
            
        except yaml.YAMLError as e:
            return self._create_error_marker(content, filename, f"YAML-Fehler: {str(e)}")
    
    def _create_error_marker(self, content: str, filename: str, error: str) -> Dict[str, Any]:
        """Erstellt einen Fehler-Marker für ungültige Dateien."""
        return {
            'id': Path(filename).stem,
            'level': 1,
            'description': f"Fehler beim Parsen: {error}",
            'category': 'error',
            'examples': [],
            'source_file': filename,
            'format': Path(filename).suffix.lower(),
            'error': error,
            'raw_content': content
        }
    
    def validate_marker(self, marker_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validiert einen Marker und gibt Fehler zurück."""
        errors = []
        
        # Pflichtfelder prüfen
        for field in self.validation_rules['required_fields']:
            if field not in marker_data or not marker_data[field]:
                errors.append(f"Pflichtfeld fehlt: {field}")
        
        # Feldtypen prüfen
        for field, expected_type in self.validation_rules['field_types'].items():
            if field in marker_data:
                if not isinstance(marker_data[field], expected_type):
                    errors.append(f"Falscher Typ für {field}: erwartet {expected_type.__name__}")
        
        # Level-Bereich prüfen
        if 'level' in marker_data:
            level = marker_data['level']
            if not isinstance(level, int) or level < 1 or level > 10:
                errors.append("Level muss zwischen 1 und 10 liegen")
        
        return len(errors) == 0, errors
    
    def get_marker_summary(self, marker_data: Dict[str, Any]) -> str:
        """Erstellt eine Zusammenfassung für einen Marker."""
        icon = self.get_file_icon(marker_data.get('source_file', ''))
        id_str = marker_data.get('id', 'Unbekannt')
        level = marker_data.get('level', 1)
        category = marker_data.get('category', 'general')
        
        return f"{icon} {id_str} (Level {level}, {category})"
    
    def collect_markers_from_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Sammelt alle Marker aus einem Verzeichnis."""
        markers = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            return markers
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and self.is_supported_format(str(file_path)):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    marker_data = self.parse_marker_content(content, str(file_path))
                    markers.append(marker_data)
                    
                except Exception as e:
                    # Fehler-Marker erstellen
                    error_marker = self._create_error_marker(
                        f"Fehler beim Lesen: {str(e)}", 
                        str(file_path), 
                        str(e)
                    )
                    markers.append(error_marker)
        
        return markers
    
    def filter_markers(self, markers: List[Dict[str, Any]], 
                      search_query: str = "", 
                      category_filter: str = "",
                      format_filter: str = "",
                      error_only: bool = False) -> List[Dict[str, Any]]:
        """Filtert Marker basierend auf verschiedenen Kriterien."""
        filtered_markers = markers
        
        # Fehler-Marker filtern
        if error_only:
            filtered_markers = [m for m in filtered_markers if 'error' in m]
        else:
            filtered_markers = [m for m in filtered_markers if 'error' not in m]
        
        # Such-Query filtern
        if search_query:
            query_lower = search_query.lower()
            filtered_markers = [
                m for m in filtered_markers
                if (query_lower in m.get('id', '').lower() or
                    query_lower in m.get('description', '').lower() or
                    query_lower in m.get('category', '').lower())
            ]
        
        # Kategorie filtern
        if category_filter:
            filtered_markers = [
                m for m in filtered_markers
                if m.get('category', '').lower() == category_filter.lower()
            ]
        
        # Format filtern
        if format_filter:
            filtered_markers = [
                m for m in filtered_markers
                if m.get('format', '').lower() == format_filter.lower()
            ]
        
        return filtered_markers
    
    def smart_parse_text(self, text: str) -> Dict[str, Any]:
        """Intelligente Text-Parsing mit automatischer Korrektur"""
        lines = text.strip().split('\n')
        marker_data = {}
        
        # ID wird später gesetzt, wenn gefunden
        marker_id_found = False
        
        current_key = None
        examples = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Zuerst nach Marker-ID suchen (erste Zeile in Großbuchstaben)
            if not marker_id_found and line.upper() == line and len(line) > 3 and not ':' in line:
                marker_data['id'] = line
                marker_id_found = True
                continue
            
            # Verschiedene Formate erkennen und korrigieren
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip().strip('"\'')
                
                # Schlüssel-Mapping
                key_mapping = {
                    'level': 'level',
                    'beschreibung': 'description',
                    'description': 'description',
                    'kategorie': 'category',
                    'category': 'category',
                    'beispiele': 'examples',
                    'examples': 'examples'
                }
                
                if key in key_mapping:
                    current_key = key_mapping[key]
                    if current_key == 'examples':
                        examples.append(value)
                    else:
                        marker_data[current_key] = value
                elif key.upper() == key and not marker_id_found:  # ID in Großbuchstaben
                    marker_data['id'] = value
                    marker_id_found = True
                else:
                    marker_data[key] = value
            
            elif current_key == 'examples' and line.startswith('-'):
                examples.append(line[1:].strip())
            
            elif 'level' in line.lower():
                # Level aus verschiedenen Formaten extrahieren
                level_match = re.search(r'level\s*:?\s*(\d+)', line.lower())
                if level_match:
                    marker_data['level'] = int(level_match.group(1))
            
            elif 'beschreibung' in line.lower() or 'description' in line.lower():
                # Beschreibung extrahieren
                desc_match = re.search(r'(?:beschreibung|description)\s*:?\s*(.+)', line.lower())
                if desc_match:
                    marker_data['description'] = desc_match.group(1).strip()
        
        # Automatische ID-Generierung falls keine gefunden
        if 'id' not in marker_data:
            marker_data['id'] = f"marker_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Standardwerte setzen
        if 'level' not in marker_data:
            marker_data['level'] = 1
        
        if 'description' not in marker_data:
            marker_data['description'] = f"Marker {marker_data['id']}"
        
        if 'category' not in marker_data:
            marker_data['category'] = 'general'
        
        if examples:
            marker_data['examples'] = examples
        
        return marker_data


# Test-Funktion
def test_marker_manager():
    """Testet den MarkerManager."""
    manager = MarkerManager()
    
    # Test-Daten
    test_content = """
    TEST_MARKER
    Level: 2
    Beschreibung: Ein Test-Marker
    Kategorie: test
    Beispiele:
    - Beispiel 1
    - Beispiel 2
    """
    
    # Test-Parsing
    result = manager.parse_marker_content(test_content, "test_marker.txt")
    print("Parsing-Ergebnis:", result)
    
    # Test-Validierung
    is_valid, errors = manager.validate_marker(result)
    print("Validierung:", is_valid, errors)
    
    # Test-Filterung
    markers = [result]
    filtered = manager.filter_markers(markers, search_query="test")
    print("Filterung:", len(filtered))


if __name__ == "__main__":
    test_marker_manager() 