#!/usr/bin/env python3
"""
TEST SUITE - PHASE 1 FEATURES
=============================

Umfassende Tests für alle Phase 1 Features:
- Multi-Format-Support
- Live-Suche
- Marker-Management
- Such-Engine
"""

import unittest
import tempfile
import os
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any

# Eigene Module importieren
from marker_manager import MarkerManager
from search_engine import SearchEngine, FuzzyMatcher, FilterManager


class TestMarkerManager(unittest.TestCase):
    """Tests für den MarkerManager."""
    
    def setUp(self):
        """Setzt Test-Umgebung auf."""
        self.manager = MarkerManager()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Räumt Test-Umgebung auf."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_supported_formats(self):
        """Testet unterstützte Formate."""
        self.assertIn('.txt', self.manager.supported_formats)
        self.assertIn('.py', self.manager.supported_formats)
        self.assertIn('.json', self.manager.supported_formats)
        self.assertIn('.yaml', self.manager.supported_formats)
        self.assertIn('.yml', self.manager.supported_formats)
    
    def test_file_icons(self):
        """Testet Icon-Zuordnung."""
        self.assertEqual(self.manager.get_file_icon('test.txt'), '📄')
        self.assertEqual(self.manager.get_file_icon('test.py'), '🐍')
        self.assertEqual(self.manager.get_file_icon('test.json'), '📊')
        self.assertEqual(self.manager.get_file_icon('test.yaml'), '📊')
        self.assertEqual(self.manager.get_file_icon('test.yml'), '📊')
    
    def test_txt_marker_parsing(self):
        """Testet TXT-Marker-Parsing."""
        content = """
        TEST_MARKER
        Level: 2
        Beschreibung: Ein Test-Marker
        Kategorie: test
        Beispiele:
        - Beispiel 1
        - Beispiel 2
        """
        
        result = self.manager.parse_marker_content(content, "test_marker.txt")
        
        self.assertEqual(result['id'], 'TEST_MARKER')
        self.assertEqual(result['level'], 2)
        self.assertEqual(result['description'], 'ein test-marker')
        self.assertEqual(result['category'], 'test')
        self.assertEqual(len(result['examples']), 2)
        self.assertEqual(result['format'], 'txt')
    
    def test_yaml_marker_parsing(self):
        """Testet YAML-Marker-Parsing."""
        content = """
        id: YAML_MARKER
        level: 3
        description: Ein YAML-Marker
        category: yaml
        examples:
          - YAML-Beispiel 1
          - YAML-Beispiel 2
        """
        
        result = self.manager.parse_marker_content(content, "test_marker.yaml")
        
        self.assertEqual(result['id'], 'YAML_MARKER')
        self.assertEqual(result['level'], 3)
        self.assertEqual(result['description'], 'Ein YAML-Marker')
        self.assertEqual(result['category'], 'yaml')
        self.assertEqual(len(result['examples']), 2)
        self.assertEqual(result['format'], 'yaml')
    
    def test_json_marker_parsing(self):
        """Testet JSON-Marker-Parsing."""
        content = """
        {
            "id": "JSON_MARKER",
            "level": 1,
            "description": "Ein JSON-Marker",
            "category": "json",
            "examples": ["JSON-Beispiel 1", "JSON-Beispiel 2"]
        }
        """
        
        result = self.manager.parse_marker_content(content, "test_marker.json")
        
        self.assertEqual(result['id'], 'JSON_MARKER')
        self.assertEqual(result['level'], 1)
        self.assertEqual(result['description'], 'Ein JSON-Marker')
        self.assertEqual(result['category'], 'json')
        self.assertEqual(len(result['examples']), 2)
        self.assertEqual(result['format'], 'json')
    
    def test_marker_validation(self):
        """Testet Marker-Validierung."""
        # Gültiger Marker
        valid_marker = {
            'id': 'VALID_MARKER',
            'level': 1,
            'description': 'Ein gültiger Marker'
        }
        
        is_valid, errors = self.manager.validate_marker(valid_marker)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Ungültiger Marker
        invalid_marker = {
            'id': '',  # Leere ID
            'level': 15,  # Ungültiges Level
            'description': 123  # Falscher Typ
        }
        
        is_valid, errors = self.manager.validate_marker(invalid_marker)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_error_marker_creation(self):
        """Testet Fehler-Marker-Erstellung."""
        content = "ungültiger content"
        result = self.manager.parse_marker_content(content, "invalid.yaml")
        
        self.assertIn('error', result)
        self.assertEqual(result['category'], 'error')
        self.assertIn('raw_content', result)


