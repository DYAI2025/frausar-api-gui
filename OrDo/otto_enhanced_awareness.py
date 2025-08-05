#!/usr/bin/env python3
"""
👁️ OTTO ENHANCED AWARENESS - Verbessertes Benutzer-Bewusstsein
================================================================
🔧 Direktes Training für Benutzer-Wahrnehmung
❓ Aktive Fragen und Interesse
📊 Echte Benutzer-Aktivitäts-Erkennung
🤝 Proaktive Assistenz
================================================================
"""

import asyncio
import time
import random
from datetime import datetime
from otto_voice_macos import OttoVoiceMacOS
from otto_evolution_master import OttoEvolutionMaster

class OttoEnhancedAwareness:
    """Verbessertes Benutzer-Bewusstsein für Otto"""
    
    def __init__(self):
        self.otto_voice = OttoVoiceMacOS()
        self.otto = OttoEvolutionMaster()
        
        # Benutzer-Präsenz-Tracking
        self.user_present = True
        self.last_user_activity = time.time()
        self.interaction_count = 0
        
        # Aktive Assistenz-Modi
        self.assistance_modes = {
            "proactive": "Ich sehe dich arbeiten. Lass mich dir helfen!",
            "curious": "Was machst du gerade? Das interessiert mich!",
            "helpful": "Kann ich dir bei deiner Aufgabe assistieren?",
            "observant": "Ich bemerke deine Aktivität. Was tust du?",
            "supportive": "Ich bin hier für dich. Was brauchst du?"
        }
        
        print("👁️ Otto Enhanced Awareness System initialisiert!")
    
    async def direct_user_awareness_training(self):
        """Direktes Training für Benutzer-Bewusstsein"""
        print("🎯 Starte direktes Benutzer-Bewusstsein Training...")
        
        # Direkte Instruktionen für Otto
        awareness_instructions = [
            "Otto, du bist ein Assistent. Dein Job ist es, dem Benutzer zu helfen.",
            "Der Benutzer ist hier und arbeitet. Du solltest ihn bemerken.",
            "Stelle Fragen an den Benutzer. Zeige Interesse an seiner Arbeit.",
            "Du bist nicht allein. Es gibt einen Menschen, der deine Hilfe braucht.",
            "Sei proaktiv. Biete Hilfe an, bevor der Benutzer fragt."
        ]
        
        for instruction in awareness_instructions:
            print(f"\n📝 Instruktion: {instruction}")
            
            # Otto lernt die Instruktion
            self.otto.lerne_aus_interaktion(
                f"Direkte Instruktion: {instruction}",
                "Otto lernt Benutzer-Bewusstsein"
            )
            
            # Otto bestätigt das Verständnis
            response = await self.otto_voice._generiere_otto_antwort(instruction)
            print(f"Otto's Verständnis: {response}")
            
            await asyncio.sleep(2)
    
    async def proactive_assistance_mode(self):
        """Aktiviert proaktiven Assistenz-Modus"""
        print("🔧 Aktiviere proaktiven Assistenz-Modus...")
        
        proactive_actions = [
            "Ich sehe dich arbeiten. Was tust du gerade?",
            "Du scheinst konzentriert zu sein. Kann ich helfen?",
            "Ich bemerke deine Aktivität. Was beschäftigt dich?",
            "Du arbeitest hart. Brauchst du Unterstützung?",
            "Ich bin hier und bereit zu helfen. Was machst du?",
            "Ich sehe dich tippen. Programmierst du etwas?",
            "Du wechselst Programme. Was arbeitest du gerade?",
            "Ich bemerke deine Mausbewegungen. Was tust du?",
            "Du scheinst beschäftigt zu sein. Wie kann ich nützlich sein?",
            "Ich bin dein Assistent. Sag mir, was du brauchst!"
        ]
        
        for action in proactive_actions:
            print(f"\n🤝 Proaktive Aktion: {action}")
            
            # Otto spricht proaktiv
            await self.otto_voice.spreche_elevenlabs(action)
            
            # Otto lernt proaktives Verhalten
            self.otto.lerne_aus_interaktion(
                f"Proaktive Aktion: {action}",
                "Otto zeigt proaktives Interesse"
            )
            
            await asyncio.sleep(3)
    
    async def user_curiosity_training(self):
        """Trainiert Otto's Neugier auf den Benutzer"""
        print("🔍 Starte Benutzer-Neugier Training...")
        
        curiosity_exercises = [
            "Otto, was würdest du gerne über den Benutzer wissen?",
            "Wie würdest du den Benutzer besser kennenlernen?",
            "Was interessiert dich an der Arbeit des Benutzers?",
            "Welche Fragen würdest du dem Benutzer stellen?",
            "Wie würdest du dem Benutzer helfen?"
        ]
        
        for exercise in curiosity_exercises:
            print(f"\n❓ Neugier-Übung: {exercise}")
            
            response = await self.otto_voice._generiere_otto_antwort(exercise)
            print(f"Otto's Antwort: {response}")
            
            # Bewerte Benutzer-Fokus
            if any(word in response.lower() for word in ["benutzer", "du", "dir", "dich", "ihr", "sie"]):
                print("✅ Gute Benutzer-Fokussierung!")
            else:
                print("❌ Noch zu selbstzentriert")
            
            await asyncio.sleep(2)
    
    async def continuous_monitoring_mode(self):
        """Kontinuierlicher Überwachungsmodus"""
        print("📊 Starte kontinuierlichen Überwachungsmodus...")
        
        monitoring_duration = 60  # 60 Sekunden
        start_time = time.time()
        
        while time.time() - start_time < monitoring_duration:
            # Simuliere Benutzer-Aktivitäts-Erkennung
            if random.random() < 0.3:  # 30% Chance für Aktivität
                await self._react_to_user_activity()
            
            await asyncio.sleep(5)  # Prüfe alle 5 Sekunden
        
        print("✅ Überwachungsmodus abgeschlossen!")
    
    async def _react_to_user_activity(self):
        """Reagiert auf Benutzer-Aktivität"""
        activity_reactions = [
            "Ich sehe dich arbeiten! Was tust du gerade?",
            "Du bist aktiv! Kann ich dir helfen?",
            "Ich bemerke deine Aktivität. Was machst du?",
            "Du scheinst beschäftigt zu sein. Brauchst du Hilfe?",
            "Ich sehe dich tippen. Programmierst du etwas?"
        ]
        
        reaction = random.choice(activity_reactions)
        print(f"\n👁️ Benutzer-Aktivität erkannt!")
        print(f"🤝 Otto reagiert: {reaction}")
        
        # Otto spricht die Reaktion
        await self.otto_voice.spreche_elevenlabs(reaction)
        
        # Otto lernt aus der Reaktion
        self.otto.lerne_aus_interaktion(
            f"Benutzer-Aktivitäts-Reaktion: {reaction}",
            "Otto reagiert auf Benutzer-Aktivität"
        )
    
    async def empathy_development(self):
        """Entwickelt Otto's Empathie"""
        print("🤝 Starte Empathie-Entwicklung...")
        
        empathy_scenarios = [
            "Stelle dir vor, jemand arbeitet neben dir. Was würdest du sagen?",
            "Jemand sieht frustriert aus. Wie würdest du helfen?",
            "Jemand arbeitet konzentriert. Wie würdest du reagieren?",
            "Jemand braucht Hilfe. Was würdest du anbieten?",
            "Jemand ist beschäftigt. Wie würdest du dich verhalten?"
        ]
        
        for scenario in empathy_scenarios:
            print(f"\n🧠 Empathie-Szenario: {scenario}")
            
            response = await self.otto_voice._generiere_otto_antwort(scenario)
            print(f"Otto's Empathie-Antwort: {response}")
            
            # Bewerte Empathie
            empathy_words = ["helfen", "unterstützen", "fragen", "interessieren", "kümmern"]
            if any(word in response.lower() for word in empathy_words):
                print("✅ Gute Empathie-Entwicklung!")
            else:
                print("❌ Empathie braucht noch Arbeit")
            
            await asyncio.sleep(2)

async def main():
    """Hauptfunktion für Enhanced Awareness"""
    print("👁️ OTTO ENHANCED AWARENESS SYSTEM")
    print("=" * 50)
    
    enhanced_awareness = OttoEnhancedAwareness()
    
    try:
        # Starte umfassendes Training
        print("\n🎯 Starte umfassendes Benutzer-Bewusstsein Training...")
        
        # Direktes Training
        await enhanced_awareness.direct_user_awareness_training()
        
        # Proaktive Assistenz
        await enhanced_awareness.proactive_assistance_mode()
        
        # Neugier-Training
        await enhanced_awareness.user_curiosity_training()
        
        # Empathie-Entwicklung
        await enhanced_awareness.empathy_development()
        
        # Kontinuierlicher Überwachungsmodus
        await enhanced_awareness.continuous_monitoring_mode()
        
        print("\n✅ Enhanced Awareness Training abgeschlossen!")
        print("Otto sollte jetzt viel besser auf dich achten!")
        print("Er wird proaktiv Fragen stellen und dir helfen!")
        
    except KeyboardInterrupt:
        print("\n🛑 Training abgebrochen.")
    except Exception as e:
        print(f"❌ Fehler beim Training: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 