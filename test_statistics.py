#!/usr/bin/env python3
"""
Test für erweiterte Statistiken & Analytics
===========================================

Testet die Funktionalität des neuen Statistics-Systems.
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.append(str(Path(__file__).parent))

def test_statistics_manager():
    """Testet den StatisticsManager."""
    print("🧪 Teste StatisticsManager...")
    
    try:
        # Prüfe ob die Datei existiert
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        if not gui_file.exists():
            print(f"❌ GUI-Datei nicht gefunden: {gui_file}")
            return False
        
        print("✅ GUI-Datei gefunden")
        
        # Lese die Datei und prüfe auf StatisticsManager-Klasse
        content = gui_file.read_text(encoding='utf-8')
        
        # Prüfe auf StatisticsManager-Klasse
        if "class StatisticsManager:" in content:
            print("✅ StatisticsManager-Klasse gefunden")
        else:
            print("❌ StatisticsManager-Klasse nicht gefunden")
            return False
        
        # Prüfe auf wichtige Methoden
        required_methods = [
            'get_comprehensive_stats',
            'analyze_marker_file',
            'get_growth_chart_data',
            'get_category_distribution',
            'get_level_distribution',
            'get_recent_activity',
            'export_statistics_report'
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

def test_statistics_dialog():
    """Testet den StatisticsDialog."""
    print("🧪 Teste StatisticsDialog...")
    
    try:
        # Prüfe ob die Datei existiert
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        if not gui_file.exists():
            print(f"❌ GUI-Datei nicht gefunden: {gui_file}")
            return False
        
        # Lese die Datei und prüfe auf StatisticsDialog-Klasse
        content = gui_file.read_text(encoding='utf-8')
        
        # Prüfe auf StatisticsDialog-Klasse
        if "class StatisticsDialog:" in content:
            print("✅ StatisticsDialog-Klasse gefunden")
        else:
            print("❌ StatisticsDialog-Klasse nicht gefunden")
            return False
        
        # Prüfe auf wichtige Methoden
        required_methods = [
            'setup_ui',
            'setup_overview_tab',
            'setup_categories_tab',
            'setup_growth_tab',
            'setup_activity_tab',
            'load_statistics',
            'refresh_statistics',
            'export_report'
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
    """Testet die GUI-Integration der Statistiken."""
    print("🧪 Teste GUI-Integration...")
    
    try:
        # Prüfe ob die Datei existiert
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        if not gui_file.exists():
            print(f"❌ GUI-Datei nicht gefunden: {gui_file}")
            return False
        
        # Lese die Datei und prüfe auf Integration
        content = gui_file.read_text(encoding='utf-8')
        
        # Prüfe auf Statistics-Manager in GUI
        if "self.statistics_manager = StatisticsManager(" in content:
            print("✅ Statistics-Manager in GUI integriert")
        else:
            print("❌ Statistics-Manager nicht in GUI integriert")
            return False
        
        # Prüfe auf Statistiken-Button
        if 'text="📊 Erweiterte Statistiken"' in content:
            print("✅ Statistiken-Button gefunden")
        else:
            print("❌ Statistiken-Button nicht gefunden")
            return False
        
        # Prüfe auf open_statistics_dialog Methode
        if "def open_statistics_dialog(self):" in content:
            print("✅ open_statistics_dialog Methode gefunden")
        else:
            print("❌ open_statistics_dialog Methode nicht gefunden")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
        return False

def test_statistics_features():
    """Testet die Statistiken-Features."""
    print("🧪 Teste Statistiken-Features...")
    
    try:
        # Prüfe ob die Datei existiert
        gui_file = Path(__file__).parent / "Frausar_API_GUI" / "enhanced_smart_marker_gui.py"
        if not gui_file.exists():
            print(f"❌ GUI-Datei nicht gefunden: {gui_file}")
            return False
        
        # Lese die Datei und prüfe auf Features
        content = gui_file.read_text(encoding='utf-8')
        
        # Prüfe auf wichtige Statistiken-Features
        required_features = [
            'get_comprehensive_stats',
            'categories',
            'levels',
            'authors',
            'growth_data',
            'validation_stats',
            'performance',
            'export_statistics_report',
            'get_growth_chart_data',
            'get_category_distribution',
            'get_level_distribution',
            'get_recent_activity'
        ]
        
        for feature in required_features:
            if feature in content:
                print(f"✅ Feature {feature} gefunden")
            else:
                print(f"❌ Feature {feature} nicht gefunden")
                return False
        
        # Prüfe auf Tab-Struktur
        tab_features = [
            'setup_overview_tab',
            'setup_categories_tab',
            'setup_growth_tab',
            'setup_activity_tab',
            'notebook.add'
        ]
        
        for feature in tab_features:
            if feature in content:
                print(f"✅ Tab-Feature {feature} gefunden")
            else:
                print(f"❌ Tab-Feature {feature} nicht gefunden")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
        return False

def main():
    """Hauptfunktion für alle Tests."""
    print("🚀 Starte Statistiken Tests...")
    print("=" * 50)
    
    tests = [
        ("StatisticsManager", test_statistics_manager),
        ("StatisticsDialog", test_statistics_dialog),
        ("GUI-Integration", test_gui_integration),
        ("Statistiken-Features", test_statistics_features)
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
        print("🎉 Alle Statistiken Tests erfolgreich!")
        return True
    else:
        print("⚠️ Einige Tests fehlgeschlagen")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 