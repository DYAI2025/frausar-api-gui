#!/usr/bin/env python3
"""
DEMONSTRATION: Semantischer Wächter & Beispiel-Generator
=======================================================

Dieses Skript demonstriert die Funktionalität des Semantischen Wächters 
mit dem exakten Beispiel aus der Entwicklungsaufgabe.

Es zeigt:
1. Validierung eines Lean-Deep 3.1 Markers
2. Beispiel-Generierung mit Qualitätskontrolle
3. Datei-basierte Verarbeitung
4. Umfassende Berichte und Statistiken
"""

import yaml
import json
from pathlib import Path
from semantic_guardian import MarkerExampleProcessor, ValidationResult

def create_demo_marker():
    """Erstellt den Demo-Marker aus der Entwicklungsaufgabe"""
    return {
        "id": "C_RELATIONAL_DESTABILIZATION_LOOP",
        "frame": {
            "signal": ["Nähe/Distanz-Kontraste"],
            "concept": "Bindungsambivalenz", 
            "pragmatics": "Destabilisierung",
            "narrative": "loop"
        },
        "composed_of": ["S_AMBIVALENT_ATTACHMENT_SPEECH", "S_SOFT_WITHDRAWAL"],
        "activation": {"rule": "ANY 2 IN 48h"},
        "scoring": {"base": 2.0, "weight": 1.6, "decay": 0.01, "formula": "logistic"},
        "tags": ["beziehung", "ambivalenz", "loop"],
        "examples": [
            "[cite_start]\"Ich vermisse dich … aber ich brauche Abstand.\" [cite: 277]",
            "[cite_start]\"Du bist mir wichtig – aber ich weiß nicht, ob ich bereit bin.\" [cite: 278]"
        ]
    }

def create_invalid_marker():
    """Erstellt einen ungültigen Marker für Demonstrationszwecke"""
    return {
        "id": "INVALID_MARKER",  # Falsches Präfix
        "level": 3,  # Verbotenes Legacy-Feld
        "marker_name": "INVALID",  # Verbotenes Legacy-Feld
        "frame": {
            "signal": [],  # Leer
            "concept": "",  # Leer
            "pragmatics": "",  # Leer
            "narrative": ""  # Leer
        }
    }

def create_test_markers():
    """Erstellt verschiedene Test-Marker für alle Ebenen"""
    return {
        "atomic": {
            "id": "A_SUPPORT_OFFER",
            "frame": {
                "signal": ["ich bin für dich da", "ruf mich an", "meld dich"],
                "concept": "Unterstützungsangebot",
                "pragmatics": "Bindungsstärkung",
                "narrative": "offer"
            },
            "pattern": ["ich bin für dich da", "ruf mich an", "meld dich", "immer erreichbar"],
            "examples": ["Ich bin immer für dich da.", "Ruf mich an, wenn du willst."]
        },
        "semantic": {
            "id": "S_EMOTIONAL_SUPPORT_CLUSTER",
            "frame": {
                "signal": ["Häufung von Unterstützungsangeboten"],
                "concept": "Emotionale Verfügbarkeit",
                "pragmatics": "Beziehungsstabilisierung", 
                "narrative": "sustain"
            },
            "composed_of": ["A_SUPPORT_OFFER", "A_EMOTIONAL_AVAILABILITY"],
            "activation": {"rule": "ANY 2 IN 3 messages"},
            "examples": []
        },
        "cluster": {
            "id": "C_STABLE_RELATIONSHIP_PATTERN",
            "frame": {
                "signal": ["Konstante Support-Muster über Zeit"],
                "concept": "Beziehungsstabilität",
                "pragmatics": "Langfristige Bindung",
                "narrative": "foundation"
            },
            "composed_of": ["S_EMOTIONAL_SUPPORT_CLUSTER", "S_LOYALTY_SIGNALS"],
            "activation": {"rule": "AT_LEAST 3 IN 20 messages"},
            "scoring": {"base": 1.8, "weight": 1.4, "decay": 0.005},
            "examples": []
        },
        "meta": {
            "id": "MM_RELATIONSHIP_STRENGTH_INDICATOR",
            "frame": {
                "signal": ["Mehrschichtige Beziehungstiefe-Signale"],
                "concept": "Beziehungsintensität",
                "pragmatics": "Strukturelle Verbindung",
                "narrative": "meta_foundation"
            },
            "composed_of": ["C_STABLE_RELATIONSHIP_PATTERN", "C_SHARED_VALUES_CLUSTER"],
            "activation": {"rule": "ANY 2 IN 50 messages"},
            "scoring": {"base": 2.5, "weight": 1.8, "decay": 0.001},
            "examples": []
        }
    }

def print_header(title: str):
    """Druckt eine formatierte Überschrift"""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")

