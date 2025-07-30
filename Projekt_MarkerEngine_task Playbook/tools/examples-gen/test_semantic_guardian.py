#!/usr/bin/env python3
"""
Test-Suite für den Semantischen Wächter & Beispiel-Generator
============================================================

Umfassende Tests für alle Komponenten:
- Schema-Validierung (Lean-Deep 3.1)
- Frame-Analyse (Klarheit, Kohärenz, Spezifität)
- Beispiel-Generierung und Qualitätskontrolle
- End-to-End Workflow-Tests
"""

import sys
import json
import yaml
import tempfile
from pathlib import Path
from typing import Dict, Any, List

# Import des Hauptmoduls
from semantic_guardian import (
    SemanticGuardian, ExampleGenerator, MarkerExampleProcessor,
    ValidationResult, MarkerLevel
)

class TestResults:
    """Sammelt und verwaltet Testergebnisse"""
    
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []
    
    def add_result(self, test_name: str, passed: bool, details: str = ""):
        """Fügt ein Testergebnis hinzu"""
        self.tests_run += 1
        if passed:
            self.tests_passed += 1
            print(f"✅ {test_name}")
        else:
            self.tests_failed += 1
            self.failures.append(f"{test_name}: {details}")
            print(f"❌ {test_name}: {details}")
    
    def summary(self):
        """Gibt eine Zusammenfassung aus"""
        print(f"\n{'='*60}")
        print(f"TEST-ZUSAMMENFASSUNG")
        print(f"{'='*60}")
        print(f"Tests durchgeführt: {self.tests_run}")
        print(f"Tests bestanden:    {self.tests_passed}")
        print(f"Tests fehlgeschlagen: {self.tests_failed}")
        
        if self.failures:
            print(f"\n❌ FEHLGESCHLAGENE TESTS:")
            for failure in self.failures:
                print(f"   - {failure}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\nErfolgsquote: {success_rate:.1f}%")
        
        return self.tests_failed == 0


