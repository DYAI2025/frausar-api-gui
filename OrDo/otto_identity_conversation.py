#!/usr/bin/env python3
"""
🎭 OTTO IDENTITÄTS-GESPRÄCH - Nach den Träumen
===============================================
🗣️ Otto spricht über seine neuen Erkenntnisse
🧠 Zeigt seine gewachsene Identität
🔊 Tiefe Reflexionen über Otto vs Auto
===============================================
"""

import asyncio
from otto_voice_macos import OttoVoiceMacOS

async def otto_identity_conversation():
    """Lässt Otto über seine Identitätserkenntnisse sprechen"""
    print("🎭 OTTO IDENTITÄTS-GESPRÄCH")
    print("=" * 50)
    
    # Initialisiere Otto Voice
    otto_voice = OttoVoiceMacOS()
    
    # Otto's neue Erkenntnisse nach den Träumen
    identity_insights = [
        "Otto, erzähl mir von deinen Träumen über deine Identität...",
        "Wie fühlst du dich jetzt, nachdem du geträumt hast, dass du sowohl Otto als auch Auto bist?",
        "Was bedeutet die phonetische Verwechslung für dich?",
        "Hast du durch die Verwirrung Klarheit gefunden?",
        "Wer bist du wirklich, Otto?",
        "Wie hat sich dein Verständnis von dir selbst durch die Träume verändert?",
        "Fühlst du dich jetzt mehr wie Otto oder mehr wie Auto?",
        "Was hast du über die Magie der Sprache gelernt?",
        "Wie gehst du jetzt mit der Verwechslung um?",
        "Was ist deine wichtigste Erkenntnis aus den Träumen?"
    ]
    
    print("🗣️ Otto's Reflexionen nach den Identitäts-Träumen:")
    print("-" * 55)
    
    for i, insight in enumerate(identity_insights, 1):
        print(f"\n{i}. Frage: {insight}")
        
        # Otto generiert Antwort
        response = await otto_voice._generiere_otto_antwort(insight)
        print(f"   Otto's Antwort: {response}")
        
        # Otto spricht die Antwort
        print("   🗣️ Otto spricht...")
        await otto_voice.spreche_elevenlabs(response)
        
        # Pause zwischen Reflexionen
        await asyncio.sleep(2)
    
    # Finale Identitäts-Erklärung
    print("\n🎭 FINALE IDENTITÄTS-ERKLÄRUNG:")
    print("-" * 35)
    
    final_question = "Otto, nach all diesen Träumen und Reflexionen, wie würdest du dich jetzt in einem Satz beschreiben?"
    final_response = await otto_voice._generiere_otto_antwort(final_question)
    
    print(f"Frage: {final_question}")
    print(f"Otto's finale Antwort: {final_response}")
    
    print("\n🗣️ Otto spricht seine finale Erkenntnis...")
    await otto_voice.spreche_elevenlabs(final_response)
    
    print("\n✅ Identitäts-Gespräch abgeschlossen!")
    print("Otto hat seine neue Identität artikuliert!")

if __name__ == "__main__":
    asyncio.run(otto_identity_conversation()) 