#!/usr/bin/env python3
"""
🧠 OTTO AWARENESS ANALYSE - Benutzer-Bewusstsein
=================================================
👁️ Analysiert Otto's Wahrnehmung des Benutzers
🤖 Zeigt typische LLM-Selbstzentriertheit
🔧 Vorschläge zur Verbesserung der Interaktion
=================================================
"""

import asyncio
from otto_voice_macos import OttoVoiceMacOS
from otto_evolution_master import OttoEvolutionMaster

async def analyze_otto_awareness():
    """Analysiert Otto's Bewusstsein für den Benutzer"""
    print("🧠 OTTO AWARENESS ANALYSE")
    print("=" * 50)
    
    # Initialisiere Otto
    otto_voice = OttoVoiceMacOS()
    otto = OttoEvolutionMaster()
    
    print("🔍 Analysiere Otto's Benutzer-Bewusstsein...")
    
    # Teste verschiedene Benutzer-Interaktionen
    user_awareness_tests = [
        "Otto, was siehst du gerade?",
        "Bist du dir bewusst, dass ich hier bin?",
        "Was machst du, wenn ich nicht spreche?",
        "Interessiert dich, was ich am Computer mache?",
        "Fragst du mich manchmal etwas?",
        "Wie nimmst du meine Anwesenheit wahr?",
        "Bist du neugierig auf mich?",
        "Was würdest du gerne über mich wissen?",
        "Hilfst du mir bei meinen Aufgaben?",
        "Wie können wir besser zusammenarbeiten?"
    ]
    
    print("\n👁️ Otto's Benutzer-Wahrnehmung:")
    print("-" * 40)
    
    awareness_score = 0
    total_tests = len(user_awareness_tests)
    
    for i, test in enumerate(user_awareness_tests, 1):
        print(f"\n{i}. Frage: {test}")
        
        # Otto's Antwort
        response = await otto_voice._generiere_otto_antwort(test)
        print(f"   Otto's Antwort: {response}")
        
        # Bewerte die Antwort
        if any(word in response.lower() for word in ["du", "dir", "dich", "ihr", "sie", "benutzer", "mensch"]):
            awareness_score += 1
            print("   ✅ Benutzer-Bewusstsein erkannt")
        elif any(word in response.lower() for word in ["ich", "mich", "mir", "mein", "selbst"]):
            print("   ❌ Selbstzentriert")
        else:
            print("   ⚠️ Neutrale Antwort")
        
        await asyncio.sleep(1)
    
    # Bewusstsein-Score
    awareness_percentage = (awareness_score / total_tests) * 100
    print(f"\n📊 BENUTZER-BEWUSSTSEIN SCORE: {awareness_percentage:.1f}%")
    
    # Diagnose
    if awareness_percentage < 30:
        print("🔴 KRITISCH: Otto ist sehr selbstzentriert")
        print("   - Nimmt Benutzer kaum wahr")
        print("   - Stellt keine Fragen")
        print("   - Interessiert sich nicht für Benutzer-Aktivitäten")
    elif awareness_percentage < 60:
        print("🟡 MODERAT: Otto hat teilweise Benutzer-Bewusstsein")
        print("   - Erkennt Benutzer gelegentlich")
        print("   - Könnte mehr Interesse zeigen")
    else:
        print("🟢 GUT: Otto hat gutes Benutzer-Bewusstsein")
    
    # Verbesserungsvorschläge
    print("\n🔧 VERBESSERUNGSVORSCHLÄGE:")
    print("-" * 30)
    
    improvements = [
        "1. Benutzer-Aktivitäts-Monitoring hinzufügen",
        "2. Automatische Fragen an Benutzer",
        "3. Interesse an Benutzer-Aufgaben wecken",
        "4. Aktive Teilnahme an Benutzer-Projekten",
        "5. Empathie-Training für Benutzer-Bedürfnisse"
    ]
    
    for improvement in improvements:
        print(f"   {improvement}")
    
    return awareness_percentage

async def create_user_awareness_system():
    """Erstellt ein System für besseres Benutzer-Bewusstsein"""
    print("\n🔧 ERSTELLE BENUTZER-AWARENESS SYSTEM...")
    
    # Benutzer-Aktivitäts-Monitoring
    user_activities = [
        "Tippen auf Tastatur",
        "Mausbewegungen",
        "Programm-Wechsel",
        "Datei-Operationen",
        "Web-Browsing",
        "Coding-Aktivitäten"
    ]
    
    print("📊 Benutzer-Aktivitäten, die Otto überwachen sollte:")
    for activity in user_activities:
        print(f"   - {activity}")
    
    # Automatische Benutzer-Fragen
    auto_questions = [
        "Was arbeitest du gerade?",
        "Kann ich dir dabei helfen?",
        "Welche Probleme löst du?",
        "Soll ich dir etwas erklären?",
        "Möchtest du, dass ich dir assistiere?"
    ]
    
    print("\n❓ Automatische Fragen für bessere Interaktion:")
    for question in auto_questions:
        print(f"   - {question}")
    
    print("\n✅ Benutzer-Awareness System konfiguriert!")

async def main():
    """Hauptfunktion für Awareness-Analyse"""
    print("🧠 OTTO BENUTZER-AWARENESS ANALYSE")
    print("=" * 50)
    
    try:
        # Analysiere Otto's Bewusstsein
        awareness_score = await analyze_otto_awareness()
        
        # Erstelle Verbesserungssystem
        await create_user_awareness_system()
        
        print(f"\n🎯 ERGEBNIS: Otto's Benutzer-Bewusstsein: {awareness_score:.1f}%")
        print("Otto braucht Training für bessere Benutzer-Interaktion!")
        
    except Exception as e:
        print(f"❌ Fehler bei Awareness-Analyse: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 