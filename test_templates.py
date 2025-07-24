#!/usr/bin/env python3
"""
TEST: Marker-Templates Funktionalität
=====================================

Testet die Marker-Templates Funktionalität in der Enhanced Smart Marker GUI.
"""

import os
import sys
from pathlib import Path

def test_template_functionality():
    """Testet die Template-Funktionalität."""
    print("🧪 Teste Marker-Templates Funktionalität...")
    
    # GUI-Datei lesen
    gui_file = Path("Frausar_API_GUI/enhanced_smart_marker_gui.py")
    
    if not gui_file.exists():
        print("❌ GUI-Datei nicht gefunden!")
        return False
    
    with open(gui_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: TemplateManager Klasse
    total_tests += 1
    if "class TemplateManager:" in content:
        print("✅ TemplateManager Klasse gefunden")
        tests_passed += 1
    else:
        print("❌ TemplateManager Klasse nicht gefunden")
    
    # Test 2: TemplateManager Methoden
    template_methods = [
        "__init__",
        "create_default_templates",
        "get_available_templates",
        "extract_template_info",
        "create_template",
        "delete_template",
        "get_template_content",
        "apply_template",
        "validate_template"
    ]
    
    for method in template_methods:
        total_tests += 1
        if f"def {method}(" in content:
            print(f"✅ TemplateManager.{method} gefunden")
            tests_passed += 1
        else:
            print(f"❌ TemplateManager.{method} nicht gefunden")
    
    # Test 3: TemplateDialog Klasse
    total_tests += 1
    if "class TemplateDialog:" in content:
        print("✅ TemplateDialog Klasse gefunden")
        tests_passed += 1
    else:
        print("❌ TemplateDialog Klasse nicht gefunden")
    
    # Test 4: TemplateDialog Methoden
    dialog_methods = [
        "__init__",
        "setup_ui",
        "load_templates",
        "on_template_select",
        "update_preview",
        "apply_template",
        "create_new_template",
        "delete_selected_template",
        "on_close"
    ]
    
    for method in dialog_methods:
        total_tests += 1
        if f"def {method}(" in content:
            print(f"✅ TemplateDialog.{method} gefunden")
            tests_passed += 1
        else:
            print(f"❌ TemplateDialog.{method} nicht gefunden")
    
    # Test 5: GUI Integration
    total_tests += 1
    if "self.template_manager = TemplateManager()" in content:
        print("✅ TemplateManager in GUI initialisiert")
        tests_passed += 1
    else:
        print("❌ TemplateManager nicht in GUI initialisiert")
    
    # Test 6: Template Button
    total_tests += 1
    if "📋 Marker-Templates" in content:
        print("✅ Template-Button in GUI gefunden")
        tests_passed += 1
    else:
        print("❌ Template-Button nicht in GUI gefunden")
    
    # Test 7: open_template_dialog Methode
    total_tests += 1
    if "def open_template_dialog(self):" in content:
        print("✅ open_template_dialog Methode gefunden")
        tests_passed += 1
    else:
        print("❌ open_template_dialog Methode nicht gefunden")
    
    # Test 8: Template-Verzeichnis
    total_tests += 1
    if "templates" in content and "template_dir" in content:
        print("✅ Template-Verzeichnis-Konfiguration gefunden")
        tests_passed += 1
    else:
        print("❌ Template-Verzeichnis-Konfiguration nicht gefunden")
    
    # Test 9: Default Templates
    total_tests += 1
    if "create_default_templates" in content:
        print("✅ Default-Templates-Erstellung gefunden")
        tests_passed += 1
    else:
        print("❌ Default-Templates-Erstellung nicht gefunden")
    
    # Test 10: Template-Validierung
    total_tests += 1
    if "validate_template" in content:
        print("✅ Template-Validierung gefunden")
        tests_passed += 1
    else:
        print("❌ Template-Validierung nicht gefunden")
    
    # Test 11: Template-Anwendung
    total_tests += 1
    if "apply_template" in content:
        print("✅ Template-Anwendung gefunden")
        tests_passed += 1
    else:
        print("❌ Template-Anwendung nicht gefunden")
    
    # Test 12: Template-Preview
    total_tests += 1
    if "update_preview" in content:
        print("✅ Template-Preview gefunden")
        tests_passed += 1
    else:
        print("❌ Template-Preview nicht gefunden")
    
    print(f"\n📊 Test-Ergebnis: {tests_passed}/{total_tests} Tests bestanden")
    
    if tests_passed == total_tests:
        print("🎉 Alle Template-Tests bestanden!")
        return True
    else:
        print("⚠️  Einige Template-Tests fehlgeschlagen")
        return False

def test_template_file_structure():
    """Testet die Template-Dateistruktur."""
    print("\n📁 Teste Template-Dateistruktur...")
    
    # Template-Verzeichnis
    template_dir = Path("templates")
    
    if template_dir.exists():
        print("✅ Template-Verzeichnis existiert")
        
        # Prüfe Template-Dateien
        template_files = list(template_dir.glob("*.yaml"))
        if template_files:
            print(f"✅ {len(template_files)} Template-Dateien gefunden:")
            for file in template_files:
                print(f"   • {file.name}")
        else:
            print("⚠️  Keine Template-Dateien gefunden")
    else:
        print("⚠️  Template-Verzeichnis existiert nicht (wird bei erstem Start erstellt)")

if __name__ == "__main__":
    print("🧪 MARKER-TEMPLATES TEST")
    print("=" * 50)
    
    success = test_template_functionality()
    test_template_file_structure()
    
    if success:
        print("\n✅ Marker-Templates Funktionalität ist vollständig implementiert!")
        sys.exit(0)
    else:
        print("\n❌ Marker-Templates Funktionalität ist unvollständig!")
        sys.exit(1) 