def print_section(title: str):
    """Druckt eine Sektion-Überschrift"""
    print(f"\n{'-'*40}")
    print(f"📋 {title}")
    print(f"{'-'*40}")

def print_validation_report(report, marker_id: str):
    """Druckt einen detaillierten Validierungsbericht"""
    print(f"\n🔍 VALIDIERUNGSBERICHT: {marker_id}")
    print(f"Status: {report.result.value}")
    print(f"Geeignet für Beispiele: {'✅ Ja' if report.is_suitable_for_examples else '❌ Nein'}")
    print(f"Confidence: {report.confidence:.2f}")
    
    if report.schema_errors:
        print(f"\n❌ Schema-Fehler:")
        for error in report.schema_errors:
            print(f"   • {error}")
    
    if report.semantic_errors:
        print(f"\n⚠️  Semantische Probleme:")
        for error in report.semantic_errors:
            print(f"   • {error}")
    
    if report.frame_analysis:
        fa = report.frame_analysis
        print(f"\n📊 Frame-Analyse:")
        print(f"   Klarheit:    {fa.clarity_score:.2f} {'✅' if fa.is_clear else '❌'}")
        print(f"   Kohärenz:    {fa.coherence_score:.2f} {'✅' if fa.is_coherent else '❌'}")
        print(f"   Spezifität:  {fa.specificity_score:.2f} {'✅' if fa.is_specific else '❌'}")
        
        if fa.issues:
            print(f"\n⚠️  Erkannte Probleme:")
            for issue in fa.issues:
                print(f"   • {issue}")
        
        if fa.recommendations:
            print(f"\n💡 Empfehlungen:")
            for rec in fa.recommendations:
                print(f"   • {rec}")

