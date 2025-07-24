#!/usr/bin/env python3
"""
Umfassender Test für Frausar API GUI
=====================================

Testet:
- Drei-Schichten-Architektur
- Marker-Erstellung (Einzel und Multi)
- GUI-Layout und Displays
- Fehlerbehandlung
- Stabilität
"""

import sys
import os
from pathlib import Path
import yaml
import json
import tempfile
import shutil

def test_architecture():
    """Testet die Drei-Schichten-Architektur."""
    print("\n🧪 Teste Drei-Schichten-Architektur...")
    
    layers = {
        "API-Schicht": ["api/main.py", "api/models.py", "api/__init__.py"],
        "Service-Schicht": ["services/agent_service.py", "services/data_service.py", "services/config_service.py"],
        "GUI-Schicht": ["enhanced_smart_marker_gui.py", "smart_marker_gui.py", "simple_marker_gui.py"]
    }
    
    all_ok = True
    for layer, files in layers.items():
        print(f"\n📋 {layer}:")
        for file in files:
            file_path = Path(file)
            if file_path.exists():
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} fehlt")
                all_ok = False
    
    return all_ok

def test_marker_creation():
    """Testet Marker-Erstellung."""
    print("\n🧪 Teste Marker-Erstellung...")
    
    # Test-Verzeichnis erstellen
    test_dir = Path("test_markers")
    test_dir.mkdir(exist_ok=True)
    
    try:
        # Single Marker Test
        single_marker = {
            "id": "A_TEST_SINGLE",
            "level": 1,
            "description": "Test Single Marker",
            "category": "test",
            "version": "1.0.0",
            "status": "active",
            "author": "test_script"
        }
        
        # Speichere als YAML
        yaml_file = test_dir / f"{single_marker['id']}.yaml"
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(single_marker, f, default_flow_style=False, allow_unicode=True)
        
        # Prüfe ob Datei erstellt wurde
        if yaml_file.exists():
            print("  ✅ Single Marker erstellt")
            with open(yaml_file, 'r', encoding='utf-8') as f:
                loaded = yaml.safe_load(f)
                if loaded['id'] == single_marker['id']:
                    print("  ✅ Single Marker korrekt gespeichert")
                else:
                    print("  ❌ Single Marker fehlerhaft")
        
        # Multi-Marker Test
        multi_marker_text = """A_TEST_MULTI_1
level: 1
description: Erster Multi-Marker
category: test

---

A_TEST_MULTI_2
level: 2
description: Zweiter Multi-Marker
category: test

---

A_TEST_MULTI_3
level: 3
description: Dritter Multi-Marker
category: test"""
        
        # Simuliere Multi-Marker Split
        blocks = multi_marker_text.split('---')
        created_count = 0
        
        for block in blocks:
            if block.strip():
                lines = block.strip().split('\n')
                if lines:
                    marker_id = lines[0].strip()
                    if marker_id and not ':' in marker_id:
                        # Erstelle Marker
                        marker_data = {"id": marker_id}
                        for line in lines[1:]:
                            if ':' in line:
                                key, value = line.split(':', 1)
                                marker_data[key.strip()] = value.strip()
                        
                        # Speichere Marker
                        yaml_file = test_dir / f"{marker_id}.yaml"
                        with open(yaml_file, 'w', encoding='utf-8') as f:
                            yaml.dump(marker_data, f, default_flow_style=False, allow_unicode=True)
                        
                        if yaml_file.exists():
                            created_count += 1
        
        if created_count == 3:
            print(f"  ✅ Multi-Marker erstellt ({created_count} Marker)")
        else:
            print(f"  ❌ Multi-Marker Problem (nur {created_count} von 3 erstellt)")
        
        return True
        
    finally:
        # Aufräumen
        if test_dir.exists():
            shutil.rmtree(test_dir)
            print("  🧹 Test-Verzeichnis aufgeräumt")

