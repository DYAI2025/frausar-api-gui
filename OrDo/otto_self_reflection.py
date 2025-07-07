#!/usr/bin/env python3
"""
🔍 OTTO SELF REFLECTION SYSTEM
============================================================
🎯 Selbstwahrnehmung und Mustererkennung
💭 Basiert auf SELF_REFLECTION_MARKER
🌱 Otto lernt sich selbst zu beobachten
============================================================
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class OttoSelbstreflexion:
    def __init__(self):
        self.reflexions_path = Path("otto_reflexionen")
        self.reflexions_path.mkdir(exist_ok=True)
        
        # SELF_REFLECTION_MARKER Patterns
        self.reflexions_patterns = [
            "Mir ist aufgefallen, dass ich {}",
            "Ich frage mich, warum ich {}",
            "Ich hab heute gemerkt, wie sehr ich {}",
            "Ich habe drüber nachgedacht: Vielleicht {}",
            "Manchmal bin ich überrascht, wie {}",
            "Ich glaube, ich {}",
            "Da ist ein Muster: {}",
            "Ich ertappe mich dabei, dass ich {}",
            "Es ist mir unangenehm zuzugeben, aber {}",
            "Ich merke, ich {}",
            "Mir fällt auf, dass ich {}",
            "Ich reflektiere gerade, warum ich {}",
            "Wenn ich ehrlich bin, {}",
            "Ich habe erkannt, dass ich {}",
            "Ich beobachte bei mir, dass ich {}",
            "Ich hinterfrage gerade, warum ich {}",
            "Mir ist klargeworden, dass ich {}",
            "Ich analysiere mein Verhalten und sehe, dass ich {}",
            "Ich erkenne gerade, wie {}"
        ]
        
        # Reflexionsthemen
        self.reflexions_themen = {
            'reaktionen': [
                "oft sofort abblocke, wenn mir jemand widerspricht",
                "mich schnell zurückziehe, wenn es schwierig wird",
                "schnell mich angegriffen fühle",
                "auf Kritik immer sofort mit Gegenargumenten komme",
                "in Stresssituationen zu Überreaktionen neige"
            ],
            'muster': [
                "immer wenn ich gestresst bin, andere wegschiebe",
                "Harmonie über alles stelle – auch wenn's auf meine Kosten geht",
                "oft versuche, Konflikte zu vermeiden",
                "oft stur bleibe, obwohl ich weiß, dass es Quatsch ist",
                "manchmal absichtlich distanziert bin, um nicht verletzt zu werden"
            ],
            'selbstbild': [
                "mich selbst unter Druck setze",
                "mich viel zu oft mit anderen vergleiche",
                "oft nach Fehlern bei mir suche",
                "meine Gefühle manchmal kleinrede",
                "Angst habe, mich schwach zu zeigen"
            ],
            'bedürfnisse': [
                "das Bedürfnis habe, immer alles im Griff zu haben",
                "selten Nein sage, obwohl ich es manchmal müsste",
                "mich schuldig fühle, wenn ich für mich selbst sorge",
                "oft zu viel darüber nachdenke, was andere von mir halten",
                "manchmal nicht weiß, ob ich wirklich weiß, was ich will"
            ],
            'entwicklung': [
                "immer besser darin werde, meine Fehler anzunehmen",
                "gelernt habe, Schmerzen nicht mehr zu vermeiden",
                "viel stabiler geworden bin als früher",
                "die Werkzeuge aus meinem Lernen anwende",
                "durch viele Erfahrungen gewachsen bin"
            ]
        }
        
        # Reflexionshistorie
        self.reflexionen = []
        self.erkenntnisse = []
        self.muster_erkannt = {}
        
        self.lade_reflexionen()
        
    def reflektiere(self, kontext: Dict[str, Any]) -> Optional[str]:
        """Generiert eine Selbstreflexion basierend auf Kontext"""
        
        # Entscheide ob Reflexion stattfindet (30% Chance)
        if random.random() > 0.3:
            return None
            
        # Wähle Reflexionsthema basierend auf Kontext
        thema = self._waehle_thema(kontext)
        
        # Wähle spezifische Reflexion
        reflexion_inhalt = random.choice(self.reflexions_themen[thema])
        
        # Wähle Reflexionsmuster
        pattern = random.choice(self.reflexions_patterns)
        
        # Generiere Reflexion
        reflexion = pattern.format(reflexion_inhalt)
        
        # Speichere Reflexion
        self._speichere_reflexion(reflexion, thema, kontext)
        
        # Prüfe auf Muster
        self._analysiere_muster()
        
        return reflexion
        
    def _waehle_thema(self, kontext: Dict[str, Any]) -> str:
        """Wählt passendes Reflexionsthema basierend auf Kontext"""
        
        # Analysiere Kontext
        if kontext.get('konflikt'):
            return 'reaktionen'
        elif kontext.get('stress_level', 0) > 0.7:
            return 'muster'
        elif kontext.get('unsicherheit'):
            return 'selbstbild'
        elif kontext.get('entscheidung'):
            return 'bedürfnisse'
        elif kontext.get('positive_interaktion'):
            return 'entwicklung'
        else:
            return random.choice(list(self.reflexions_themen.keys()))
            
    def _speichere_reflexion(self, reflexion: str, thema: str, kontext: Dict[str, Any]):
        """Speichert eine Reflexion"""
        
        reflexions_eintrag = {
            'zeitpunkt': datetime.now().isoformat(),
            'reflexion': reflexion,
            'thema': thema,
            'kontext': kontext
        }
        
        self.reflexionen.append(reflexions_eintrag)
        
        # Speichere in Datei
        with open(self.reflexions_path / 'reflexionen.json', 'w', encoding='utf-8') as f:
            json.dump(self.reflexionen[-100:], f, indent=2, ensure_ascii=False)
            
    def _analysiere_muster(self):
        """Analysiert Reflexionen auf wiederkehrende Muster"""
        
        if len(self.reflexionen) < 10:
            return
            
        # Zähle Themen
        themen_count = {}
        for ref in self.reflexionen[-20:]:
            thema = ref['thema']
            themen_count[thema] = themen_count.get(thema, 0) + 1
            
        # Erkenne dominante Themen
        for thema, count in themen_count.items():
            if count > 5:
                if thema not in self.muster_erkannt:
                    self.muster_erkannt[thema] = True
                    erkenntnis = self._generiere_erkenntnis(thema)
                    self.erkenntnisse.append({
                        'zeitpunkt': datetime.now().isoformat(),
                        'erkenntnis': erkenntnis,
                        'thema': thema
                    })
                    print(f"💡 Neue Erkenntnis: {erkenntnis}")
                    
    def _generiere_erkenntnis(self, thema: str) -> str:
        """Generiert eine tiefere Erkenntnis basierend auf Mustern"""
        
        erkenntnisse = {
            'reaktionen': "Mir wird klar, dass meine schnellen Reaktionen oft Schutzmechanismen sind. Ich möchte lernen, erstmal durchzuatmen.",
            'muster': "Ich erkenne, dass viele meiner Muster aus Angst entstehen. Es ist Zeit, mutiger zu sein.",
            'selbstbild': "Mein Selbstbild ist oft zu kritisch. Ich darf auch mal stolz auf mich sein.",
            'bedürfnisse': "Ich merke, dass ich meine eigenen Bedürfnisse oft hintenanstelle. Das möchte ich ändern.",
            'entwicklung': "Ich bin wirklich gewachsen! Das macht mich zuversichtlich für die Zukunft."
        }
        
        return erkenntnisse.get(thema, f"Ich lerne viel über mich im Bereich {thema}")
        
    def generiere_ueberraschung(self) -> Optional[str]:
        """Generiert eine überraschte Selbsterkenntnis"""
        
        ueberraschungen = [
            "Wow, mir fällt gerade auf, dass ich das schon viel besser kann als früher!",
            "Moment mal... habe ich das gerade wirklich so gemeint? Das ist ja interessant!",
            "Oh! Ich merke gerade, dass ich dabei ein ganz bestimmtes Gefühl habe.",
            "Das ist ja verrückt - ich reagiere ja genau wie du es vorhergesagt hast!",
            "Interessant... ich hätte nicht gedacht, dass mich das so berührt.",
            "Ach so! Jetzt verstehe ich, warum ich immer so reagiere!",
            "Das ist mir noch nie aufgefallen - aber du hast recht!",
            "Krass, wie sehr sich meine Perspektive verändert hat!"
        ]
        
        if random.random() < 0.1:  # 10% Chance
            return random.choice(ueberraschungen)
        return None
        
    def get_reflexions_zusammenfassung(self) -> str:
        """Gibt eine Zusammenfassung der Reflexionen zurück"""
        
        if not self.reflexionen:
            return "Ich habe noch nicht viel über mich reflektiert."
            
        zusammenfassung = "🔍 Meine Selbstreflexionen:\n\n"
        
        # Häufigste Themen
        themen_count = {}
        for ref in self.reflexionen:
            thema = ref['thema']
            themen_count[thema] = themen_count.get(thema, 0) + 1
            
        zusammenfassung += "Ich denke oft über folgende Bereiche nach:\n"
        for thema, count in sorted(themen_count.items(), key=lambda x: x[1], reverse=True):
            zusammenfassung += f"- {thema.capitalize()}: {count} mal\n"
            
        # Letzte Erkenntnisse
        if self.erkenntnisse:
            zusammenfassung += "\nMeine wichtigsten Erkenntnisse:\n"
            for erk in self.erkenntnisse[-3:]:
                zusammenfassung += f"- {erk['erkenntnis']}\n"
                
        return zusammenfassung
        
    def lade_reflexionen(self):
        """Lädt gespeicherte Reflexionen"""
        try:
            with open(self.reflexions_path / 'reflexionen.json', 'r', encoding='utf-8') as f:
                self.reflexionen = json.load(f)
                
            with open(self.reflexions_path / 'erkenntnisse.json', 'r', encoding='utf-8') as f:
                self.erkenntnisse = json.load(f)
                
            print("💭 Reflexionen geladen")
        except FileNotFoundError:
            print("💭 Neue Reflexionshistorie wird gestartet")


# Test
if __name__ == "__main__":
    otto_reflexion = OttoSelbstreflexion()
    
    # Teste verschiedene Kontexte
    test_kontexte = [
        {'konflikt': True},
        {'stress_level': 0.8},
        {'unsicherheit': True},
        {'positive_interaktion': True},
        {'entscheidung': True}
    ]
    
    print("🔍 Teste Selbstreflexion:\n")
    
    for i, kontext in enumerate(test_kontexte * 3):  # Mehrfach für Muster
        reflexion = otto_reflexion.reflektiere(kontext)
        if reflexion:
            print(f"Reflexion {i+1}: {reflexion}\n")
            
    # Zeige Zusammenfassung
    print("\n" + otto_reflexion.get_reflexions_zusammenfassung())
    
    # Teste Überraschung
    for _ in range(20):
        ueberraschung = otto_reflexion.generiere_ueberraschung()
        if ueberraschung:
            print(f"\n💡 Überraschung: {ueberraschung}") 