#!/usr/bin/env python3
"""
SPRACHEINGABE für CoSD - Einfach sprechen und analysieren lassen!
"""

import speech_recognition as sr
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def sprache_erkennen():
    """Erkennt Spracheingabe und gibt Text zurück"""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("🎤 Sprich jetzt... (3 Sekunden)")
        r.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=10)
            print("🔍 Verarbeite Sprache...")
            
            text = r.recognize_google(audio, language='de-DE')
            print(f"✅ Erkannt: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            print("❌ Keine Sprache erkannt - zu leise oder zu kurz")
            return None
        except sr.UnknownValueError:
            print("❌ Sprache nicht verstanden")
            return None
        except sr.RequestError as e:
            print(f"❌ Fehler bei Spracherkennung: {e}")
            return None

def main():
    print("🎤 SPRACHEINGABE für CoSD")
    print("=" * 50)
    
    try:
        from cosd import CoSDAnalyzer
        print("✅ CoSD geladen!")
        
        analyzer = CoSDAnalyzer()
        print("✅ Analyzer bereit!")
        
        print("\n💡 So funktioniert's:")
        print("   1. Sprich deinen Text")
        print("   2. Warte auf Analyse")
        print("   3. Sieh das Ergebnis")
        print("   4. Wiederhole oder beende mit 'Ende'")
        
        while True:
            print("\n" + "-" * 30)
            print("🎤 Drücke Enter und sprich...")
            input()
            
            text = sprache_erkennen()
            if not text:
                continue
            
            if "ende" in text.lower() or "stop" in text.lower():
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
