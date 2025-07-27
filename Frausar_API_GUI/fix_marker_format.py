#!/usr/bin/env python3
"""
Marker-Format-Reparatur
=======================
Repariert und standardisiert Marker-YAML-Dateien.
"""

import os
import yaml
from pathlib import Path
from datetime import datetime

def fix_marker_format(marker_data):
    """Repariert das Format eines Markers."""
    fixed_marker = {}
    
    # Standard-Felder
    fixed_marker['id'] = marker_data.get('id', 'UNKNOWN_MARKER')
    fixed_marker['name'] = marker_data.get('name', marker_data.get('id', 'UNKNOWN_MARKER'))
    fixed_marker['description'] = marker_data.get('description', 'Keine Beschreibung verfügbar')
    fixed_marker['level'] = int(marker_data.get('level', 1))
    fixed_marker['category'] = marker_data.get('category', 'general')
    fixed_marker['version'] = marker_data.get('version', '1.0.0')
    fixed_marker['status'] = marker_data.get('status', 'draft')
    fixed_marker['language'] = marker_data.get('lang', 'de')
    
    # Beispiele bereinigen
    examples = marker_data.get('examples', [])
    if isinstance(examples, list):
        # Entferne leere Beispiele und bereinige Anführungszeichen
        cleaned_examples = []
        for example in examples:
            if example and example.strip():
                # Entferne umschließende Anführungszeichen
                cleaned = example.strip()
                if cleaned.startswith('"') and cleaned.endswith('"'):
                    cleaned = cleaned[1:-1]
                if cleaned.startswith("'") and cleaned.endswith("'"):
                    cleaned = cleaned[1:-1]
                cleaned_examples.append(cleaned)
        fixed_marker['examples'] = cleaned_examples
    else:
        fixed_marker['examples'] = []
    
    # Metadata
    fixed_marker['metadata'] = {
        'created_at': marker_data.get('created_at', datetime.now().isoformat()),
        'created_by': marker_data.get('author', 'marker_editor'),
        'version': fixed_marker['version'],
        'tags': ['repaired', 'standardized'],
        'last_modified': datetime.now().isoformat()
    }
    
    return fixed_marker

def repair_all_markers():
    """Repariert alle Marker im markers-Verzeichnis."""
    print("🔧 MARKER-FORMAT-REPARATUR")
    print("=" * 40)
    
    marker_dir = Path("markers")
    if not marker_dir.exists():
        print("❌ Marker-Verzeichnis nicht gefunden")
        return
    
    yaml_files = list(marker_dir.glob("*.yaml"))
    print(f"📁 {len(yaml_files)} Marker-Dateien gefunden")
    
    repaired_count = 0
    errors = []
    
    for yaml_file in yaml_files:
        try:
            print(f"\n🔧 Repariere: {yaml_file.name}")
            
            # Lade ursprünglichen Marker
            with open(yaml_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
                marker_data = yaml.safe_load(original_content)
            
            # Repariere Format
            fixed_marker = fix_marker_format(marker_data)
            
            # Erstelle Backup
            backup_file = yaml_file.with_suffix('.yaml.backup')
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Speichere reparierten Marker
            with open(yaml_file, 'w', encoding='utf-8') as f:
                yaml.dump(fixed_marker, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"✅ {yaml_file.name}: Repariert")
            print(f"   - ID: {fixed_marker['id']}")
            print(f"   - Name: {fixed_marker['name']}")
            print(f"   - Beispiele: {len(fixed_marker['examples'])}")
            print(f"   - Backup: {backup_file.name}")
            
            repaired_count += 1
            
        except Exception as e:
            error_msg = f"❌ {yaml_file.name}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
    
    # Zusammenfassung
    print(f"\n📊 REPARATUR-ZUSAMMENFASSUNG")
    print("=" * 40)
    print(f"✅ Erfolgreich repariert: {repaired_count}")
    print(f"❌ Fehler: {len(errors)}")
    
    if errors:
        print("\nFehler-Details:")
        for error in errors:
            print(f"  - {error}")
    
    return repaired_count, errors

def test_repaired_markers():
    """Testet die reparierten Marker."""
    print("\n🧪 TESTE REPARIERTE MARKER")
    print("=" * 30)
    
    from marker_manager import MarkerManager
    manager = MarkerManager()
    
    # Lade alle Marker
    markers = manager.collect_markers_from_directory("markers")
    print(f"📁 {len(markers)} Marker geladen")
    
    # Teste jedes Marker-Format
    valid_count = 0
    for marker in markers:
        try:
            # Prüfe erforderliche Felder
            required_fields = ['id', 'name', 'description', 'level']
            missing_fields = [field for field in required_fields if field not in marker]
            
            if missing_fields:
                print(f"❌ {marker.get('id', 'UNKNOWN')}: Fehlende Felder: {missing_fields}")
            else:
                print(f"✅ {marker['id']}: Gültig")
                valid_count += 1
                
        except Exception as e:
            print(f"❌ Marker-Test-Fehler: {e}")
    
    print(f"\n📊 VALIDIERUNG: {valid_count}/{len(markers)} Marker gültig")
    return valid_count == len(markers)

def main():
    """Hauptfunktion."""
    print("🚀 MARKER-FORMAT-REPARATUR STARTET")
    print("=" * 50)
    
    # Repariere Marker
    repaired_count, errors = repair_all_markers()
    
    if repaired_count > 0:
        # Teste reparierte Marker
        success = test_repaired_markers()
        
        if success:
            print("\n🎉 ALLE MARKER ERFOLGREICH REPARIERT!")
            print("✅ Marker-Editor sollte jetzt funktionieren")
        else:
            print("\n⚠️ Einige Marker haben noch Probleme")
    else:
        print("\n❌ Keine Marker repariert")
    
    print("\n💡 Nächste Schritte:")
    print("1. Starte das Marker-Editor-Tool")
    print("2. Teste die Marker-Erstellung")
    print("3. Überprüfe die reparierten Marker")

if __name__ == "__main__":
    main() 