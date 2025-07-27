#!/usr/bin/env python3
"""
Test für verbesserte Marker-Erstellung
======================================

Demonstriert die neuen intelligenten ID-Generierungsfunktionen.
"""

import sys
import os
from pathlib import Path

# Pfad zum Projekt hinzufügen
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from marker_manager import MarkerManager

def test_improved_marker_creation():
    """Testet die verbesserte Marker-Erstellung."""
    
    print("🧪 Teste verbesserte Marker-Erstellung...")
    print("=" * 50)
    
    # MarkerManager initialisieren
    marker_manager = MarkerManager()
    
    # Test-Beispiele
    test_cases = [
        {
            "name": "Marker mit Beschreibung",
            "text": """
description: Datenbank-Verbindung konfigurieren
level: 2
category: database
examples:
  - MySQL-Verbindung einrichten
  - PostgreSQL-Konfiguration
"""
        },
        {
            "name": "Marker ohne ID, mit Beschreibung",
            "text": """
description: API-Endpunkt validieren
level: 1
category: api
examples:
  - Request-Parameter prüfen
  - Response-Format validieren
"""
        },
        {
            "name": "Marker mit expliziter ID",
            "text": """
id: API_VALIDATION
description: API-Validierung durchführen
level: 3
category: api
"""
        },
        {
            "name": "Marker mit langer Beschreibung",
            "text": """
description: Sehr lange und detaillierte Beschreibung für einen komplexen Marker mit vielen Wörtern
level: 4
category: complex
"""
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        # Marker parsen
        marker_data = marker_manager.smart_parse_text(test_case['text'])
        
        # Ergebnisse anzeigen
        print(f"ID: {marker_data.get('id', 'N/A')}")
        print(f"Beschreibung: {marker_data.get('description', 'N/A')}")
        print(f"Level: {marker_data.get('level', 'N/A')}")
        print(f"Kategorie: {marker_data.get('category', 'N/A')}")
        
        if 'examples' in marker_data:
            print(f"Beispiele: {len(marker_data['examples'])} gefunden")
    
    print("\n" + "=" * 50)
    print("✅ Test abgeschlossen!")
    print("\n💡 Verbesserungen:")
    print("• IDs werden aus Beschreibungen generiert")
    print("• Keine Platzhalternamen mehr")
    print("• Sinnvolle, lesbare IDs")
    print("• Automatische Längenbegrenzung")

def test_multi_marker_creation():
    """Testet Multi-Marker-Erstellung."""
    
    print("\n🧪 Teste Multi-Marker-Erstellung...")
    print("=" * 50)
    
    # Multi-Marker Text
    multi_marker_text = """
description: Erster Marker für Datenbank
level: 1
category: database
---
description: Zweiter Marker für API
level: 2
category: api
---
description: Dritter Marker für Validierung
level: 3
category: validation
"""
    
    marker_manager = MarkerManager()
    
    # Marker-Blöcke aufteilen
    blocks = multi_marker_text.split('---')
    
    print(f"Gefundene Marker-Blöcke: {len(blocks)}")
    print()
    
    for i, block in enumerate(blocks, 1):
        if not block.strip():
            continue
            
        print(f"📝 Marker {i}:")
        marker_data = marker_manager.smart_parse_text(block)
        print(f"  ID: {marker_data.get('id', 'N/A')}")
        print(f"  Beschreibung: {marker_data.get('description', 'N/A')}")
        print()

if __name__ == "__main__":
    test_improved_marker_creation()
    test_multi_marker_creation() 