class SemanticGuardianTestSuite:
    """Umfassende Test-Suite für den Semantischen Wächter"""
    
    def __init__(self):
        self.results = TestResults()
        self.guardian = SemanticGuardian()
        self.generator = ExampleGenerator()
        self.processor = MarkerExampleProcessor()
    
    def run_all_tests(self):
        """Führt alle Tests durch"""
        print("🚀 Starte umfassende Test-Suite für Semantischen Wächter")
        print("="*60)
        
        # Schema-Validierung Tests
        self.test_lean_deep_schema_validation()
        
        # Frame-Analyse Tests
        self.test_frame_analysis()
        
        # Beispiel-Generierung Tests
        self.test_example_generation()
        
        # Qualitätskontrolle Tests
        self.test_quality_control()
        
        # End-to-End Tests
        self.test_end_to_end_workflow()
        
        # Echte Marker Tests
        self.test_real_markers()
        
        return self.results.summary()
    
    def test_lean_deep_schema_validation(self):
        """Tests für Lean-Deep 3.1 Schema-Validierung"""
        print("\n📋 Schema-Validierung Tests")
        print("-" * 40)
        
        # Test 1: Gültiger Lean-Deep 3.1 Marker
        valid_marker = {
            "id": "C_RELATIONAL_DESTABILIZATION_LOOP",
            "frame": {
                "signal": ["Nähe/Distanz-Kontraste"],
                "concept": "Bindungsambivalenz",
                "pragmatics": "Destabilisierung",
                "narrative": "loop"
            },
            "composed_of": ["S_AMBIVALENT_ATTACHMENT_SPEECH", "S_SOFT_WITHDRAWAL"],
            "activation": {"rule": "ANY 2 IN 48h"},
            "scoring": {"base": 2.0, "weight": 1.6, "decay": 0.01, "formula": "logistic"},
            "tags": ["beziehung", "ambivalenz", "loop"],
            "examples": [
                "Ich vermisse dich … aber ich brauche Abstand.",
                "Du bist mir wichtig – aber ich weiß nicht, ob ich bereit bin."
            ]
        }
        
        report = self.guardian.validate_marker(valid_marker)
        self.results.add_result(
            "Gültiger Lean-Deep 3.1 Marker",
            report.result == ValidationResult.VALID,
            f"Result: {report.result}, Errors: {report.schema_errors}"
        )
        
        # Test 2: Verbotene Legacy-Felder
        legacy_marker = valid_marker.copy()
        legacy_marker.update({
            "level": 3,
            "marker_name": "TEST",
            "description": "Test description",
            "category": "CLUSTER"
        })
        
        report = self.guardian.validate_marker(legacy_marker)
        self.results.add_result(
            "Legacy-Felder Erkennung",
            report.result == ValidationResult.INVALID_SCHEMA and "Verbotene Legacy-Felder" in str(report.schema_errors),
            f"Sollte Legacy-Felder ablehnen: {report.schema_errors}"
        )
        
        # Test 3: Fehlende Pflichtfelder
        incomplete_marker = {"id": "A_TEST"}  # Fehlt frame
        
        report = self.guardian.validate_marker(incomplete_marker)
        self.results.add_result(
            "Fehlende Pflichtfelder",
            report.result == ValidationResult.INVALID_SCHEMA,
            f"Sollte fehlende Felder erkennen: {report.schema_errors}"
        )
        
        # Test 4: Falsches ID-Präfix
        wrong_prefix_marker = valid_marker.copy()
        wrong_prefix_marker["id"] = "WRONG_PREFIX_TEST"
        
        report = self.guardian.validate_marker(wrong_prefix_marker)
        self.results.add_result(
            "Falsches ID-Präfix",
            report.result == ValidationResult.INVALID_SCHEMA and "Ungültiges ID-Präfix" in str(report.schema_errors),
            f"Sollte falsches Präfix erkennen: {report.schema_errors}"
        )
        
        # Test 5: Struktur-Block Validierung
        no_structure_marker = valid_marker.copy()
        del no_structure_marker["composed_of"]
        
        report = self.guardian.validate_marker(no_structure_marker)
        self.results.add_result(
            "Fehlender Struktur-Block",
            report.result == ValidationResult.INVALID_SCHEMA,
            f"Sollte fehlenden Struktur-Block erkennen: {report.schema_errors}"
        )
        
        # Test 6: Atomic Marker mit pattern
        atomic_marker = {
            "id": "A_SUPPORT_PHRASE",
            "frame": {
                "signal": ["ich bin da", "für dich da"],
                "concept": "Unterstützung",
                "pragmatics": "Bindung",
                "narrative": "offer"
            },
            "pattern": ["ich bin da", "für dich da", "immer da"],
            "examples": ["Ich bin immer für dich da."]
        }
        
        report = self.guardian.validate_marker(atomic_marker)
        self.results.add_result(
            "Gültiger Atomic Marker",
            report.result == ValidationResult.VALID,
            f"Atomic Marker sollte gültig sein: {report.schema_errors}"
        )
    
    def test_frame_analysis(self):
        """Tests für Frame-Analyse (Klarheit, Kohärenz, Spezifität)"""
        print("\n🔍 Frame-Analyse Tests")
        print("-" * 40)
        
        # Test 1: Klarer, kohärenter Frame
        clear_frame = {
            "signal": ["ich bin immer für dich da", "jederzeit erreichbar"],
            "concept": "Verlässlichkeit",
            "pragmatics": "Bindungsstärkung",
            "narrative": "offer"
        }
        
        analysis = self.guardian._analyze_frame(clear_frame, "TEST_CLEAR")
        self.results.add_result(
            "Klarer Frame - Klarheit",
            analysis.is_clear and analysis.clarity_score > 0.7,
            f"Clarity Score: {analysis.clarity_score}, Issues: {analysis.issues}"
        )
        
        # Test 2: Vager, unklarer Frame
        vague_frame = {
            "signal": ["und so weiter", "etc.", "ähnliches"],
            "concept": "Kommunikation",
            "pragmatics": "Wirkung",
            "narrative": "story"
        }
        
        analysis = self.guardian._analyze_frame(vague_frame, "TEST_VAGUE")
        self.results.add_result(
            "Vager Frame - Klarheit niedrig",
            not analysis.is_clear and analysis.clarity_score < 0.5,
            f"Clarity Score: {analysis.clarity_score}, sollte niedrig sein"
        )
        
        # Test 3: Inkohärenter Frame (Signal vs Concept Mismatch)
        incoherent_frame = {
            "signal": ["ich hasse dich", "verschwinde"],
            "concept": "Unterstützung",
            "pragmatics": "Bindungsstärkung",
            "narrative": "offer"
        }
        
        analysis = self.guardian._analyze_frame(incoherent_frame, "TEST_INCOHERENT")
        self.results.add_result(
            "Inkohärenter Frame",
            not analysis.is_coherent and analysis.coherence_score < 0.7,
            f"Coherence Score: {analysis.coherence_score}, sollte niedrig sein"
        )
        
        # Test 4: Zu generischer Frame
        generic_frame = {
            "signal": ["text", "nachricht"],
            "concept": "Kommunikation",
            "pragmatics": "Wirkung",
            "narrative": "story"
        }
        
        analysis = self.guardian._analyze_frame(generic_frame, "TEST_GENERIC")
        self.results.add_result(
            "Generischer Frame - niedrige Spezifität",
            analysis.specificity_score < 0.5,
            f"Specificity Score: {analysis.specificity_score}, sollte niedrig sein"
        )
        
        # Test 5: Narrative-Pragmatic Konflikt
        conflict_frame = {
            "signal": ["ich ziehe mich zurück"],
            "concept": "Rückzug", 
            "pragmatics": "Engagement",  # Konflikt!
            "narrative": "withdrawal"
        }
        
        analysis = self.guardian._analyze_frame(conflict_frame, "TEST_CONFLICT")
        self.results.add_result(
            "Narrativ-Pragmatik Konflikt",
            "Konflikt" in str(analysis.issues),
            f"Sollte Konflikt erkennen, Issues: {analysis.issues}"
        )
    
    def test_example_generation(self):
        """Tests für Beispiel-Generierung"""
        print("\n🎯 Beispiel-Generierung Tests")
        print("-" * 40)
        
        # Test 1: Erfolgreiche Generierung für gültigen Marker
        valid_marker = {
            "id": "S_SUPPORT_PHRASES",
            "frame": {
                "signal": ["ich bin für dich da", "ruf mich an"],
                "concept": "Unterstützung",
                "pragmatics": "Bindungsstärkung", 
                "narrative": "offer"
            },
            "composed_of": ["A_SUPPORT_OFFER"],
            "examples": []
        }
        
        examples, warnings = self.generator.generate_examples(valid_marker, 3)
        self.results.add_result(
            "Beispiel-Generierung erfolgreich",
            len(examples) > 0,
            f"Generierte {len(examples)} Beispiele, Warnings: {warnings}"
        )
        
        # Test 2: Verschiedene Generierungsstrategien
        if examples:
            # Prüfe Variabilität
            unique_examples = set(examples)
            self.results.add_result(
                "Beispiel-Variabilität",
                len(unique_examples) == len(examples),
                f"Alle Beispiele sollten einzigartig sein: {len(unique_examples)}/{len(examples)}"
            )
        
        # Test 3: Qualitätsbewertung
        test_examples = [
            "Ich bin immer für dich da.",  # Gut
            "x",  # Zu kurz
            "Lorem ipsum dolor sit amet " * 20,  # Zu lang
            "Ich hasse dich total."  # Inhaltlich inkohärent
        ]
        
        quality_results = []
        for example in test_examples:
            is_quality = self.generator._evaluate_example_quality(
                example, valid_marker["frame"], "TEST"
            )
            quality_results.append(is_quality)
        
        expected = [True, False, False, False]
        self.results.add_result(
            "Qualitätsbewertung",
            quality_results == expected,
            f"Qualitätsbewertung: {quality_results}, erwartet: {expected}"
        )
        
        # Test 4: Loop-Narrativ spezifische Generierung
        loop_marker = {
            "id": "C_DESTABILIZATION_LOOP",
            "frame": {
                "signal": ["ich will dich", "ich brauche Abstand"],
                "concept": "Ambivalenz",
                "pragmatics": "Destabilisierung",
                "narrative": "loop"
            },
            "composed_of": ["S_AMBIVALENT_SPEECH"]
        }
        
        loop_examples, _ = self.generator.generate_examples(loop_marker, 2)
        self.results.add_result(
            "Loop-Narrativ Generierung",
            len(loop_examples) > 0,
            f"Loop-Beispiele generiert: {len(loop_examples)}"
        )
    
    def test_quality_control(self):
        """Tests für Qualitätskontrolle"""
        print("\n🔬 Qualitätskontrolle Tests")
        print("-" * 40)
        
        test_frame = {
            "signal": ["ich bin da", "für dich da"],
            "concept": "Unterstützung",
            "pragmatics": "Bindung",
            "narrative": "offer"
        }
        
        # Test verschiedene Beispiel-Qualitäten
        test_cases = [
            ("Ich bin immer für dich da, wenn du Hilfe brauchst.", True, "Gutes Beispiel"),
            ("Hi.", False, "Zu kurz"),
            ("X" * 250, False, "Zu lang"),
            ("", False, "Leer"),
            ("Ich bin total müde und esse gerne Pizza.", False, "Irrelevant"),
            ("Du bist mir egal und ich mag dich nicht.", False, "Semantisch inkohärent"),
            ("Ich bin da! Ruf mich an, wenn du Unterstützung brauchst.", True, "Relevant und kohärent")
        ]
        
        passed_tests = 0
        for example, expected, description in test_cases:
            result = self.generator._evaluate_example_quality(example, test_frame, "TEST")
            if result == expected:
                passed_tests += 1
            else:
                print(f"  ⚠️  {description}: erwartet {expected}, erhalten {result}")
        
        self.results.add_result(
            "Qualitätskontrolle umfassend",
            passed_tests == len(test_cases),
            f"{passed_tests}/{len(test_cases)} Qualitätstests bestanden"
        )
    
    def test_end_to_end_workflow(self):
        """Tests für den kompletten End-to-End Workflow"""
        print("\n🔄 End-to-End Workflow Tests")
        print("-" * 40)
        
        # Test 1: Kompletter Workflow mit gültigem Marker
        valid_marker = {
            "id": "C_POSITIVE_MINDSET",
            "frame": {
                "signal": ["das schaffen wir", "läuft super", "bin optimistisch"],
                "concept": "Optimismus",
                "pragmatics": "Motivation",
                "narrative": "encouragement"
            },
            "composed_of": ["S_POSITIVE_ATTITUDE", "S_ENCOURAGEMENT"],
            "activation": {"rule": "ANY 2 IN 5 messages"},
            "examples": ["Das wird schon klappen!"]
        }
        
        result = self.processor.generate_examples_for_marker(valid_marker, 3)
        self.results.add_result(
            "End-to-End gültiger Marker",
            result["success"] and len(result["new_examples"]) > 0,
            f"Success: {result['success']}, Examples: {len(result.get('new_examples', []))}"
        )
        
        # Test 2: Workflow mit ungültigem Marker
        invalid_marker = {
            "id": "INVALID_NO_PREFIX",
            "frame": {
                "signal": [],  # Leer
                "concept": "",  # Leer
                "pragmatics": "",  # Leer
                "narrative": ""  # Leer
            }
        }
        
        result = self.processor.generate_examples_for_marker(invalid_marker, 3)
        self.results.add_result(
            "End-to-End ungültiger Marker",
            not result["success"] and "GENERIERUNG ABGELEHNT" in result["error"],
            f"Sollte ablehnen: {result.get('error', 'No error')}"
        )
        
        # Test 3: Datei-basierter Workflow
        test_marker_data = {
            "id": "A_TEST_MARKER",
            "frame": {
                "signal": ["test signal", "beispiel"],
                "concept": "Test",
                "pragmatics": "Testen",
                "narrative": "test"
            },
            "pattern": ["test signal", "beispiel"],
            "examples": []
        }
        
        # Temporäre Datei erstellen
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_marker_data, f, default_flow_style=False, allow_unicode=True)
            temp_file = Path(f.name)
        
        try:
            result = self.processor.process_marker_file(temp_file, num_examples=2, backup=False)
            self.results.add_result(
                "Datei-basierter Workflow",
                result["success"],
                f"File processing: {result.get('error', 'Success')}"
            )
        finally:
            # Cleanup
            if temp_file.exists():
                temp_file.unlink()
    
    def test_real_markers(self):
        """Tests mit echten Markern aus dem Projekt"""
        print("\n🎯 Tests mit echten Markern")
        print("-" * 40)
        
        # Suche nach echten Marker-Dateien
        base_path = Path("claude_curser")
        marker_files = []
        
        # Suche in verschiedenen Verzeichnissen
        search_paths = [
            "Codex_MarkerEngine/_v1.1_CODEX_MEWT/ALL_YAML",
            "_ALL_yaml:json_MARKER/marker_yaml_ME/ALL_YAML",
            "ALL_SEMANTIC_MARKER_TXT/ALL_NEWMARKER01/ALL_YAML"
        ]
        
        for search_path in search_paths:
            full_path = base_path / search_path
            if full_path.exists():
                yaml_files = list(full_path.glob("*.yaml"))
                marker_files.extend(yaml_files[:2])  # Maximal 2 pro Pfad
                if len(marker_files) >= 4:  # Maximal 4 Dateien testen
                    break
        
        if not marker_files:
            self.results.add_result(
                "Echte Marker gefunden",
                False,
                "Keine echten Marker-Dateien zum Testen gefunden"
            )
            return
        
        # Teste echte Marker
        successful_validations = 0
        for marker_file in marker_files[:3]:  # Teste maximal 3
            try:
                with open(marker_file, 'r', encoding='utf-8') as f:
                    marker_data = yaml.safe_load(f)
                
                if not isinstance(marker_data, dict):
                    continue
                
                # Validierung
                report = self.guardian.validate_marker(marker_data, str(marker_file.name))
                
                if report.result in [ValidationResult.VALID, ValidationResult.AMBIGUOUS_FRAME]:
                    successful_validations += 1
                
                print(f"  📄 {marker_file.name}: {report.result.value}")
                
            except Exception as e:
                print(f"  ❌ {marker_file.name}: Fehler beim Laden - {e}")
        
        self.results.add_result(
            "Echte Marker Validierung",
            successful_validations > 0,
            f"{successful_validations} von {len(marker_files[:3])} Markern erfolgreich validiert"
        )
    
    def test_counter_semantics(self):
        """
        Spezielle Tests für semantische Gegenprüfung - 
        Überprüft, ob die generierten Beispiele wirklich zur gewünschten Semantik führen
        """
        print("\n🔍 Semantische Gegenprüfung")
        print("-" * 40)
        
        # Test-Marker mit sehr spezifischer Semantik
        specific_marker = {
            "id": "S_CONDITIONAL_SUPPORT",
            "frame": {
                "signal": ["falls du Hilfe brauchst", "wenn du willst"],
                "concept": "Bedingte Unterstützung",
                "pragmatics": "Zurückhaltung",
                "narrative": "conditional_offer"
            },
            "composed_of": ["A_CONDITIONAL_PHRASE"],
            "examples": []
        }
        
        # Generiere Beispiele
        examples, warnings = self.generator.generate_examples(specific_marker, 5)
        
        # Semantische Gegenprüfung
        semantic_matches = 0
        for example in examples:
            example_lower = example.lower()
            
            # Prüfe auf konditionale Strukturen
            conditional_indicators = ["falls", "wenn", "solltest", "möchtest", "brauchst"]
            has_conditional = any(indicator in example_lower for indicator in conditional_indicators)
            
            # Prüfe auf Zurückhaltung (nicht zu direkt)
            direct_phrases = ["sofort", "jetzt", "muss", "musst", "unbedingt"]
            is_not_too_direct = not any(phrase in example_lower for phrase in direct_phrases)
            
            if has_conditional and is_not_too_direct:
                semantic_matches += 1
        
        self.results.add_result(
            "Semantische Gegenprüfung - Konditionalität",
            semantic_matches >= len(examples) * 0.6,  # Mindestens 60% sollten passen
            f"{semantic_matches}/{len(examples)} Beispiele erfüllen die spezifische Semantik"
        )