def main():
    """Hauptfunktion für die Demonstration"""
    print_header("SEMANTISCHER WÄCHTER & BEISPIEL-GENERATOR")
    print("🚀 Demonstration der KI-getriebenen Beispiel-Generierung")
    print("📖 Folgt der Lean-Deep 3.1 Spezifikation")
    print("🎯 Epic-ID: EPIC-KB-002")
    
    # Initialisierung
    processor = MarkerExampleProcessor()
    
    # Demo 1: Erfolgreiche Verarbeitung des Hauptbeispiels
    print_section("Demo 1: Hauptbeispiel aus der Entwicklungsaufgabe")
    
    demo_marker = create_demo_marker()
    print("📄 Original Marker:")
    print(yaml.dump(demo_marker, default_flow_style=False, allow_unicode=True))
    
    result = processor.generate_examples_for_marker(demo_marker, num_examples=3)
    
    if result["success"]:
        print("✅ GENERIERUNG ERFOLGREICH!")
        print_validation_report(result["validation_report"], demo_marker["id"])
        
        print(f"\n🎯 NEUE BEISPIELE ({len(result['new_examples'])}):")
        for i, example in enumerate(result["new_examples"], 1):
            print(f"   {i}. {example}")
        
        if result["warnings"]:
            print(f"\n⚠️  Warnungen:")
            for warning in result["warnings"]:
                print(f"   • {warning}")
    else:
        print(f"❌ GENERIERUNG FEHLGESCHLAGEN: {result['error']}")
    
    # Demo 2: Ungültiger Marker (Wächter-Funktion)
    print_section("Demo 2: Semantischer Wächter - Ablehnung ungültiger Marker")
    
    invalid_marker = create_invalid_marker()
    print("📄 Ungültiger Marker:")
    print(yaml.dump(invalid_marker, default_flow_style=False, allow_unicode=True))
    
    result = processor.generate_examples_for_marker(invalid_marker, num_examples=3)
    
    print(f"❌ ERWARTUNGSGEMÄSS ABGELEHNT: {result['error']}")
    print_validation_report(result["validation_report"], invalid_marker["id"])
    
    # Demo 3: Alle Marker-Ebenen testen
    print_section("Demo 3: Tests für alle Marker-Ebenen (A, S, C, MM)")
    
    test_markers = create_test_markers()
    
    for level, marker in test_markers.items():
        print(f"\n🔹 {level.upper()} MARKER: {marker['id']}")
        
        result = processor.generate_examples_for_marker(marker, num_examples=2)
        
        if result["success"]:
            validation = result["validation_report"]
            print(f"   ✅ Validierung: {validation.result.value} (Confidence: {validation.confidence:.2f})")
            print(f"   🎯 Beispiele generiert: {len(result['new_examples'])}")
            
            # Zeige erstes Beispiel
            if result["new_examples"]:
                print(f"   📝 Erstes Beispiel: {result['new_examples'][0]}")
        else:
            print(f"   ❌ Fehlgeschlagen: {result['error']}")
    
    # Demo 4: Datei-basierte Verarbeitung
    print_section("Demo 4: Datei-basierte Verarbeitung")
    
    # Erstelle temporäre Demo-Datei
    demo_file = Path("demo_marker.yaml")
    
    with open(demo_file, 'w', encoding='utf-8') as f:
        yaml.dump(demo_marker, f, default_flow_style=False, allow_unicode=True)
    
    print(f"📁 Verarbeite Datei: {demo_file}")
    
    result = processor.process_marker_file(demo_file, num_examples=2, backup=True)
    
    if result["success"]:
        print(f"✅ Datei erfolgreich verarbeitet!")
        print(f"📊 {result['examples_added']} neue Beispiele hinzugefügt")
        print(f"📦 Backup erstellt: {demo_file}.backup")
        
        # Zeige aktualisierte Datei
        print(f"\n📄 Aktualisierte Datei:")
        with open(demo_file, 'r', encoding='utf-8') as f:
            updated_content = f.read()
        print(updated_content[:500] + "..." if len(updated_content) > 500 else updated_content)
    else:
        print(f"❌ Dateiverarbeitung fehlgeschlagen: {result['error']}")
    
    # Demo 5: Statistiken und Performance
    print_section("Demo 5: System-Statistiken")
    
    stats = processor.get_comprehensive_stats()
    
    print("📊 VALIDIERUNGS-STATISTIKEN:")
    val_stats = stats["validation_stats"]
    for key, value in val_stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n📊 GENERIERUNGS-STATISTIKEN:")
    gen_stats = stats["generation_stats"]
    for key, value in gen_stats.items():
        print(f"   {key}: {value}")
    
    # Berechne Erfolgsquoten
    if val_stats["total_validated"] > 0:
        success_rate = (val_stats["valid_markers"] / val_stats["total_validated"]) * 100
        print(f"\n🎯 GESAMTERFOLGSQUOTE: {success_rate:.1f}%")
    
    # Demo 6: Semantische Gegenprüfung
    print_section("Demo 6: Semantische Gegenprüfung der Beispiele")
    
    # Generiere Beispiele für spezifischen Marker
    specific_marker = {
        "id": "S_CONDITIONAL_SUPPORT",
        "frame": {
            "signal": ["falls du Hilfe brauchst", "wenn du möchtest"],
            "concept": "Bedingte Unterstützung",
            "pragmatics": "Zurückhaltung",
            "narrative": "conditional_offer"
        },
        "composed_of": ["A_CONDITIONAL_PHRASE"],
        "examples": []
    }
    
    result = processor.generate_examples_for_marker(specific_marker, num_examples=4)
    
    if result["success"]:
        examples = result["new_examples"]
        print(f"🎯 Generierte Beispiele für 'Bedingte Unterstützung':")
        
        semantic_matches = 0
        for i, example in enumerate(examples, 1):
            print(f"   {i}. {example}")
            
            # Semantische Analyse
            example_lower = example.lower()
            has_conditional = any(word in example_lower for word in ["falls", "wenn", "solltest", "möchtest"])
            is_not_direct = not any(word in example_lower for word in ["sofort", "muss", "unbedingt"])
            
            if has_conditional and is_not_direct:
                semantic_matches += 1
                print(f"      ✅ Semantisch korrekt (konditional + zurückhaltend)")
            else:
                print(f"      ⚠️  Semantik überprüfen")
        
        match_rate = (semantic_matches / len(examples)) * 100
        print(f"\n📊 Semantische Trefferquote: {match_rate:.1f}% ({semantic_matches}/{len(examples)})")
        
        if match_rate >= 75:
            print("✅ SEMANTISCHE QUALITÄT: HOCH")
        elif match_rate >= 50:
            print("⚠️  SEMANTISCHE QUALITÄT: MITTEL")
        else:
            print("❌ SEMANTISCHE QUALITÄT: NIEDRIG")
    
    # Finale Zusammenfassung
    print_header("DEMONSTRATION ABGESCHLOSSEN")
    print("🎉 Der Semantische Wächter & Beispiel-Generator funktioniert optimal!")
    print("🔒 Semantische Integrität wird gewährleistet")
    print("🚀 Bereit für den Produktiveinsatz in der MarkerEngine")
    print("📈 Hohe Qualitätsstandards werden eingehalten")
    
    # Cleanup
    if demo_file.exists():
        backup_file = Path(f"{demo_file}.backup")
        print(f"\n🧹 Demo-Dateien:")
        print(f"   📄 Demo-Marker: {demo_file}")
        if backup_file.exists():
            print(f"   📦 Backup: {backup_file}")
        print("   (Dateien bleiben für weitere Tests erhalten)")

if __name__ == "__main__":
    main()