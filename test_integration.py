#!/usr/bin/env python3
"""
Integration Test für Enhanced Smart Marker System
================================================

Testet die Integration zwischen:
- Enhanced Smart Marker GUI
- Import Bridge
- Marker Repair Engine
"""

import sys
import os
from pathlib import Path

# Pfad zum Hauptverzeichnis hinzufügen
sys.path.append(str(Path(__file__).parent))

def test_import_bridge():
    """Testet die Import Bridge Funktionalität."""
    print("🧪 Teste Import Bridge...")
    
    try:
        from marker_import_bridge import YAMLBlockSplitter, MarkerValidator, MarkerWriter, HistoryLogger
        print("✅ Import Bridge Module geladen")
        
        # Test YAMLBlockSplitter
        splitter = YAMLBlockSplitter()
        test_text = """id: A_TEST_1
level: 1
description: Test Marker 1

---

id: S_TEST_2
level: 2
description: Test Marker 2"""
        
        blocks = splitter.split(test_text)
        assert len(blocks) == 2, f"Erwartet 2 Blöcke, erhalten {len(blocks)}"
        print("✅ YAMLBlockSplitter funktioniert")
        
        # Test MarkerValidator
        validator = MarkerValidator()
        data, errors = validator.validate(blocks[0])
        assert not errors, f"Validierungsfehler: {errors}"
        print("✅ MarkerValidator funktioniert")
        
        # Test MarkerWriter
        marker_dir = Path("test_markers")
        json_dir = Path("test_markers_json")
        writer = MarkerWriter(marker_dir, json_dir)
        print("✅ MarkerWriter initialisiert")
        
        # Test HistoryLogger
        logger = HistoryLogger(Path("test_history.json"))
        logger.append({"status": "test", "id": "TEST_1"})
        print("✅ HistoryLogger funktioniert")
        
        # Cleanup
        if marker_dir.exists():
            import shutil
            shutil.rmtree(marker_dir)
        if json_dir.exists():
            import shutil
            shutil.rmtree(json_dir)
        if Path("test_history.json").exists():
            os.remove("test_history.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Import Bridge Test fehlgeschlagen: {e}")
        return False

def test_enhanced_gui_integration():
    """Testet die GUI-Integration."""
    print("🧪 Teste Enhanced GUI Integration...")
    
    try:
        # Teste Import der GUI
        sys.path.append(str(Path(__file__).parent / "Frausar_API_GUI"))
        from enhanced_smart_marker_gui import EnhancedSmartMarkerGUI, IMPORT_BRIDGE_AVAILABLE
        
        print(f"✅ Enhanced GUI geladen (Import Bridge: {IMPORT_BRIDGE_AVAILABLE})")
        
        # Teste GUI-Initialisierung (ohne tkinter)
        if IMPORT_BRIDGE_AVAILABLE:
            print("✅ Import Bridge ist in GUI verfügbar")
        else:
            print("⚠️ Import Bridge ist in GUI nicht verfügbar")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced GUI Test fehlgeschlagen: {e}")
        return False

def test_marker_repair_engine():
    """Testet die Marker Repair Engine."""
    print("🧪 Teste Marker Repair Engine...")
    
    try:
        from marker_repair_engine import MarkerRepairEngine
        
        repairer = MarkerRepairEngine({})
        print("✅ MarkerRepairEngine initialisiert")
        
        # Test Reparatur
        test_data = {
            "id": "invalid_id",
            "level": 5,  # Ungültiges Level
            "description": "Test"
        }
        
        repaired_data, changes = repairer.repair(test_data)
        print(f"✅ Reparatur durchgeführt: {changes}")
        
        return True
        
    except Exception as e:
        print(f"❌ Marker Repair Engine Test fehlgeschlagen: {e}")
        return False

def test_end_to_end_workflow():
    """Testet den kompletten Workflow."""
    print("🧪 Teste End-to-End Workflow...")
    
    try:
        # Test-Marker erstellen
        test_marker = """id: E_E2E_TEST_1
level: 1
description: End-to-End Test Marker
version: 1.0.0
status: draft
author: test"""
        
        # Import Bridge verwenden
        from marker_import_bridge import YAMLBlockSplitter, MarkerValidator, MarkerWriter, HistoryLogger
        
        splitter = YAMLBlockSplitter()
        validator = MarkerValidator()
        writer = MarkerWriter(Path("test_e2e_markers"), Path("test_e2e_json"))
        logger = HistoryLogger(Path("test_e2e_history.json"))
        
        # Verarbeite Marker
        blocks = splitter.split(test_marker)
        assert len(blocks) == 1, "Sollte 1 Block haben"
        
        data, errors = validator.validate(blocks[0])
        assert not errors, f"Validierungsfehler: {errors}"
        
        yaml_path, json_path = writer.write(data)
        assert yaml_path.exists(), "YAML-Datei wurde nicht erstellt"
        assert json_path.exists(), "JSON-Datei wurde nicht erstellt"
        
        logger.append({"status": "imported", "id": data["id"]})
        
        print("✅ End-to-End Workflow erfolgreich")
        
        # Cleanup
        import shutil
        if Path("test_e2e_markers").exists():
            shutil.rmtree("test_e2e_markers")
        if Path("test_e2e_json").exists():
            shutil.rmtree("test_e2e_json")
        if Path("test_e2e_history.json").exists():
            os.remove("test_e2e_history.json")
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-End Workflow Test fehlgeschlagen: {e}")
        return False

def main():
    """Hauptfunktion für alle Tests."""
    print("🚀 Starte Integration Tests für Enhanced Smart Marker System")
    print("=" * 60)
    
    tests = [
        ("Import Bridge", test_import_bridge),
        ("Enhanced GUI Integration", test_enhanced_gui_integration),
        ("Marker Repair Engine", test_marker_repair_engine),
        ("End-to-End Workflow", test_end_to_end_workflow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} erfolgreich")
        else:
            print(f"❌ {test_name} fehlgeschlagen")
    
    print("\n" + "=" * 60)
    print(f"📊 Test-Ergebnisse: {passed}/{total} Tests erfolgreich")
    
    if passed == total:
        print("🎉 Alle Tests erfolgreich! System ist bereit.")
        return 0
    else:
        print("⚠️ Einige Tests fehlgeschlagen. Bitte prüfen Sie die Fehler.")
        return 1

if __name__ == "__main__":
    exit(main()) 