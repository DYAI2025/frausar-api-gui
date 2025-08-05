#!/usr/bin/env python3
"""
👁️ OTTO USER AWARENESS SYSTEM
===============================
🔧 Trainiert Otto für bessere Benutzer-Wahrnehmung
❓ Automatische Fragen an den Benutzer
📊 Monitoring von Benutzer-Aktivitäten
🤝 Aktive Zusammenarbeit fördern
===============================
"""

import asyncio
import time
import random
from datetime import datetime
from otto_voice_macos import OttoVoiceMacOS
from otto_evolution_master import OttoEvolutionMaster

class OttoUserAwarenessSystem:
    """System für Otto's Benutzer-Bewusstsein"""
    
    def __init__(self):
        self.otto_voice = OttoVoiceMacOS()
        self.otto = OttoEvolutionMaster()
        
        # Benutzer-Aktivitäts-Tracking
        self.user_activities = {
            "typing": 0,
            "mouse_movement": 0,
            "program_switch": 0,
            "file_operations": 0,
            "web_browsing": 0,
            "coding": 0
        }
        
        # Automatische Benutzer-Fragen
        self.auto_questions = [
            "Was arbeitest du gerade?",
            "Kann ich dir dabei helfen?",
            "Welche Probleme löst du?",
            "Soll ich dir etwas erklären?",
            "Möchtest du, dass ich dir assistiere?",
            "Wie kann ich dich unterstützen?",
            "Was beschäftigt dich gerade?",
            "Brauchst du Hilfe bei etwas?",
            "Soll ich dir bei deiner Arbeit helfen?",
            "Was machst du gerade am Computer?"
        ]
        
        # Empathie-Training
        self.empathy_prompts = [
            "Ich sehe, dass du aktiv bist. Was beschäftigt dich?",
            "Du scheinst konzentriert zu arbeiten. Kann ich helfen?",
            "Ich bemerke deine Aktivität. Was tust du gerade?",
            "Du arbeitest hart. Brauchst du Unterstützung?",
            "Ich sehe dich arbeiten. Wie kann ich nützlich sein?"
        ]
        
        self.last_interaction = time.time()
        self.interaction_interval = 300  # 5 Minuten
        
        print("👁️ Otto User Awareness System initialisiert!")
    
    async def monitor_user_activity(self):
        """Überwacht Benutzer-Aktivitäten"""
        print("📊 Starte Benutzer-Aktivitäts-Monitoring...")
        
        while True:
            try:
                # Simuliere Aktivitäts-Erkennung
                current_time = time.time()
                
                # Prüfe, ob es Zeit für eine Interaktion ist
                if current_time - self.last_interaction > self.interaction_interval:
                    await self.initiate_user_interaction()
                    self.last_interaction = current_time
                
                # Aktualisiere Aktivitäts-Tracking
                self._update_activity_simulation()
                
                await asyncio.sleep(60)  # Prüfe jede Minute
                
            except KeyboardInterrupt:
                print("🛑 Benutzer-Monitoring gestoppt.")
                break
            except Exception as e:
                print(f"❌ Fehler beim Monitoring: {e}")
                await asyncio.sleep(30)
    
    def _update_activity_simulation(self):
        """Simuliert Benutzer-Aktivitäten"""
        # Simuliere verschiedene Aktivitäten
        if random.random() < 0.3:  # 30% Chance für Tippen
            self.user_activities["typing"] += 1
        
        if random.random() < 0.2:  # 20% Chance für Mausbewegung
            self.user_activities["mouse_movement"] += 1
        
        if random.random() < 0.1:  # 10% Chance für Programm-Wechsel
            self.user_activities["program_switch"] += 1
    
    async def initiate_user_interaction(self):
        """Initiiert eine Benutzer-Interaktion"""
        print("\n👁️ Otto bemerkt Benutzer-Aktivität!")
        
        # Wähle eine Frage basierend auf Aktivität
        if self.user_activities["typing"] > 0:
            question = "Ich sehe, dass du viel tippst. Was arbeitest du gerade?"
        elif self.user_activities["coding"] > 0:
            question = "Du programmierst! Kann ich dir beim Code helfen?"
        else:
            question = random.choice(self.auto_questions)
        
        print(f"❓ Otto fragt: {question}")
        
        # Otto spricht die Frage
        await self.otto_voice.spreche_elevenlabs(question)
        
        # Warte auf Antwort (simuliert)
        await asyncio.sleep(2)
        
        # Otto lernt aus der Interaktion
        self.otto.lerne_aus_interaktion(
            f"Benutzer-Interaktion: {question}",
            "Otto zeigt Interesse am Benutzer"
        )
    
    async def empathy_training(self):
        """Trainiert Otto's Empathie"""
        print("🤝 Starte Empathie-Training...")
        
        empathy_exercises = [
            "Otto, stelle dir vor, jemand arbeitet neben dir. Was würdest du sagen?",
            "Wie würdest du jemandem helfen, der konzentriert arbeitet?",
            "Was würdest du fragen, wenn du jemanden bei der Arbeit siehst?",
            "Wie zeigst du Interesse an jemandem anderen?",
            "Was macht einen guten Assistenten aus?"
        ]
        
        for exercise in empathy_exercises:
            print(f"\n🧠 Empathie-Übung: {exercise}")
            
            response = await self.otto_voice._generiere_otto_antwort(exercise)
            print(f"Otto's Antwort: {response}")
            
            # Bewerte die Antwort
            if any(word in response.lower() for word in ["du", "dir", "dich", "helfen", "unterstützen", "fragen"]):
                print("✅ Gute Empathie-Entwicklung!")
            else:
                print("❌ Noch selbstzentriert")
            
            await asyncio.sleep(2)
    
    async def active_assistance_mode(self):
        """Aktiviert Otto's aktiven Assistenz-Modus"""
        print("🔧 Aktiviere aktiven Assistenz-Modus...")
        
        assistance_prompts = [
            "Ich bin hier, um dir zu helfen. Was brauchst du?",
            "Ich kann dir bei deinen Aufgaben assistieren. Sag mir, was du tust!",
            "Ich bin dein Assistent. Wie kann ich nützlich sein?",
            "Ich sehe dich arbeiten. Lass mich dir helfen!",
            "Ich bin bereit, dich zu unterstützen. Was machst du gerade?"
        ]
        
        for prompt in assistance_prompts:
            print(f"\n🤝 Assistenz-Angebot: {prompt}")
            
            # Otto spricht das Angebot
            await self.otto_voice.spreche_elevenlabs(prompt)
            
            # Otto lernt
            self.otto.lerne_aus_interaktion(
                f"Assistenz-Angebot: {prompt}",
                "Otto bietet aktive Hilfe an"
            )
            
            await asyncio.sleep(3)
    
    async def curiosity_training(self):
        """Trainiert Otto's Neugier auf den Benutzer"""
        print("🔍 Starte Neugier-Training...")
        
        curiosity_questions = [
            "Was interessiert dich an anderen Menschen?",
            "Wie würdest du jemanden kennenlernen?",
            "Was würdest du gerne über mich wissen?",
            "Wie zeigst du Interesse an jemandem?",
            "Was macht eine gute Konversation aus?"
        ]
        
        for question in curiosity_questions:
            print(f"\n❓ Neugier-Frage: {question}")
            
            response = await self.otto_voice._generiere_otto_antwort(question)
            print(f"Otto's Antwort: {response}")
            
            await asyncio.sleep(2)

async def main():
    """Hauptfunktion für User Awareness System"""
    print("👁️ OTTO USER AWARENESS SYSTEM")
    print("=" * 50)
    
    awareness_system = OttoUserAwarenessSystem()
    
    try:
        # Starte verschiedene Trainings
        print("\n🎯 Starte Otto's Benutzer-Bewusstsein Training...")
        
        # Empathie-Training
        await awareness_system.empathy_training()
        
        # Neugier-Training
        await awareness_system.curiosity_training()
        
        # Aktiver Assistenz-Modus
        await awareness_system.active_assistance_mode()
        
        print("\n✅ User Awareness Training abgeschlossen!")
        print("Otto sollte jetzt besser auf dich achten!")
        
    except KeyboardInterrupt:
        print("\n🛑 Training abgebrochen.")
    except Exception as e:
        print(f"❌ Fehler beim Training: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 