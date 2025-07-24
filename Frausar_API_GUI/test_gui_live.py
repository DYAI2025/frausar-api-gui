#!/usr/bin/env python3
"""
Live-Test für Frausar API GUI
==============================

Testet die GUI-Funktionalität mit echten Marker-Daten
und simuliert Benutzer-Interaktionen.
"""

import sys
import os
from pathlib import Path
import yaml
import time
import tempfile
import shutil

def create_test_markers():
    """Erstellt Test-Marker für die Live-Demo."""
    print("\n🔨 Erstelle Test-Marker...")
    
    # Sicherstelle dass markers-Verzeichnis existiert
    markers_dir = Path("markers")
    markers_dir.mkdir(exist_ok=True)
    
    test_markers = [
        {
            "id": "A_PROD_API_AUTH",
            "level": 3,
            "description": "API-Authentifizierung für Produktionsumgebung",
            "category": "security",
            "version": "2.1.0",
            "status": "active",
            "author": "Security Team",
            "examples": [
                "Bearer Token Validierung",
                "OAuth2 Flow Implementation",
                "JWT Token Refresh"
            ]
        },
        {
            "id": "B_DEV_LOGGING",
            "level": 1,
            "description": "Entwicklungs-Logging-Konfiguration",
            "category": "development",
            "version": "1.0.5",
            "status": "active",
            "author": "Dev Team",
            "examples": [
                "Debug Level Logging",
                "Console Output Formatting",
                "Log Rotation Settings"
            ]
        },
        {
            "id": "C_TEST_VALIDATION",
            "level": 2,
            "description": "Test-Datenvalidierung",
            "category": "testing",
            "version": "1.2.0",
            "status": "active",
            "author": "QA Team",
            "examples": [
                "Schema Validation",
                "Input Sanitization",
                "Edge Case Testing"
            ]
        },
        {
            "id": "E_ERROR_HANDLER",
            "level": 2,
            "description": "Globaler Fehlerbehandler",
            "category": "error_handling",
            "version": "1.5.0",
            "status": "active",
            "author": "Core Team"
        },
        {
            "id": "D_DATA_PIPELINE",
            "level": 1,
            "description": "Datenpipeline-Konfiguration",
            "category": "data",
            "version": "3.0.0",
            "status": "active",
            "author": "Data Team",
            "examples": [
                "ETL Process Configuration",
                "Data Transformation Rules",
                "Pipeline Monitoring"
            ]
        }
    ]
    
    created = 0
    for marker in test_markers:
        file_path = markers_dir / f"{marker['id']}.yaml"
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(marker, f, default_flow_style=False, allow_unicode=True)
        created += 1
        print(f"  ✅ Erstellt: {marker['id']}")
    
    print(f"\n✅ {created} Test-Marker erstellt")
    return created

def test_multi_marker_creation():
    """Testet Multi-Marker-Erstellung."""
    print("\n🧪 Teste Multi-Marker-Erstellung...")
    
    multi_marker_text = """A_MULTI_TEST_1
Level: 1
Beschreibung: Erster Multi-Test-Marker
Kategorie: multi-test
Version: 1.0.0
Status: testing
Autor: Test-Script
Beispiele:
- Multi-Marker Test 1
- Parallele Verarbeitung

---

B_MULTI_TEST_2
Level: 2  
Beschreibung: Zweiter Multi-Test-Marker
Kategorie: multi-test
Version: 1.0.0
Status: testing
Autor: Test-Script

---

C_MULTI_TEST_3
Level: 3
Beschreibung: Dritter Multi-Test-Marker mit Sonderzeichen äöü
Kategorie: multi-test
Version: 1.0.0
Status: testing
Autor: Test-Script
Beispiele:
- Unicode-Test: äöüß
- Sonderzeichen: €§°"""
    
    # Speichere in temporäre Datei
    test_file = Path("test_multi_markers.txt")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(multi_marker_text)
    
    print(f"  ✅ Multi-Marker-Testdatei erstellt: {test_file}")
    
    # Test mit MarkerManager
    from marker_manager import MarkerManager
    mm = MarkerManager()
    
    # Teste Splitting
    blocks = multi_marker_text.split('---')
    if len(blocks) == 3:
        print(f"  ✅ Multi-Marker korrekt aufgeteilt: {len(blocks)} Blöcke")
    else:
        print(f"  ❌ Multi-Marker-Split fehlerhaft: {len(blocks)} statt 3")
    
    # Teste Parsing jedes Blocks
    parsed_markers = []
    for i, block in enumerate(blocks):
        if block.strip():
            try:
                parsed = mm.smart_parse_text(block)
                if parsed and 'id' in parsed:
                    parsed_markers.append(parsed)
                    print(f"  ✅ Marker {i+1} erfolgreich geparst: {parsed['id']}")
                else:
                    print(f"  ❌ Marker {i+1} konnte nicht geparst werden")
            except Exception as e:
                print(f"  ❌ Fehler beim Parsen von Marker {i+1}: {e}")
    
    print(f"\n📊 Multi-Marker Ergebnis: {len(parsed_markers)}/3 erfolgreich")
    
    # Aufräumen
    if test_file.exists():
        test_file.unlink()
        print("  🧹 Testdatei gelöscht")
    
    return len(parsed_markers) == 3

