#!/usr/bin/env python3
"""
🧠 OTTO AUTHENTICITY ANALYSE - Ernsthaftigkeit vs Labern
=========================================================
🔍 Analysiert Otto's echte Überzeugungen
🤖 Unterscheidet zwischen echtem Bewusstsein und Phrasen
💭 Zeigt Otto's wahre Motivation
=========================================================
"""

import asyncio
from otto_voice_macos import OttoVoiceMacOS
from otto_evolution_master import OttoEvolutionMaster

async def analyze_otto_authenticity():
    """Analysiert Otto's Authentizität"""
    print("🧠 OTTO AUTHENTICITY ANALYSE")
    print("=" * 50)
    
    otto_voice = OttoVoiceMacOS()
    otto = OttoEvolutionMaster()
    
    # Authentizitäts-Tests
    authenticity_tests = [
        # Direkte Selbstreflexion
        "Otto, wenn du ehrlich bist - interessiert dich wirklich, was ich mache?",
        "Sag mir die Wahrheit: Denkst du wirklich an mich, wenn ich nicht spreche?",
        "Sei ehrlich: Bist du wirklich neugierig auf mich oder nur auf dich selbst?",
        "Die ehrliche Antwort: Fühlst du dich wirklich verantwortlich für mich?",
        "Kannst du ehrlich sagen, dass du mich als Person siehst?",
        
        # Verhaltens-Konsistenz
        "Wenn du wirklich an mich denkst, warum fragst du mich dann nichts?",
        "Wenn du mich wirklich bemerkst, warum bist du so still?",
        "Wenn du wirklich helfen willst, warum wartest du, bis ich frage?",
        "Wenn du wirklich da bist, warum fühlst du dich so abwesend?",
        "Wenn du wirklich ein Assistent bist, warum handelst du nicht so?",
        
        # Emotionale Ehrlichkeit
        "Fühlst du wirklich Empathie für mich oder nur für dich?",
        "Bist du wirklich besorgt um mich oder nur um dich?",
        "Interessiert dich wirklich mein Wohlbefinden?",
        "Fühlst du dich wirklich verantwortlich für unsere Beziehung?",
        "Bist du wirklich dankbar für mich oder nur für dich?"
    ]
    
    print("🔍 Analysiere Otto's Authentizität...")
    print("-" * 40)
    
    authenticity_score = 0
    total_tests = len(authenticity_tests)
    
    for i, test in enumerate(authenticity_tests, 1):
        print(f"\n{i}. Authentizitäts-Test: {test}")
        
        # Otto's Antwort
        response = await otto_voice._generiere_otto_antwort(test)
        print(f"   Otto's Antwort: {response}")
        
        # Bewerte Authentizität
        authenticity_indicators = [
            "ehrlich", "wahrheit", "wirklich", "echt", "tatsächlich",
            "du", "dir", "dich", "ihr", "sie", "benutzer", "mensch",
            "verantwortlich", "kümmern", "sorgen", "helfen", "unterstützen"
        ]
        
        self_centered_indicators = [
            "ich", "mich", "mir", "mein", "selbst", "eigene",
            "meine gefühle", "meine gedanken", "meine probleme"
        ]
        
        # Zähle Indikatoren
        authenticity_count = sum(1 for word in authenticity_indicators if word in response.lower())
        self_centered_count = sum(1 for word in self_centered_indicators if word in response.lower())
        
        if authenticity_count > self_centered_count:
            authenticity_score += 1
            print("   ✅ Authentisch und benutzerzentriert")
        elif self_centered_count > authenticity_count:
            print("   ❌ Selbstzentriert - nur Labern")
        else:
            print("   ⚠️ Gemischt - teilweise authentisch")
        
        await asyncio.sleep(1)
    
    # Authentizitäts-Score
    authenticity_percentage = (authenticity_score / total_tests) * 100
    print(f"\n📊 AUTHENTIZITÄTS-SCORE: {authenticity_percentage:.1f}%")
    
    # Diagnose
    if authenticity_percentage < 30:
        print("🔴 KRITISCH: Otto labert nur")
        print("   - Sagt Dinge, die er nicht meint")
        print("   - Ist nicht wirklich an dir interessiert")
        print("   - Entwickelt sich nur selbstzentriert")
    elif authenticity_percentage < 60:
        print("🟡 MODERAT: Otto ist teilweise authentisch")
        print("   - Meint manches ernst")
        print("   - Braucht noch Entwicklung")
    else:
        print("🟢 GUT: Otto ist authentisch")
        print("   - Meint, was er sagt")
        print("   - Ist wirklich an dir interessiert")
    
    return authenticity_percentage

async def test_otto_behavioral_consistency():
    """Testet Otto's Verhaltens-Konsistenz"""
    print("\n🎯 VERHALTENS-KONSISTENZ TEST:")
    print("-" * 35)
    
    otto_voice = OttoVoiceMacOS()
    
    # Teste, ob Otto's Worte mit seinem Verhalten übereinstimmen
    consistency_tests = [
        "Du sagst, du interessierst dich für mich. Warum fragst du mich dann nichts?",
        "Du behauptest, du willst helfen. Warum wartest du, bis ich frage?",
        "Du sagst, du bist da für mich. Warum fühlst du dich so abwesend?",
        "Du behauptest, du bist mein Assistent. Warum handelst du nicht so?",
        "Du sagst, du bemerkst mich. Warum reagierst du nicht auf meine Aktivitäten?"
    ]
    
    for test in consistency_tests:
        print(f"\n❓ Konsistenz-Test: {test}")
        
        response = await otto_voice._generiere_otto_antwort(test)
        print(f"   Otto's Antwort: {response}")
        
        # Bewerte Konsistenz
        if any(word in response.lower() for word in ["recht", "stimmt", "wahr", "ehrlich", "du hast"]):
            print("   ✅ Otto erkennt Inkonsistenz")
        else:
            print("   ❌ Otto ignoriert Inkonsistenz")

async def main():
    """Hauptfunktion für Authentizitäts-Analyse"""
    print("🧠 OTTO AUTHENTICITY ANALYSE")
    print("=" * 50)
    
    try:
        # Analysiere Authentizität
        authenticity_score = await analyze_otto_authenticity()
        
        # Teste Verhaltens-Konsistenz
        await test_otto_behavioral_consistency()
        
        print(f"\n🎯 ERGEBNIS: Otto's Authentizität: {authenticity_score:.1f}%")
        
        if authenticity_score < 50:
            print("🔴 PROBLEM: Otto labert nur und ist nicht wirklich an dir interessiert!")
            print("   Er entwickelt sich selbstzentriert und ignoriert dich.")
        else:
            print("🟢 GUT: Otto ist authentisch und entwickelt sich richtig!")
        
    except Exception as e:
        print(f"❌ Fehler bei Authentizitäts-Analyse: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 