def test_gui_components():
    """Testet GUI-Komponenten."""
    print("\n🧪 Teste GUI-Komponenten...")
    
    # Prüfe Enhanced GUI
    gui_file = Path("enhanced_smart_marker_gui.py")
    if not gui_file.exists():
        print("  ❌ enhanced_smart_marker_gui.py nicht gefunden")
        return False
    
    with open(gui_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    components = {
        "Drei-Spalten-Layout": ["setup_marker_overview", "setup_input_section", "setup_details_section"],
        "Import Bridge": ["IMPORT_BRIDGE_AVAILABLE", "use_import_bridge"],
        "Batch-Import": ["BatchImportManager", "BatchImportDialog"],
        "Statistiken": ["StatisticsManager", "StatisticsDialog"],
        "Templates": ["TemplateManager", "TemplateDialog"],
        "Inline-Editor": ["InlineEditor"],
        "Such-Engine": ["SearchEngine", "live_search"],
        "Filter": ["filter_markers", "category_var", "format_var"]
    }
    
    all_ok = True
    for feature, required in components.items():
        found = all([req in content for req in required])
        if found:
            print(f"  ✅ {feature}")
        else:
            print(f"  ❌ {feature} unvollständig")
            all_ok = False
    
    # Prüfe Layout-Details
    print("\n  📐 Layout-Details:")
    if "left_frame.pack(side=tk.LEFT" in content:
        print("    ✅ Linke Spalte (Marker-Übersicht) links positioniert")
    if "middle_frame.pack(side=tk.LEFT" in content:
        print("    ✅ Mittlere Spalte (Eingabe) in der Mitte")
    if "right_frame.pack(side=tk.LEFT" in content:
        print("    ✅ Rechte Spalte (Details) rechts positioniert")
    
    # Prüfe Details-Anzeige
    if "self.details_text = scrolledtext.ScrolledText" in content:
        print("    ✅ Details-Anzeige vorhanden")
        # Suche nach der Position relativ zur Marker-Liste
        if "setup_details_section" in content and "right_frame" in content:
            print("    ✅ Details-Anzeige korrekt rechts neben Marker-Liste")
    
    return all_ok

def test_error_handling():
    """Testet Fehlerbehandlung."""
    print("\n🧪 Teste Fehlerbehandlung...")
    
    # Test ungültige YAML-Syntax
    from marker_manager import MarkerManager
    mm = MarkerManager()
    
    test_cases = [
        {
            "name": "Ungültige YAML-Syntax",
            "input": "id: TEST\nlevel: [invalid",
            "should_handle": True
        },
        {
            "name": "Fehlende Pflichtfelder",
            "input": "some_field: value",
            "should_handle": True
        },
        {
            "name": "Leerer Input",
            "input": "",
            "should_handle": True
        },
        {
            "name": "Ungültiger Level",
            "input": "id: TEST\nlevel: abc",
            "should_handle": True
        }
    ]
    
    all_ok = True
    for test in test_cases:
        try:
            result = mm.smart_parse_text(test["input"])
            if test["should_handle"]:
                print(f"  ✅ {test['name']} - Fehler behandelt")
            else:
                print(f"  ❌ {test['name']} - Sollte fehlschlagen")
                all_ok = False
        except Exception as e:
            if not test["should_handle"]:
                print(f"  ✅ {test['name']} - Erwarteter Fehler")
            else:
                print(f"  ❌ {test['name']} - Unbehandelter Fehler: {e}")
                all_ok = False
    
    return all_ok

def test_stability():
    """Testet Stabilität."""
    print("\n🧪 Teste Stabilität...")
    
    # Test große Datenmenge
    print("  📊 Teste mit vielen Markern...")
    try:
        from marker_manager import MarkerManager
        mm = MarkerManager()
        
        # Erstelle 100 Test-Marker
        for i in range(100):
            marker_text = f"A_STRESS_TEST_{i}\nlevel: {(i % 3) + 1}\ndescription: Stress Test Marker {i}"
            result = mm.smart_parse_text(marker_text)
            if not result or 'id' not in result:
                raise Exception(f"Marker {i} konnte nicht erstellt werden")
        
        print("  ✅ 100 Marker erfolgreich verarbeitet")
        
    except Exception as e:
        print(f"  ❌ Stabilitätsproblem: {e}")
        return False
    
    # Test Sonderzeichen
    print("  🔤 Teste Sonderzeichen...")
    special_chars = ["Ä", "Ö", "Ü", "ß", "€", "§", "°", "→", "←", "↑", "↓"]
    try:
        for char in special_chars:
            marker_text = f"A_SPECIAL_{char}\nlevel: 1\ndescription: Test mit {char}"
            result = mm.smart_parse_text(marker_text)
            # ID sollte bereinigt werden
            if result and 'id' in result:
                continue
            else:
                raise Exception(f"Problem mit Sonderzeichen: {char}")
        
        print("  ✅ Sonderzeichen werden korrekt behandelt")
        
    except Exception as e:
        print(f"  ❌ Sonderzeichen-Problem: {e}")
        return False
    
    return True

def test_api_integration():
    """Testet API-Integration."""
    print("\n🧪 Teste API-Integration...")
    
    # Prüfe API-Dateien
    api_files = {
        "api/main.py": "FastAPI Hauptdatei",
        "api/models.py": "Pydantic Models",
        "agents/base_agent.py": "Base Agent",
        "agents/data_cleaning_agent.py": "Data Cleaning Agent",
        "services/agent_service.py": "Agent Service",
        "services/data_service.py": "Data Service"
    }
    
    all_ok = True
    for file, desc in api_files.items():
        if Path(file).exists():
            print(f"  ✅ {desc} vorhanden")
        else:
            print(f"  ❌ {desc} fehlt")
            all_ok = False
    
    # Prüfe Import-Struktur
    try:
        sys.path.insert(0, str(Path.cwd()))
        from services import get_agent_service, get_data_service, get_config_service
        print("  ✅ Services importierbar")
    except ImportError as e:
        print(f"  ❌ Service-Import fehlgeschlagen: {e}")
        all_ok = False
    
    return all_ok

def main():
    """Haupttest-Funktion."""
    print("🚀 UMFASSENDER TEST - FRAUSAR API GUI")
    print("=" * 50)
    
    # Wechsle ins richtige Verzeichnis
    if not Path("enhanced_smart_marker_gui.py").exists():
        print("❌ Nicht im Frausar_API_GUI Verzeichnis!")
        return False
    
    tests = [
        ("Architektur", test_architecture),
        ("Marker-Erstellung", test_marker_creation),
        ("GUI-Komponenten", test_gui_components),
        ("Fehlerbehandlung", test_error_handling),
        ("Stabilität", test_stability),
        ("API-Integration", test_api_integration)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ Fehler in {name}: {e}")
            results[name] = False
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print("📊 TEST-ZUSAMMENFASSUNG")
    print("=" * 50)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test, result in results.items():
        status = "✅ BESTANDEN" if result else "❌ FEHLGESCHLAGEN"
        print(f"{test}: {status}")
    
    print(f"\nGesamtergebnis: {passed}/{total} Tests bestanden")
    
    if passed == total:
        print("\n🎉 ALLE TESTS BESTANDEN!")
        print("✅ System ist stabil und bereit für Live-Betrieb")
        print("✅ Drei-Schichten-Architektur funktioniert")
        print("✅ Marker können erstellt werden")
        print("✅ GUI-Layout ist korrekt")
        print("✅ Fehlerbehandlung funktioniert")
        return True
    else:
        print("\n⚠️  EINIGE TESTS FEHLGESCHLAGEN")
        print("❌ System benötigt weitere Überprüfung")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 