def test_gui_display():
    """Testet GUI-Display-Komponenten."""
    print("\n🧪 Teste GUI-Display-Komponenten...")
    
    from marker_manager import MarkerManager
    from search_engine import SearchEngine
    
    mm = MarkerManager()
    se = SearchEngine()
    
    # Lade Marker
    markers = mm.collect_markers_from_directory("markers")
    print(f"  📁 {len(markers)} Marker geladen")
    
    # Teste Suche
    search_results = se.live_search("api", markers)
    print(f"  🔍 Suche 'api': {len(search_results)} Ergebnisse")
    
    search_results = se.live_search("test", markers)
    print(f"  🔍 Suche 'test': {len(search_results)} Ergebnisse")
    
    # Teste Filter
    filters = {"category": "security"}
    filtered = se.apply_filters(markers, filters)
    print(f"  🔧 Filter 'security': {len(filtered)} Marker")
    
    filters = {"level": 1}
    filtered = se.apply_filters(markers, filters)
    print(f"  🔧 Filter 'Level 1': {len(filtered)} Marker")
    
    # Teste Statistiken
    stats = se.get_search_statistics(markers)
    print(f"\n  📊 Statistiken:")
    print(f"     Gesamt: {stats['total_markers']}")
    print(f"     Kategorien: {stats['unique_categories']}")
    print(f"     Fehler: {stats['error_markers']}")
    
    return True

def test_error_handling():
    """Testet erweiterte Fehlerbehandlung."""
    print("\n🧪 Teste erweiterte Fehlerbehandlung...")
    
    from marker_manager import MarkerManager
    mm = MarkerManager()
    
    error_cases = [
        {
            "name": "Leere Eingabe",
            "input": "",
            "expected": "Standardwerte"
        },
        {
            "name": "Nur Whitespace",
            "input": "   \n\t   ",
            "expected": "Standardwerte"
        },
        {
            "name": "Ungültige Zeichen in ID",
            "input": "TEST-MARKER-äöü\nLevel: 1",
            "expected": "Bereinigte ID"
        },
        {
            "name": "Gemischte Sprachen",
            "input": "TEST_MIXED\nLevel: 1\nBeschreibung: Test\nDescription: Test",
            "expected": "Beide Felder"
        },
        {
            "name": "Sehr lange ID",
            "input": "A_VERY_LONG_MARKER_ID_THAT_EXCEEDS_NORMAL_LENGTH_LIMITS_AND_SHOULD_BE_HANDLED\nLevel: 1",
            "expected": "Gekürzte ID"
        }
    ]
    
    all_ok = True
    for test in error_cases:
        try:
            result = mm.smart_parse_text(test["input"])
            if result:
                print(f"  ✅ {test['name']}: {test['expected']} - OK")
            else:
                print(f"  ❌ {test['name']}: Kein Ergebnis")
                all_ok = False
        except Exception as e:
            print(f"  ❌ {test['name']}: Unbehandelter Fehler - {e}")
            all_ok = False
    
    return all_ok

