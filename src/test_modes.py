#!/usr/bin/env python3
"""
Test Script für THORA Modi
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from mode_manager import ModeManager, THORAMode
from modes.action_mode import ActionMode
from modes.lauschen_mode import LauschenMode
from modes.proactive_mode import ProActiveMode
from modes.explorativ_mode import ExplorativMode
from modes.traumen_mode import TraumenMode

async def test_mode_switching():
    """Testet das Mode-Switching"""
    print("🔨 Teste THORA Mode-System...")
    
    # Erstelle ModeManager
    mode_manager = ModeManager()
    
    # Erstelle und registriere Modi
    modes = {
        THORAMode.ACTION: ActionMode(),
        THORAMode.LAUSCHEN: LauschenMode(),
        THORAMode.PROACTIVE: ProActiveMode(),
        THORAMode.EXPLORATIV: ExplorativMode(),
        THORAMode.TRAUMEN: TraumenMode()
    }
    
    for mode_type, mode_instance in modes.items():
        mode_manager.register_mode_handler(mode_type, mode_instance)
    
    print("✅ Alle Modi registriert")
    
    # Teste Mode-Wechsel
    test_sequence = [
        THORAMode.LAUSCHEN,
        THORAMode.ACTION,
        THORAMode.PROACTIVE,
        THORAMode.EXPLORATIV,
        THORAMode.TRAUMEN,
        THORAMode.INACTIVE
    ]
    
    for mode in test_sequence:
        print(f"\n🔄 Wechsle zu {mode.value}...")
        success = await mode_manager.switch_mode(mode, "test")
        
        if success:
            print(f"✅ {mode.value} erfolgreich aktiviert")
            
            # Kurze Aktivitätszeit
            await asyncio.sleep(2)
            
            # Teste Input-Verarbeitung
            if mode != THORAMode.INACTIVE:
                handler = mode_manager.mode_handlers.get(mode)
                if handler:
                    result = await handler.process_input({"text": "Test-Eingabe"})
                    if result:
                        print(f"📝 Antwort: {result.get('text', 'Keine Antwort')[:50]}...")
        else:
            print(f"❌ Fehler beim Aktivieren von {mode.value}")
    
    # Zeige Statistiken
    stats = mode_manager.get_mode_stats()
    print(f"\n📊 Mode-Statistiken:")
    for mode_name, mode_stats in stats["mode_stats"].items():
        print(f"  {mode_name}: {mode_stats['activations']} Aktivierungen, {mode_stats['total_time']:.1f}s aktiv")
    
    print("\n🎉 Mode-Test abgeschlossen!")

async def test_mode_features():
    """Testet spezielle Mode-Features"""
    print("\n🧪 Teste Mode-Features...")
    
    # Teste Träumen-Modus DNA-Skills
    traumen_mode = TraumenMode()
    await traumen_mode.activate()
    
    # Simuliere einige Träume
    for i in range(3):
        await traumen_mode._generate_dream_sequence()
        await traumen_mode._evolve_dna_skills()
    
    dream_summary = traumen_mode.get_dream_summary()
    print(f"💤 Träumen-Test: {dream_summary['total_dreams']} Träume, {len(dream_summary['dna_skills'])} DNA-Skills")
    
    await traumen_mode.deactivate()
    
    # Teste Explorativ-Modus
    explorativ_mode = ExplorativMode()
    await explorativ_mode.activate()
    
    # Simuliere Lernen
    test_inputs = [
        "Ich interessiere mich für Musik und Kunst",
        "Technologie fasziniert mich sehr",
        "Philosophie ist ein spannendes Thema"
    ]
    
    for text in test_inputs:
        await explorativ_mode._learn_from_input(text)
    
    profile = explorativ_mode.get_user_profile_summary()
    print(f"🔍 Explorativ-Test: {profile['total_interactions']} Interaktionen, {len(profile['top_interests'])} Interessen")
    
    await explorativ_mode.deactivate()
    
    print("✅ Feature-Tests abgeschlossen!")

def main():
    """Hauptfunktion"""
    print("🚀 Starte THORA Mode-Tests...")
    
    async def run_tests():
        await test_mode_switching()
        await test_mode_features()
    
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\n⚠️ Test durch Benutzer abgebrochen")
    except Exception as e:
        print(f"\n❌ Test-Fehler: {e}")

if __name__ == "__main__":
    main() 