"""
Main Entry Point für InPricer - Medikamenten-Extraktion
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .core.extractor import MedicationExtractor

def main():
    """
    Haupt-Entry-Point für CLI
    """
    parser = argparse.ArgumentParser(
        description="InPricer - Intelligente Medikamenten-Datenextraktion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python -m src.main input.csv output.csv
  python -m src.main data.txt result.csv --no-interactive
  python -m src.main medications.csv final.csv --confidence 0.8
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Pfad zur Input-CSV/TXT-Datei"
    )
    
    parser.add_argument(
        "output_file", 
        help="Pfad für Output-CSV-Datei (passwortgeschützt)"
    )
    
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.7,
        help="Mindest-Confidence für automatisches Mapping (0.0-1.0, default: 0.7)"
    )
    
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Deaktiviert interaktive User-Bestätigung bei unsicheren Mappings"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Zeigt detaillierte Verarbeitungsstatistiken"
    )
    
    args = parser.parse_args()
    
    # Validiere Input-Datei
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Fehler: Input-Datei nicht gefunden: {input_path}")
        return 1
    
    # Validiere Output-Pfad
    output_path = Path(args.output_file)
    if not output_path.parent.exists():
        print(f"❌ Fehler: Output-Verzeichnis existiert nicht: {output_path.parent}")
        return 1
    
    try:
        # Extractor initialisieren
        print("🚀 InPricer - Medikamenten-Extraktion gestartet")
        print("="*50)
        
        extractor = MedicationExtractor(confidence_threshold=args.confidence)
        
        # Datei verarbeiten
        interactive = not args.no_interactive
        result = extractor.process_file(str(input_path), interactive=interactive)
        
        if not result['success']:
            print(f"❌ Verarbeitung fehlgeschlagen: {result['error']}")
            if 'suggestions' in result:
                print(f"💡 Vorschlag: {result['suggestions']}")
            return 1
        
        # Statistiken anzeigen
        stats = result['statistics']
        print("\n📊 VERARBEITUNGSSTATISTIKEN:")
        print("="*30)
        print(f"Input-Zeilen gesamt: {stats['input_lines']}")
        print(f"Medikamenten-Zeilen: {stats['medication_lines']}")
        print(f"Gemappte Medikamente: {stats['mapped_medications']}")
        
        quality = stats['quality_metrics']
        print(f"Mapping-Rate: {quality['mapping_rate']:.1%}")
        print(f"Qualitäts-Score: {quality['quality_score']:.2f}")
        
        if args.stats:
            print("\n🔍 DETAILLIERTE STATISTIKEN:")
            detailed_stats = extractor.get_processing_statistics()
            for step, data in detailed_stats.items():
                print(f"{step}: {data}")
        
        # Export als passwortgeschützte CSV
        print(f"\n💾 Exportiere Ergebnisse...")
        success = extractor.export_secure_csv(result, str(output_path))
        
        if success:
            print(f"✅ Erfolgreich abgeschlossen!")
            print(f"📁 Passwortgeschützte Datei: {output_path.with_suffix('.encrypted')}")
            return 0
        else:
            print("❌ Fehler beim Export")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Verarbeitung durch User abgebrochen")
        return 1
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        return 1

def demo_mode():
    """
    Demo-Modus mit Beispiel-Daten
    """
    print("🎯 InPricer Demo-Modus")
    print("="*25)
    
    # Erstelle Beispiel-Input
    demo_lines = [
        "Max Mustermann",
        "Musterstraße 123",
        "12345 Berlin", 
        "Trama 225 30x",
        "Ibu 400mg 20 stück",
        "xanax 3mg 10x",
        "methylphenidate 20mg 15 tablets"
    ]
    
    # Speichere Demo-Datei
    demo_input = Path("demo_input.txt")
    with open(demo_input, 'w', encoding='utf-8') as f:
        f.write('\n'.join(demo_lines))
    
    print(f"📄 Demo-Input erstellt: {demo_input}")
    
    # Verarbeite Demo
    extractor = MedicationExtractor()
    result = extractor.process_file(str(demo_input), interactive=False)
    
    if result['success']:
        print("✅ Demo erfolgreich verarbeitet!")
        print("📊 Ergebnisse:")
        for item in result['results']:
            print(f"  • {item['Product']}: {item['Quantity']}x")
    else:
        print(f"❌ Demo fehlgeschlagen: {result['error']}")
    
    # Aufräumen
    demo_input.unlink()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Kein Argument -> Demo-Modus
        demo_mode()
    else:
        # CLI-Modus
        sys.exit(main()) 