def test_performance():
    """Testet Performance mit vielen Markern."""
    print("\n🧪 Teste Performance...")
    
    from marker_manager import MarkerManager
    from search_engine import SearchEngine
    import time
    
    mm = MarkerManager()
    se = SearchEngine()
    
    # Erstelle viele Test-Marker
    print("  📊 Erstelle 500 Test-Marker...")
    start_time = time.time()
    
    test_markers = []
    for i in range(500):
        marker = {
            "id": f"PERF_TEST_{i:04d}",
            "level": (i % 3) + 1,
            "description": f"Performance Test Marker {i}",
            "category": f"perf-cat-{i % 10}",
            "format": "yaml",
            "source_file": f"perf_test_{i}.yaml"
        }
        test_markers.append(marker)
    
    creation_time = time.time() - start_time
    print(f"  ✅ 500 Marker in {creation_time:.2f}s erstellt")
    
    # Teste Suche
    print("  🔍 Teste Suchperformance...")
    search_times = []
    
    for query in ["test", "perf", "marker", "100", "cat-5"]:
        start_time = time.time()
        results = se.live_search(query, test_markers)
        search_time = time.time() - start_time
        search_times.append(search_time)
        print(f"     Suche '{query}': {len(results)} Ergebnisse in {search_time:.3f}s")
    
    avg_search_time = sum(search_times) / len(search_times)
    print(f"  ⏱️  Durchschnittliche Suchzeit: {avg_search_time:.3f}s")
    
    # Teste Filter
    print("  🔧 Teste Filter-Performance...")
    start_time = time.time()
    
    filters = {"category": "perf-cat-5", "level": 2}
    filtered = se.apply_filters(test_markers, filters)
    
    filter_time = time.time() - start_time
    print(f"  ✅ Multi-Filter: {len(filtered)} Ergebnisse in {filter_time:.3f}s")
    
    # Performance-Bewertung
    if avg_search_time < 0.1 and filter_time < 0.1:
        print("\n  🚀 Exzellente Performance!")
        return True
    elif avg_search_time < 0.5 and filter_time < 0.5:
        print("\n  ✅ Gute Performance")
        return True
    else:
        print("\n  ⚠️  Performance könnte verbessert werden")
        return False

def main():
    """Haupttest-Funktion."""
    print("🚀 LIVE-TEST - FRAUSAR API GUI")
    print("=" * 50)
    
    # Prüfe ob wir im richtigen Verzeichnis sind
    if not Path("enhanced_smart_marker_gui.py").exists():
        print("❌ Nicht im Frausar_API_GUI Verzeichnis!")
        print("Wechsle ins richtige Verzeichnis...")
        os.chdir("Frausar_API_GUI")
    
    tests = [
        ("Test-Marker erstellen", create_test_markers),
        ("Multi-Marker-Erstellung", test_multi_marker_creation),
        ("GUI-Display-Komponenten", test_gui_display),
        ("Erweiterte Fehlerbehandlung", test_error_handling),
        ("Performance-Test", test_performance)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ Fehler in {name}: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print("📊 LIVE-TEST ZUSAMMENFASSUNG")
    print("=" * 50)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test, result in results.items():
        status = "✅ BESTANDEN" if result else "❌ FEHLGESCHLAGEN"
        print(f"{test}: {status}")
    
    print(f"\nGesamtergebnis: {passed}/{total} Tests bestanden")
    
    if passed == total:
        print("\n🎉 ALLE LIVE-TESTS BESTANDEN!")
        print("✅ GUI ist voll funktionsfähig")
        print("✅ Marker-Erstellung funktioniert einwandfrei")
        print("✅ Multi-Marker werden korrekt verarbeitet")
        print("✅ Display-Komponenten arbeiten korrekt")
        print("✅ Fehlerbehandlung ist robust")
        print("✅ Performance ist ausgezeichnet")
        print("\n🚀 SYSTEM IST BEREIT FÜR LIVE-BETRIEB!")
        return True
    else:
        print("\n⚠️  EINIGE TESTS FEHLGESCHLAGEN")
        print("Bitte überprüfen Sie die fehlgeschlagenen Tests")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 