class TestSearchEngine(unittest.TestCase):
    """Tests für die SearchEngine."""
    
    def setUp(self):
        """Setzt Test-Umgebung auf."""
        self.engine = SearchEngine()
        self.test_markers = [
            {
                'id': 'TEST_MARKER_1',
                'description': 'Ein Test-Marker für die Suche',
                'category': 'test',
                'level': 1,
                'format': 'txt'
            },
            {
                'id': 'PRODUCTION_MARKER',
                'description': 'Ein Produktions-Marker',
                'category': 'production',
                'level': 2,
                'format': 'yaml'
            },
            {
                'id': 'ERROR_MARKER',
                'description': 'Ein fehlerhafter Marker',
                'category': 'error',
                'level': 1,
                'format': 'json',
                'error': 'Syntax-Fehler'
            }
        ]
    
    def test_live_search(self):
        """Testet Live-Suche."""
        # Suche nach "test"
        results = self.engine.live_search('test', self.test_markers)
        self.assertGreater(len(results), 0)
        
        # Prüft ob Score gesetzt ist
        for result in results:
            self.assertIn('_search_score', result)
            self.assertIn('_matched_fields', result)
        
        # Leere Suche
        results = self.engine.live_search('', self.test_markers)
        self.assertEqual(len(results), len(self.test_markers))
    
    def test_fuzzy_matching(self):
        """Testet Fuzzy-Matching."""
        matcher = FuzzyMatcher()
        
        # Exakte Übereinstimmung
        self.assertTrue(matcher.fuzzy_match('test', 'test marker'))
        
        # Ähnliche Wörter
        self.assertTrue(matcher.fuzzy_match('tst', 'test marker'))
        
        # Keine Übereinstimmung
        self.assertFalse(matcher.fuzzy_match('xyz', 'test marker'))
    
    def test_filter_application(self):
        """Testet Filter-Anwendung."""
        # Kategorie-Filter
        filters = {'category': 'test'}
        filtered = self.engine.apply_filters(self.test_markers, filters)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['category'], 'test')
        
        # Format-Filter
        filters = {'format': 'yaml'}
        filtered = self.engine.apply_filters(self.test_markers, filters)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['format'], 'yaml')
        
        # Level-Filter
        filters = {'level': 1}
        filtered = self.engine.apply_filters(self.test_markers, filters)
        self.assertEqual(len(filtered), 2)  # 2 Marker mit Level 1
        
        # Fehler-Filter
        filters = {'error_only': True}
        filtered = self.engine.apply_filters(self.test_markers, filters)
        self.assertEqual(len(filtered), 1)
        self.assertIn('error', filtered[0])
    
    def test_search_statistics(self):
        """Testet Such-Statistiken."""
        stats = self.engine.get_search_statistics(self.test_markers)
        
        self.assertEqual(stats['total_markers'], 3)
        self.assertEqual(stats['valid_markers'], 2)
        self.assertEqual(stats['error_markers'], 1)
        self.assertIn('test', stats['categories'])
        self.assertIn('production', stats['categories'])
        self.assertIn('error', stats['categories'])
    
    def test_search_suggestions(self):
        """Testet Suchvorschläge."""
        suggestions = self.engine.get_search_suggestions('test', self.test_markers)
        self.assertGreater(len(suggestions), 0)
        self.assertIn('TEST_MARKER_1', suggestions)
    
    def test_performance_info(self):
        """Testet Performance-Informationen."""
        info = self.engine.get_performance_info()
        
        self.assertIn('cache_size', info)
        self.assertIn('cache_timeout', info)
        self.assertIn('fuzzy_threshold', info)


