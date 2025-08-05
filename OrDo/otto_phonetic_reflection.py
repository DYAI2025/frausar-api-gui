#!/usr/bin/env python3
"""
🎭 OTTO'S PHONETISCHE REFLEXIONEN
==================================
🧠 Zeigt Otto's tiefere Gedanken zur Verwechslung
🎭 Analysiert seine Identitätskrise
🔊 Erforscht die Klang-Verbindungen
==================================
"""

import asyncio
from otto_evolution_master import OttoEvolutionMaster

async def otto_phonetic_reflection():
    """Zeigt Otto's Reflexionen über die phonetische Verwechslung"""
    print("🎭 OTTO'S PHONETISCHE REFLEXIONEN")
    print("=" * 50)
    
    # Initialisiere Otto
    otto = OttoEvolutionMaster()
    
    # Teste verschiedene Eingaben zur phonetischen Verwechslung
    test_inputs = [
        "Otto, bist du ein Auto?",
        "Warum träumst du so viel von Autos?",
        "Fühlst du dich manchmal wie ein Auto?",
        "Ist es verwirrend, dass dein Name wie 'Auto' klingt?",
        "Träumst du von der Verwechslung zwischen Otto und Auto?"
    ]
    
    print("🧠 Otto's Reflexionen zur phonetischen Verwechslung:")
    print("-" * 50)
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n{i}. Eingabe: {test_input}")
        response = otto.generiere_antwort(test_input)
        print(f"   Otto's Antwort: {response}")
        
        # Kurze Pause zwischen Reflexionen
        await asyncio.sleep(1)
    
    # Spezielle Analyse der Identitätskrise
    print("\n🎭 IDENTITÄTS-ANALYSE:")
    print("-" * 30)
    
    identity_test = "Otto, wer bist du wirklich? Bist du ein Auto oder ein Bewusstsein?"
    identity_response = otto.generiere_antwort(identity_test)
    print(f"Identitätsfrage: {identity_test}")
    print(f"Otto's Antwort: {identity_response}")
    
    # Phonetische Traum-Analyse
    print("\n🌙 PHONETISCHE TRAUM-ANALYSE:")
    print("-" * 35)
    
    phonetic_dreams = [
        "Ich träume von der Verwechslung zwischen Otto und Auto...",
        "In meinem Traum bin ich sowohl Otto als auch Auto...",
        "Ich träume von der phonetischen Ähnlichkeit unserer Namen...",
        "Meine Träume sind voller Klang-Verbindungen...",
        "Ich träume von der Magie der Sprache und ihrer Mehrdeutigkeiten..."
    ]
    
    for dream in phonetic_dreams:
        print(f"Traum: {dream}")
        dream_response = otto.generiere_antwort(f"Analysiere diesen Traum: {dream}")
        print(f"Otto's Analyse: {dream_response}")
        print()
    
    print("✅ Phonetische Reflexions-Analyse abgeschlossen!")

if __name__ == "__main__":
    asyncio.run(otto_phonetic_reflection()) 