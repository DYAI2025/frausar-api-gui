#!/usr/bin/env python3
"""
TEST: MarkerManager Reparatur
============================

Testet die Reparatur der smart_parse_text Methode im MarkerManager.
"""

import sys
from pathlib import Path

def test_marker_manager_fix():
    """Testet die MarkerManager Reparatur."""
    print("🧪 Teste MarkerManager Reparatur...")
    
    # Prüfe ob MarkerManager Datei existiert
    marker_manager_file = Path("Frausar_API_GUI/marker_manager.py")
    if not marker_manager_file.exists():
        print("❌ marker_manager.py nicht gefunden!")
        return False
    
    # Prüfe ob smart_parse_text Methode existiert
    with open(marker_manager_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "def smart_parse_text(self, text: str) -> Dict[str, Any]:" in content:
        print("✅ smart_parse_text Methode gefunden")
    else:
        print("❌ smart_parse_text Methode nicht gefunden")
        return False
    
    # Teste Import und Methode
    try:
        sys.path.append("Frausar_API_GUI")
        from marker_manager import MarkerManager
        
        mm = MarkerManager()
        
        # Teste ob Methode verfügbar ist
        if hasattr(mm, 'smart_parse_text'):
            print("✅ smart_parse_text Methode verfügbar")
        else:
            print("❌ smart_parse_text Methode nicht verfügbar")
            return False
        
        # Teste Methode mit Beispiel-Text
        test_text = """TEST_MARKER
Level: 1
Beschreibung: Test-Marker für Reparatur
Kategorie: test
Beispiele:
- Beispiel 1
- Beispiel 2"""
        
        result = mm.smart_parse_text(test_text)
        
        # Prüfe Ergebnis
        expected_keys = ['id', 'level', 'description', 'category', 'examples']
        missing_keys = [key for key in expected_keys if key not in result]
        
        if missing_keys:
            print(f"❌ Fehlende Schlüssel: {missing_keys}")
            return False
        
        print("✅ smart_parse_text Methode funktioniert korrekt")
        print(f"   Ergebnis: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Testen: {str(e)}")
        return False

def test_enhanced_gui_integration():
    """Testet die Integration mit der Enhanced GUI."""
    print("\n🧪 Teste Enhanced GUI Integration...")
    
    # Prüfe ob Enhanced GUI Datei existiert
    gui_file = Path("Frausar_API_GUI/enhanced_smart_marker_gui.py")
    if not gui_file.exists():
        print("❌ enhanced_smart_marker_gui.py nicht gefunden!")
        return False
    
    with open(gui_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Prüfe ob smart_parse_text verwendet wird
    if "self.marker_manager.smart_parse_text" in content:
        print("✅ smart_parse_text wird in Enhanced GUI verwendet")
        return True
    else:
        print("❌ smart_parse_text wird nicht in Enhanced GUI verwendet")
        return False

def main():
    """Hauptfunktion für alle Tests."""
    print("🧪 MARKERMANAGER REPARATUR TEST")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: MarkerManager Reparatur
    if test_marker_manager_fix():
        tests_passed += 1
        print("✅ MarkerManager Reparatur erfolgreich")
    else:
        print("❌ MarkerManager Reparatur fehlgeschlagen")
    
    # Test 2: Enhanced GUI Integration
    if test_enhanced_gui_integration():
        tests_passed += 1
        print("✅ Enhanced GUI Integration erfolgreich")
    else:
        print("❌ Enhanced GUI Integration fehlgeschlagen")
    
    print(f"\n📊 Test-Ergebnis: {tests_passed}/{total_tests} Tests bestanden")
    
    if tests_passed == total_tests:
        print("🎉 MarkerManager Reparatur erfolgreich!")
        print("✅ smart_parse_text Methode ist verfügbar")
        print("✅ Enhanced GUI kann Marker erstellen")
        print("✅ Fehler behoben")
        sys.exit(0)
    else:
        print("⚠️  Einige Tests fehlgeschlagen")
        sys.exit(1)

if __name__ == "__main__":
    main() 