def main():
    """Hauptfunktion für die Test-Ausführung"""
    print("🔬 SEMANTISCHER WÄCHTER - UMFASSENDE TEST-SUITE")
    print("=" * 60)
    print("Testet die komplette Funktionalität des Example-Generators")
    print("nach Lean-Deep 3.1 Spezifikation\n")
    
    # Test-Suite starten
    test_suite = SemanticGuardianTestSuite()
    
    try:
        success = test_suite.run_all_tests()
        
        # Zusätzliche semantische Gegenprüfung
        test_suite.test_counter_semantics()
        
        # Finale Statistiken
        print(f"\n📊 SYSTEM-STATISTIKEN")
        print("-" * 40)
        stats = test_suite.processor.get_comprehensive_stats()
        
        for category, data in stats.items():
            print(f"{category.upper()}:")
            for key, value in data.items():
                print(f"  {key}: {value}")
        
        if success:
            print(f"\n🎉 ALLE TESTS ERFOLGREICH!")
            print(f"Der Semantische Wächter ist bereit für den Produktiveinsatz.")
            return 0
        else:
            print(f"\n⚠️  EINIGE TESTS FEHLGESCHLAGEN!")
            print(f"Bitte die Fehler überprüfen und beheben.")
            return 1
            
    except Exception as e:
        print(f"\n💥 KRITISCHER FEHLER: {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    exit(main())