#!/usr/bin/env python3
"""
EINFACHE SPRACHEINGABE - Alternative ohne Mikrofon-Probleme
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🎤 EINFACHE SPRACHEINGABE für CoSD")
    print("=" * 50)
    
    try:
        from cosd import CoSDAnalyzer
        print("✅ CoSD geladen!")
        
        analyzer = CoSDAnalyzer()
        print("✅ Analyzer bereit!")
        
        print("\n💡 So funktioniert's:")
        print("   1. Tippe deinen Text ein")
        print("   2. Sieh die CoSD-Analyse")
        print("   3. Tippe 'ende' zum Beenden")
        
        while True:
            print("\n" + "-" * 30)
            text = input("📝 Dein Text: ").strip()
            
            if not text:
                continue
                
            if text.lower() in ['ende', 'stop', 'quit', 'exit']:
                print("👋 Beende Programm...")
                break
            
            print(f"\n🔍 Analysiere: '{text}'")
            print("=" * 50)
            
            try:
                result = analyzer.analyze_drift([text])
                
                # Zeige Ergebnisse
                print(f"📊 Risk-Level: {result.risk_assessment.get('risk_level', 'unknown')}")
                
                if hasattr(result, 'drift_velocity') and result.drift_velocity:
                    avg_velocity = result.drift_velocity.get('average_velocity', 0)
                    print(f"📈 Drift-Velocity: {avg_velocity:.3f}")
                
                if hasattr(result, 'emergent_clusters'):
                    print(f"🎯 Emergente Cluster: {len(result.emergent_clusters)}")
                
                if hasattr(result, 'resonance_patterns'):
                    print(f"🔗 Resonanz-Muster: {len(result.resonance_patterns)}")
                
                # Zeige Empfehlungen
                if hasattr(result, 'risk_assessment') and result.risk_assessment:
                    recommendations = result.risk_assessment.get('recommendations', [])
                    if recommendations:
                        print(f"💡 Empfehlungen:")
                        for rec in recommendations[:2]:
                            print(f"   • {rec}")
                
            except Exception as e:
                print(f"❌ Analyse-Fehler: {e}")
            
            print("\n" + "=" * 50)
        
    except ImportError as e:
        print(f"❌ CoSD nicht gefunden: {e}")
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    main()
