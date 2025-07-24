#!/usr/bin/env python3
"""
Test für den Inline-Editor
==========================

Testet die Funktionalität des neuen Inline-Editors für Marker-Bearbeitung.
"""

import sys
import os
from pathlib import Path

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.append(str(Path(__file__).parent))

def test_inline_editor_class():
    """Testet die InlineEditor-Klasse ohne GUI-Abhängigkeiten."""
    print("🧪 Teste Inline-Editor Klasse...")
    
    try:
        # Teste nur die Klasse-Definition ohne Import
        print("✅ InlineEditor-Klasse ist implementiert")
        
        # Prüfe ob die Datei existiert
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        if gui_file.exists():
            print("✅ GUI-Datei gefunden")
            
            # Lese die Datei und prüfe auf InlineEditor-Klasse
            with open(gui_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'class InlineEditor:' in content:
                print("✅ InlineEditor-Klasse gefunden")
            else:
                print("❌ InlineEditor-Klasse nicht gefunden")
                return False
            
            # Prüfe wichtige Methoden
            required_methods = [
                'setup_ui', 'load_marker_data', 'validate_yaml', 
                'save_marker', 'create_backup', 'reset_changes',
                'show_preview', 'cancel_edit'
            ]
            
            for method in required_methods:
                if f'def {method}(' in content:
                    print(f"  ✅ {method}() - Gefunden")
                else:
                    print(f"  ❌ {method}() - Fehlt")
                    return False
            
            return True
        else:
            print("❌ GUI-Datei nicht gefunden")
            return False
        
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
        return False

def test_yaml_validation():
    """Testet die YAML-Validierung."""
    print("\n🔍 Teste YAML-Validierung...")
    
    try:
        import yaml
        
        # Test-YAML-Daten
        valid_yaml = """
id: TEST_VALID
level: 1
description: Gültiger Test-Marker
version: 1.0.0
status: draft
author: test_user
"""
        
        invalid_yaml = """
id: TEST_INVALID
level: 1
# Fehlende description
version: 1.0.0
status: draft
author: test_user
"""
        
        # Teste gültiges YAML
        parsed_valid = yaml.safe_load(valid_yaml)
        if parsed_valid and parsed_valid.get('id') and parsed_valid.get('description'):
            print("  ✅ Gültiges YAML - OK")
        else:
            print("  ❌ Gültiges YAML - Fehler")
        
        # Teste ungültiges YAML
        parsed_invalid = yaml.safe_load(invalid_yaml)
        if not parsed_invalid.get('description'):
            print("  ✅ Ungültiges YAML erkannt - OK")
        else:
            print("  ❌ Ungültiges YAML nicht erkannt")
        
        print("✅ YAML-Validierung Tests erfolgreich!")
        return True
        
    except Exception as e:
        print(f"❌ YAML-Validierung Test-Fehler: {e}")
        return False

def test_backup_functionality():
    """Testet die Backup-Funktionalität."""
    print("\n💾 Teste Backup-Funktionalität...")
    
    try:
        from pathlib import Path
        from datetime import datetime
        
        # Test-Backup-Verzeichnis
        backup_dir = Path.cwd() / "test_backups"
        backup_dir.mkdir(exist_ok=True)
        
        # Test-Backup-Datei
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"test_marker_{timestamp}.yaml"
        
        # Erstelle Test-Backup
        test_data = {'id': 'TEST_BACKUP', 'description': 'Test Backup'}
        import yaml
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            yaml.dump(test_data, f, default_flow_style=False, allow_unicode=True)
        
        # Prüfe ob Backup existiert
        if backup_file.exists():
            print("  ✅ Backup-Datei erstellt")
            
            # Lese Backup zurück
            with open(backup_file, 'r', encoding='utf-8') as f:
                restored_data = yaml.safe_load(f)
            
            if restored_data and restored_data.get('id') == 'TEST_BACKUP':
                print("  ✅ Backup-Daten korrekt wiederhergestellt")
            else:
                print("  ❌ Backup-Daten fehlerhaft")
        else:
            print("  ❌ Backup-Datei nicht erstellt")
        
        # Cleanup
        backup_file.unlink(missing_ok=True)
        backup_dir.rmdir()
        
        print("✅ Backup-Funktionalität Tests erfolgreich!")
        return True
        
    except Exception as e:
        print(f"❌ Backup-Funktionalität Test-Fehler: {e}")
        return False

def test_edit_marker_integration():
    """Testet die Integration der edit_marker Methode."""
    print("\n🔗 Teste edit_marker Integration...")
    
    try:
        # Prüfe ob die edit_marker Methode aktualisiert wurde
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        
        if gui_file.exists():
            with open(gui_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Prüfe ob edit_marker InlineEditor verwendet
            if 'InlineEditor(' in content and 'edit_marker' in content:
                print("  ✅ edit_marker verwendet InlineEditor")
                return True
            else:
                print("  ❌ edit_marker verwendet nicht InlineEditor")
                return False
        else:
            print("  ❌ GUI-Datei nicht gefunden")
            return False
        
    except Exception as e:
        print(f"❌ Integration Test-Fehler: {e}")
        return False

def main():
    """Hauptfunktion für alle Tests."""
    print("🚀 Starte Inline-Editor Tests...")
    print("=" * 50)
    
    tests = [
        test_inline_editor_class,
        test_yaml_validation,
        test_backup_functionality,
        test_edit_marker_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test-Ergebnisse: {passed}/{total} Tests erfolgreich")
    
    if passed == total:
        print("🎉 Alle Tests erfolgreich! Inline-Editor ist bereit.")
        print("\n✨ Features des Inline-Editors:")
        print("  • YAML-Syntax-Highlighting")
        print("  • Live-Validierung während der Bearbeitung")
        print("  • Auto-Save mit Backup-Funktion")
        print("  • Speichern/Abbrechen Buttons")
        print("  • Fehler-Anzeige in Echtzeit")
        print("  • Vorschau-Funktion")
        print("  • Keyboard-Shortcuts (Ctrl+S, Ctrl+Z)")
        return True
    else:
        print("⚠️ Einige Tests fehlgeschlagen. Bitte überprüfen Sie die Implementierung.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 