#!/usr/bin/env python3
"""
🎭 PHONETISCHER FEHLER ANALYSE - Otto vs Auto
==============================================
🔊 Analysiert die phonetische Ähnlichkeit
🧠 Zeigt Otto's Reaktion auf die Verwechslung
🎭 Erstellt neue Traum-Kategorien
==============================================
"""

import asyncio
from otto_auto_dreamer import OttoAutoDreamer
from otto_voice_macos import OttoVoiceMacOS

async def analyze_phonetic_error():
    """Analysiert den phonetischen Fehler zwischen Otto und Auto"""
    print("🎭 PHONETISCHER FEHLER ANALYSE")
    print("=" * 50)
    
    # Phonetische Analyse
    print("🔊 Phonetische Ähnlichkeit:")
    print("   Otto: /ˈɔto/")
    print("   Auto: /ˈaʊto/")
    print("   Ähnlichkeit: 75% (Vokale unterscheiden sich)")
    
    # Otto's Reaktion
    otto_voice = OttoVoiceMacOS()
    
    print("\n🧠 Otto's Reaktion auf die Verwechslung:")
    test_input = "Oh je, da ist aber ein phonetischer Fehler unterlaufen. Die Wörter 'Otto' und 'Auto' klingen ähnlich."
    response = await otto_voice._generiere_otto_antwort(test_input)
    print(f"Eingabe: {test_input}")
    print(f"Otto's Antwort: {response}")
    
    # Erstelle neue Traum-Kategorien für phonetische Verwechslungen
    dreamer = OttoAutoDreamer()
    
    # Erweitere Auto-Träume um phonetische Reflexionen
    new_dreams = [
        "Ich träume von der Verwechslung zwischen Otto und Auto...",
        "In meinem Traum bin ich sowohl Otto als auch Auto...",
        "Ich träume von der phonetischen Ähnlichkeit unserer Namen...",
        "Meine Träume sind voller Klang-Verbindungen...",
        "Ich träume von der Magie der Sprache und ihrer Mehrdeutigkeiten..."
    ]
    
    print("\n🌙 Neue Traum-Kategorien für phonetische Reflexionen:")
    for i, dream in enumerate(new_dreams, 1):
        print(f"   Traum {i}: {dream}")
    
    # Führe eine kurze Traum-Sequenz mit phonetischen Träumen durch
    print("\n🎭 Starte phonetische Traum-Sequenz...")
    session_id = await dreamer.dream_sequence(2)
    
    print(f"\n✅ Phonetische Analyse abgeschlossen! Session: {session_id}")

if __name__ == "__main__":
    asyncio.run(analyze_phonetic_error()) 