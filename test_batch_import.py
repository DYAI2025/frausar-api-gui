#!/usr/bin/env python3
"""
Test für Batch-Import-Funktionen
================================

Testet die Funktionalität des neuen Batch-Import-Systems.
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.append(str(Path(__file__).parent))

def test_batch_import_classes():
    """Testet die Batch-Import-Klassen ohne GUI-Abhängigkeiten."""
    print("🧪 Teste Batch-Import-Klassen...")
    
    try:
        # Prüfe ob die Datei existiert
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        if not gui_file.exists():
            print(f"❌ GUI-Datei nicht gefunden: {gui_file}")
            return False
        
        print("✅ GUI-Datei gefunden")
        
        # Lese die Datei und prüfe auf Batch-Import-Klassen
        content = gui_file.read_text(encoding='utf-8')
        
        # Prüfe auf BatchImportManager-Klasse
        if "class BatchImportManager:" in content:
            print("✅ BatchImportManager-Klasse gefunden")
        else:
            print("❌ BatchImportManager-Klasse nicht gefunden")
            return False
        
        # Prüfe auf BatchImportDialog-Klasse
        if "class BatchImportDialog:" in content:
            print("✅ BatchImportDialog-Klasse gefunden")
        else:
            print("❌ BatchImportDialog-Klasse nicht gefunden")
            return False
        
        # Prüfe auf wichtige Methoden
        required_methods = [
            'process_batch_files',
            'process_single_file',
            'get_supported_extensions',
            'validate_file_selection',
            'select_files',
            'start_batch_import',
            'show_import_results'
        ]
        
        for method in required_methods:
            if method in content:
                print(f"✅ Methode {method} gefunden")
            else:
                print(f"❌ Methode {method} nicht gefunden")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
        return False

def test_gui_integration():
    """Testet die GUI-Integration."""
    print("🧪 Teste GUI-Integration...")
    
    try:
        # Prüfe ob die Datei existiert
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        if not gui_file.exists():
            print(f"❌ GUI-Datei nicht gefunden: {gui_file}")
            return False
        
        # Lese die Datei und prüfe auf Integration
        content = gui_file.read_text(encoding='utf-8')
        
        # Prüfe auf Batch-Import-Manager in GUI
        if "self.batch_import_manager = BatchImportManager(" in content:
            print("✅ Batch-Import-Manager in GUI integriert")
        else:
            print("❌ Batch-Import-Manager nicht in GUI integriert")
            return False
        
        # Prüfe auf Batch-Import-Button
        if 'text="📦 Batch-Import"' in content:
            print("✅ Batch-Import-Button gefunden")
        else:
            print("❌ Batch-Import-Button nicht gefunden")
            return False
        
        # Prüfe auf open_batch_import Methode
        if "def open_batch_import(self):" in content:
            print("✅ open_batch_import Methode gefunden")
        else:
            print("❌ open_batch_import Methode nicht gefunden")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
        return False

def test_file_structure():
    """Testet die Dateistruktur und Imports."""
    print("🧪 Teste Dateistruktur...")
    
    try:
        # Prüfe notwendige Imports
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        content = gui_file.read_text(encoding='utf-8')
        
        # Prüfe auf notwendige Imports
        required_imports = [
            'import threading',
            'import time',
            'from pathlib import Path',
            'from typing import List, Dict, Any, Optional'
        ]
        
        for import_stmt in required_imports:
            if import_stmt in content:
                print(f"✅ Import {import_stmt} gefunden")
            else:
                print(f"❌ Import {import_stmt} nicht gefunden")
                return False
        
        # Prüfe auf Batch-Import-Features in der Dokumentation
        if "Batch-Import-Funktionen für Massenverarbeitung" in content:
            print("✅ Batch-Import-Dokumentation gefunden")
        else:
            print("❌ Batch-Import-Dokumentation nicht gefunden")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
        return False

def main():
    """Hauptfunktion für alle Tests."""
    print("🚀 Starte Batch-Import Tests...")
    print("=" * 50)
    
    tests = [
        ("Batch-Import-Klassen", test_batch_import_classes),
        ("GUI-Integration", test_gui_integration),
        ("Dateistruktur", test_file_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: ERFOLGREICH")
            else:
                print(f"❌ {test_name}: FEHLGESCHLAGEN")
                
        except Exception as e:
            print(f"❌ {test_name}: FEHLER - {e}")
            results.append((test_name, False))
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print("📊 TEST-ZUSAMMENFASSUNG")
    print("=" * 50)
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ERFOLGREICH" if result else "❌ FEHLGESCHLAGEN"
        print(f"{test_name}: {status}")
    
    print(f"\nGesamt: {successful}/{total} Tests erfolgreich")
    
    if successful == total:
        print("🎉 Alle Batch-Import Tests erfolgreich!")
        return True
    else:
        print("⚠️ Einige Tests fehlgeschlagen")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 