class TestFilterManager(unittest.TestCase):
    """Tests für den FilterManager."""
    
    def setUp(self):
        """Setzt Test-Umgebung auf."""
        self.filter_manager = FilterManager()
    
    def test_filter_management(self):
        """Testet Filter-Verwaltung."""
        # Filter hinzufügen
        self.filter_manager.add_filter('category', 'test')
        self.filter_manager.add_filter('level', 1)
        
        active_filters = self.filter_manager.get_active_filters()
        self.assertEqual(active_filters['category'], 'test')
        self.assertEqual(active_filters['level'], 1)
        
        # Filter entfernen
        self.filter_manager.remove_filter('category')
        active_filters = self.filter_manager.get_active_filters()
        self.assertNotIn('category', active_filters)
        self.assertIn('level', active_filters)
        
        # Alle Filter löschen
        self.filter_manager.clear_all_filters()
        active_filters = self.filter_manager.get_active_filters()
        self.assertEqual(len(active_filters), 0)
    
    def test_filter_summary(self):
        """Testet Filter-Zusammenfassung."""
        self.assertEqual(self.filter_manager.get_filter_summary(), "Keine Filter aktiv")
        
        self.filter_manager.add_filter('category', 'test')
        self.filter_manager.add_filter('level', 1)
        
        summary = self.filter_manager.get_filter_summary()
        self.assertIn('category: test', summary)
        self.assertIn('level: 1', summary)


class TestIntegration(unittest.TestCase):
    """Integration-Tests."""
    
    def setUp(self):
        """Setzt Test-Umgebung auf."""
        self.manager = MarkerManager()
        self.engine = SearchEngine()
        self.temp_dir = tempfile.mkdtemp()
        
        # Test-Marker erstellen
        self.create_test_markers()
    
    def tearDown(self):
        """Räumt Test-Umgebung auf."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_markers(self):
        """Erstellt Test-Marker-Dateien."""
        # TXT-Marker
        txt_content = """
        TXT_MARKER
        Level: 1
        Beschreibung: Ein TXT-Marker
        Kategorie: txt
        Beispiele:
        - TXT-Beispiel
        """
        
        with open(os.path.join(self.temp_dir, 'txt_marker.txt'), 'w') as f:
            f.write(txt_content)
        
        # YAML-Marker
        yaml_content = """
        id: YAML_MARKER
        level: 2
        description: Ein YAML-Marker
        category: yaml
        examples:
          - YAML-Beispiel
        """
        
        with open(os.path.join(self.temp_dir, 'yaml_marker.yaml'), 'w') as f:
            f.write(yaml_content)
        
        # JSON-Marker
        json_content = """
        {
            "id": "JSON_MARKER",
            "level": 3,
            "description": "Ein JSON-Marker",
            "category": "json",
            "examples": ["JSON-Beispiel"]
        }
        """
        
        with open(os.path.join(self.temp_dir, 'json_marker.json'), 'w') as f:
            f.write(json_content)
    
    def test_full_workflow(self):
        """Testet den vollständigen Workflow."""
        # Marker sammeln
        markers = self.manager.collect_markers_from_directory(self.temp_dir)
        self.assertEqual(len(markers), 3)
        
        # Suche durchführen
        results = self.engine.live_search('marker', markers)
        self.assertEqual(len(results), 3)
        
        # Filter anwenden
        filters = {'category': 'txt'}
        filtered = self.engine.apply_filters(markers, filters)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['category'], 'txt')
        
        # Statistiken generieren
        stats = self.engine.get_search_statistics(markers)
        self.assertEqual(stats['total_markers'], 3)
        self.assertEqual(stats['valid_markers'], 3)
        self.assertEqual(stats['error_markers'], 0)


def run_all_tests():
    """Führt alle Tests aus."""
    print("🧪 Starte Phase 1 Feature Tests...")
    print("=" * 50)
    
    # Test-Suite erstellen
    test_suite = unittest.TestSuite()
    
    # Tests hinzufügen
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMarkerManager))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSearchEngine))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFilterManager))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))
    
    # Tests ausführen
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Ergebnisse ausgeben
    print("=" * 50)
    print(f"📊 Test-Ergebnisse:")
    print(f"  • Tests ausgeführt: {result.testsRun}")
    print(f"  • Fehler: {len(result.failures)}")
    print(f"  • Fehlgeschlagen: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Fehler:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Fehlgeschlagene Tests:")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ Alle Tests erfolgreich!")
        return True
    else:
        print("\n❌ Einige Tests fehlgeschlagen!")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1) 