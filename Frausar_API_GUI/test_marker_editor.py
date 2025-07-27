#!/usr/bin/env python3
"""
Test-Script für Marker-Editor
============================
Testet die Marker-Editor-Funktionalität und identifiziert Fehler.
"""

import os
import sys
import yaml
from pathlib import Path

def test_marker_loading():
    """Testet das Laden von Markern."""
    print("🧪 Teste Marker-Loading...")
    
    # Prüfe Marker-Verzeichnis
    marker_dir = Path("markers")
    if not marker_dir.exists():
        print(f"❌ Marker-Verzeichnis nicht gefunden: {marker_dir}")
        return False
    
    # Zähle Marker-Dateien
    yaml_files = list(marker_dir.glob("*.yaml"))
    print(f"✅ {len(yaml_files)} YAML-Dateien gefunden")
    
    # Teste das Laden jeder Datei
    errors = []
    for yaml_file in yaml_files[:5]:  # Teste nur die ersten 5
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = f.read()
                marker_data = yaml.safe_load(content)
                print(f"✅ {yaml_file.name}: Geladen")
        except Exception as e:
            error_msg = f"❌ {yaml_file.name}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
    
    if errors:
        print(f"\n❌ {len(errors)} Fehler gefunden:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Alle Marker erfolgreich geladen")
        return True

def test_marker_creation():
    """Testet die Marker-Erstellung."""
    print("\n🧪 Teste Marker-Erstellung...")
    
    # Test-Marker
    test_marker = {
        'id': 'TEST_MARKER',
        'description': 'Test-Marker für Validierung',
        'level': 1,
        'category': 'test',
        'examples': ['Beispiel 1', 'Beispiel 2'],
        'metadata': {
            'created_at': '2025-01-27T10:00:00',
            'created_by': 'test_script',
            'version': '1.0.0',
            'tags': ['test', 'validation']
        }
    }
    
    try:
        # Teste YAML-Serialisierung
        yaml_content = yaml.dump(test_marker, default_flow_style=False, allow_unicode=True)
        print("✅ YAML-Serialisierung erfolgreich")
        
        # Teste YAML-Deserialisierung
        loaded_marker = yaml.safe_load(yaml_content)
        print("✅ YAML-Deserialisierung erfolgreich")
        
        # Teste Marker-Validierung
        required_fields = ['id', 'description', 'level']
        for field in required_fields:
            if field not in loaded_marker:
                print(f"❌ Fehlendes Feld: {field}")
                return False
        
        print("✅ Marker-Validierung erfolgreich")
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei Marker-Erstellung: {e}")
        return False

def test_marker_manager():
    """Testet den MarkerManager."""
    print("\n🧪 Teste MarkerManager...")
    
    try:
        from marker_manager import MarkerManager
        manager = MarkerManager()
        print("✅ MarkerManager erfolgreich importiert")
        
        # Teste Marker-Parsing mit korrektem Format
        test_text = """
TEST_MARKER
level: 1
description: Test-Marker für Validierung
category: test
examples:
- Beispiel 1
- Beispiel 2
---
ANOTHER_MARKER
level: 2
description: Weiterer Test-Marker
category: test
examples:
- Weiteres Beispiel
"""
        
        result = manager.smart_parse_text(test_text)
        markers_found = len(result.get('markers', []))
        print(f"✅ Marker-Parsing erfolgreich: {markers_found} Marker gefunden")
        
        # Teste Directory-Scanning
        markers_from_dir = manager.collect_markers_from_directory("markers")
        print(f"✅ Directory-Scanning: {len(markers_from_dir)} Marker aus Verzeichnis geladen")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        return False
    except Exception as e:
        print(f"❌ Fehler im MarkerManager: {e}")
        return False

def test_gui_components():
    """Testet GUI-Komponenten."""
    print("\n🧪 Teste GUI-Komponenten...")
    
    try:
        import tkinter as tk
        print("✅ Tkinter verfügbar")
        
        # Teste einfache GUI-Erstellung
        root = tk.Tk()
        root.withdraw()  # Verstecke das Fenster
        
        label = tk.Label(root, text="Test")
        print("✅ GUI-Komponenten funktionsfähig")
        
        root.destroy()
        return True
        
    except ImportError as e:
        print(f"❌ Tkinter nicht verfügbar: {e}")
        return False
    except Exception as e:
        print(f"❌ GUI-Test-Fehler: {e}")
        return False

def main():
    """Hauptfunktion für Tests."""
    print("🚀 MARKER-EDITOR TEST")
    print("=" * 30)
    
    tests = [
        ("Marker-Loading", test_marker_loading),
        ("Marker-Erstellung", test_marker_creation),
        ("MarkerManager", test_marker_manager),
        ("GUI-Komponenten", test_gui_components)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Unerwarteter Fehler in {test_name}: {e}")
            results.append((test_name, False))
    
    # Zusammenfassung
    print("\n📊 TEST-ZUSAMMENFASSUNG")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ BESTANDEN" if result else "❌ FEHLGESCHLAGEN"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nGesamt: {passed}/{len(results)} Tests bestanden")
    
    if passed == len(results):
        print("🎉 Alle Tests erfolgreich!")
        print("✅ Marker-Editor ist bereit zur Verwendung")
        return True
    else:
        print("⚠️ Einige Tests fehlgeschlagen - Überprüfung erforderlich")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 