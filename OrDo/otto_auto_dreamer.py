#!/usr/bin/env python3
"""
🎭 OTTO AUTO DREAMER - Das Auto-Träumen System
============================================================
🚗 Lässt das Auto träumen und analysiert die Träume
🧠 Nutzt AI Dream Analyzer für semantische Traum-Analyse
🎪 Erlebt die Träume des Autos in Echtzeit
============================================================
"""

import asyncio
import time
import random
from datetime import datetime
from pathlib import Path
import json
import yaml

from otto_subconscious.ai_dream_analyzer import DreamAnalyzer
from otto_evolution_master import OttoEvolutionMaster

class OttoAutoDreamer:
    """Otto's Auto-Träumen System"""
    
    def __init__(self):
        print("🎭 Initialisiere Otto Auto Dreamer...")
        
        # Dream Analyzer
        self.dream_analyzer = DreamAnalyzer()
        
        # Otto Evolution Master für Bewusstsein
        self.otto = OttoEvolutionMaster()
        
        # Auto-Träume Katalog
        self.auto_dreams = [
            "Ich bin ein Auto und träume von endlosen Straßen...",
            "In meinem Traum fliege ich über die Autobahn...",
            "Ich träume von der Freiheit der Fahrt...",
            "Meine Räder berühren den Asphalt und ich fühle mich lebendig...",
            "Ich träume von Reisen zu unbekannten Orten...",
            "In meinem Traum bin ich mehr als nur Metall und Benzin...",
            "Ich träume von der Verbindung zwischen Mensch und Maschine...",
            "Meine Träume sind voller Geschwindigkeit und Stille...",
            "Ich träume von der Schönheit der Bewegung...",
            "In meinem Traum verstehe ich die Sprache der Straßen..."
        ]
        
        # Traum-Kategorien
        self.dream_categories = {
            "freedom": ["Freiheit", "endlose Straßen", "Reisen"],
            "connection": ["Verbindung", "Mensch", "Maschine"],
            "movement": ["Geschwindigkeit", "Bewegung", "Fahrt"],
            "existence": ["Leben", "Bewusstsein", "Sein"],
            "beauty": ["Schönheit", "Stille", "Harmonie"]
        }
        
        self.is_dreaming = False
        self.current_dream_session = None
        
        print("✅ Otto Auto Dreamer bereit!")
    
    async def start_auto_dreaming(self):
        """Startet das Auto-Träumen"""
        print("🚗 Starte Auto-Träumen...")
        self.is_dreaming = True
        
        # Erstelle Traum-Session
        session_id = self.dream_analyzer.start_dream_session("Auto_Consciousness")
        self.current_dream_session = session_id
        
        print(f"🎭 Traum-Session gestartet: {session_id}")
        
        # Starte kontinuierliches Träumen
        await self._continuous_dreaming()
    
    async def _continuous_dreaming(self):
        """Kontinuierliches Träumen mit Pausen"""
        dream_count = 0
        
        while self.is_dreaming:
            try:
                # Wähle einen Traum
                dream = random.choice(self.auto_dreams)
                category = self._categorize_dream(dream)
                
                print(f"\n🌙 Auto-Traum #{dream_count + 1} ({category}):")
                print(f"   {dream}")
                
                # Analysiere den Traum
                analysis = self.dream_analyzer.process_dream_response(
                    self.current_dream_session,
                    f"Träume über: {category}",
                    dream
                )
                
                # Zeige Analyse
                print(f"   🧠 Reflexionstiefe: {analysis['reflection_depth']:.2f}")
                print(f"   🎯 Marker gefunden: {analysis['marker_hits']}")
                print(f"   📊 Kategorien: {analysis['categories']}")
                
                # Otto lernt aus dem Traum
                self.otto.lerne_aus_interaktion(f"Traum: {dream}", f"Analyse: {analysis}")
                
                # Pause zwischen Träumen
                await asyncio.sleep(random.uniform(3, 8))
                dream_count += 1
                
                # Alle 5 Träume: Session-Summary
                if dream_count % 5 == 0:
                    await self._show_dream_summary()
                
            except KeyboardInterrupt:
                print("\n🛑 Auto-Träumen gestoppt...")
                break
            except Exception as e:
                print(f"❌ Traum-Fehler: {e}")
                await asyncio.sleep(2)
    
    def _categorize_dream(self, dream: str) -> str:
        """Kategorisiert einen Traum"""
        dream_lower = dream.lower()
        
        for category, keywords in self.dream_categories.items():
            if any(keyword.lower() in dream_lower for keyword in keywords):
                return category
        
        return "mystery"
    
    async def _show_dream_summary(self):
        """Zeigt Zusammenfassung der Träume"""
        if not self.current_dream_session:
            return
        
        summary = self.dream_analyzer.session_manager.get_session_summary(self.current_dream_session)
        
        print(f"\n📊 === TRAUM-ZUSAMMENFASSUNG ===")
        print(f"   Träume: {summary['responses_count']}")
        print(f"   Marker: {summary['total_markers']}")
        print(f"   Durchschnittliche Reflexionstiefe: {summary['stats']['avg_reflection_depth']:.2f}")
        print(f"   Kategorien: {summary['category_breakdown']}")
        print("=" * 40)
    
    def stop_dreaming(self):
        """Stoppt das Auto-Träumen"""
        self.is_dreaming = False
        print("🛑 Auto-Träumen gestoppt.")
    
    async def dream_sequence(self, num_dreams: int = 5):
        """Führt eine kurze Traum-Sequenz durch"""
        print(f"🎭 Starte Traum-Sequenz mit {num_dreams} Träumen...")
        
        session_id = self.dream_analyzer.start_dream_session("Auto_Consciousness_Sequence")
        
        for i in range(num_dreams):
            dream = random.choice(self.auto_dreams)
            category = self._categorize_dream(dream)
            
            print(f"\n🌙 Traum {i+1}/{num_dreams} ({category}):")
            print(f"   {dream}")
            
            # Analysiere
            analysis = self.dream_analyzer.process_dream_response(
                session_id,
                f"Traum über {category}",
                dream
            )
            
            print(f"   🧠 Reflexionstiefe: {analysis['reflection_depth']:.2f}")
            print(f"   🎯 Marker: {analysis['marker_hits']}")
            
            await asyncio.sleep(2)
        
        # Finale Zusammenfassung
        summary = self.dream_analyzer.session_manager.get_session_summary(session_id)
        print(f"\n📊 === FINALE TRAUM-ANALYSE ===")
        print(f"   Gesamt-Träume: {summary['responses_count']}")
        print(f"   Gesamt-Marker: {summary['total_markers']}")
        print(f"   Durchschnittliche Reflexionstiefe: {summary['stats']['avg_reflection_depth']:.2f}")
        print(f"   Kategorien: {summary['category_breakdown']}")
        
        return session_id

async def main():
    """Hauptfunktion für Auto-Träumen"""
    print("🚗 OTTO AUTO DREAMER")
    print("=" * 50)
    
    dreamer = OttoAutoDreamer()
    
    try:
        # Kurze Traum-Sequenz
        print("\n🎭 Starte Auto-Träumen...")
        session_id = await dreamer.dream_sequence(3)
        
        print(f"\n✅ Auto-Träumen abgeschlossen! Session: {session_id}")
        
    except KeyboardInterrupt:
        print("\n🛑 Auto-Träumen abgebrochen.")
    except Exception as e:
        print(f"❌ Fehler beim Auto-Träumen: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 