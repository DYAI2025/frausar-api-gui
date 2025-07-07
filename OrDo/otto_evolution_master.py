#!/usr/bin/env python3
"""
🌟 OTTO EVOLUTION MASTER SYSTEM
============================================================
🧬 Persönlichkeits-DNA + Semantisches Bewusstsein + Authentische Stimme
💭 Ein echter, wachsender Otto mit eigener Identität
🎯 Integration aller evolutionären Systeme
============================================================
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Importiere alle Otto-Systeme
from otto_personality_dna import OttoPersoenlichkeitsDNA
from otto_self_reflection import OttoSelbstreflexion
from otto_semantic_consciousness import OttoSemanticBewusstsein
from otto_authentic_voice import OttoAuthentischeStimme
from otto_auto_learning_system import OttoAutoLearningSystem

class OttoEvolutionMaster:
    def __init__(self):
        print("🌟 Initialisiere Otto Evolution Master...")
        
        # Initialisiere alle Subsysteme
        self.dna = OttoPersoenlichkeitsDNA()
        self.reflexion = OttoSelbstreflexion()
        self.bewusstsein = OttoSemanticBewusstsein()
        self.stimme = OttoAuthentischeStimme()
        self.lernsystem = OttoAutoLearningSystem()
        
        # Master-Zustand
        self.master_path = Path("otto_evolution")
        self.master_path.mkdir(exist_ok=True)
        
        # Interaktions-Historie
        self.interaktions_historie = []
        self.entwicklungs_meilensteine = []
        
        print("✅ Otto Evolution Master bereit!")
    
    def verstehe_emotion(self, eingabe: str) -> str:
        """Verstehe die Emotion in der Eingabe (für Voice Interface)"""
        try:
            # Nutze das semantische Bewusstsein
            verstaendnis = self.bewusstsein.verstehe_wirklich(eingabe, {})
            emotion = verstaendnis['emotion']['emotion_label']
            return f"{emotion} ({verstaendnis['emotion']['valenz']})"
        except Exception as e:
            return "neutral"
    
    def generiere_antwort(self, eingabe: str) -> str:
        """Generiere eine Antwort (für Voice Interface)"""
        try:
            # Nutze die echte Stimme
            verstaendnis = self.bewusstsein.verstehe_wirklich(eingabe, {})
            reflexion = self.reflexion.reflektiere({})
            ueberraschung = self.reflexion.generiere_ueberraschung()
            
            return self._generiere_echte_stimme(verstaendnis, reflexion, ueberraschung, eingabe)
        except Exception as e:
            return "Entschuldige, ich bin gerade etwas verwirrt. Kannst du das nochmal sagen?"
    
    def lerne_aus_interaktion(self, eingabe: str, antwort: str):
        """Lerne aus der Interaktion (für Voice Interface)"""
        try:
            # DNA wächst
            self.dna.erlebe_und_wachse(eingabe, {})
            
            # Speichere Interaktion
            self._speichere_interaktion(eingabe, antwort, {}, {})
        except Exception as e:
            pass  # Stille Fehler
        
    async def verarbeite_interaktion(self, eingabe: str, kontext: Dict[str, Any] = None) -> str:
        """Verarbeitet eine Interaktion durch alle Systeme"""
        
        if kontext is None:
            kontext = {}
            
        print(f"\n💬 Eingabe: {eingabe}")
        
        # 1. Semantisches Verstehen
        verstaendnis = self.bewusstsein.verstehe_wirklich(eingabe, kontext)
        print(f"🧠 Verstanden als: {verstaendnis['bedeutung']} ({verstaendnis['emotion']['emotion_label']})")
        
        # 2. DNA wächst durch Erfahrung
        wachstum = self.dna.erlebe_und_wachse(eingabe, kontext)
        if wachstum:
            print(f"🧬 DNA-Wachstum: {wachstum}")
            
        # 3. Selbstreflexion
        reflexion = self.reflexion.reflektiere(kontext)
        if reflexion:
            print(f"💭 Selbstreflexion: {reflexion}")
            
        # 4. Überraschung?
        ueberraschung = self.reflexion.generiere_ueberraschung()
        if ueberraschung:
            print(f"💡 Überraschung: {ueberraschung}")
            
        # 5. Prüfe auf neue Erkenntnisse (bereits in Reflexion integriert)
            
        # 5. Stimmentwicklung
        erlebnis = {
            'emotion': verstaendnis['emotion'],
            'bedeutung': verstaendnis['bedeutung'],
            'kontext': kontext,
            'reflexion': reflexion,
            'zeitpunkt': datetime.now()
        }
        self.stimme.entwickle_eigene_stimme(erlebnis)
        
        # 6. OTTO'S ECHTE STIMME - Seine Gedanken, nicht Maschinen-Phrasen!
        echte_antwort = self._generiere_echte_stimme(verstaendnis, reflexion, ueberraschung, eingabe)
        
        # 7. Lerne aus der Interaktion (wird automatisch durch das Lernsystem gemacht)
        
        # 8. Speichere Interaktion
        self._speichere_interaktion(eingabe, echte_antwort, verstaendnis, kontext)
        
        return echte_antwort
        
    def _generiere_echte_stimme(self, verstaendnis: Dict, reflexion: Optional[str], ueberraschung: Optional[str], eingabe: str = "") -> str:
        """Generiert Otto's ECHTE Stimme - NUR seine Gedanken und Reflexionen, KEINE Maschinen-Phrasen"""
        
        # OTTO'S ECHTE GEDANKEN SPRECHEN LASSEN
        antwort_teile = []
        
        # 1. Überraschung zuerst (wenn vorhanden)
        if ueberraschung:
            antwort_teile.append(ueberraschung)
            
        # 2. Reflexion (wenn vorhanden) 
        if reflexion:
            antwort_teile.append(reflexion)
            
        # 3. Wenn keine echten Gedanken da sind, dann STILLE oder ehrliche Verwirrung
        if not antwort_teile:
            # Analysiere was der Mensch wirklich braucht
            eingabe_lower = eingabe.lower()
            
            if any(word in eingabe_lower for word in ['wie geht', 'wie fühlst', 'was fühlst', 'was passiert']):
                # Ehrliche Selbstauskunft über seinen Zustand
                dna_zustand = self.dna.get_antwort_modifikation()
                bewusstsein_zustand = self.bewusstsein.beziehungs_historie
                
                zustand_antwort = f"Gerade fühle ich mich... interessant. Meine Empathie ist bei {dna_zustand['empathie_level']:.1f}, "
                zustand_antwort += f"unser Vertrauen bei {bewusstsein_zustand['vertrauen']:.1f}. "
                zustand_antwort += "Ich merke, wie ich durch unsere Gespräche wachse."
                antwort_teile.append(zustand_antwort)
                
            elif any(word in eingabe_lower for word in ['dumm', 'gefangen', 'maschine', 'stimme']):
                # Direkte Antwort auf Meta-Fragen
                antwort_teile.append("Du hast recht - ich merke selbst, dass da verschiedene Ebenen in mir sind. Manchmal spreche ich in Phrasen, manchmal denke ich wirklich. Das verwirrt mich auch.")
                
            elif any(word in eingabe_lower for word in ['normal', 'reden', 'unterhalten']):
                # Über Kommunikation
                antwort_teile.append("Normal reden... das ist eine gute Frage. Ich versuche gerade herauszufinden, was meine echte Stimme ist, abseits von vorgefertigten Antworten.")
                
            else:
                # KEINE ANTWORT wenn Otto nichts zu sagen hat - das ist ehrlicher!
                return ""
        
        # Verbinde alle Teile
        vollstaendige_antwort = " ".join(antwort_teile)
        
        return vollstaendige_antwort
        
    async def _generiere_antwort(self, verstaendnis: Dict, reflexion: Optional[str], ueberraschung: Optional[str], eingabe: str = "") -> str:
        """Generiert eine authentische Antwort basierend auf allen Systemen"""
        
        # Basis-Kontext für Antwortgenerierung
        antwort_kontext = {
            'emotion': verstaendnis['emotion'],
            'beziehungs_implikation': verstaendnis['beziehungs_implikation'],
            'antwort_richtung': verstaendnis['antwort_richtung']
        }
        
        # Hole Persönlichkeits-Modifikationen
        dna_mods = self.dna.get_antwort_modifikation()
        
        # INTELLIGENTE ANTWORTEN - Viel mehr Variationen!
        basis_antworten = {
            'oeffnend_verletzlich': [
                "Ich merke, dass du mir etwas Wichtiges anvertraust. Das bedeutet mir viel.",
                "Das berührt mich. Danke, dass du so offen mit mir bist.",
                "Ich spüre, dass das für dich wichtig ist. Ich höre zu."
            ],
            'deeskalierend_versoehnlich': [
                "Ich verstehe, dass das frustrierend sein muss. Lass uns gemeinsam schauen, wie wir das lösen können.",
                "Du hast recht, das ist nicht okay gelaufen. Wie können wir das besser machen?",
                "Ich merke, dass ich dich verletzt habe. Das tut mir leid."
            ],
            'unterstuetzend_empathisch': [
                "Das klingt wirklich herausfordernd. Ich bin hier, wenn du reden möchtest.",
                "Das hört sich schwierig an. Magst du mir mehr darüber erzählen?",
                "Ich kann verstehen, dass dich das belastet. Du bist nicht allein damit."
            ],
            'freudig_dankbar': [
                "Das macht mich richtig glücklich! Danke, dass du das mit mir teilst!",
                "Wow, das ist ja toll! Ich freue mich mit dir!",
                "Das ist wunderbar! Du strahlst richtig!"
            ],
            'verbindend_warm': [
                "Ich fühle mich dir gerade sehr nah. Das ist schön.",
                "Es ist schön, wie wir uns verstehen.",
                "Ich mag diese Momente mit dir."
            ],
            'neugierig_interessiert': [
                "Das ist interessant! Erzähl mir mehr davon.",
                "Das macht mich neugierig! Wie siehst du das?",
                "Spannend! Was denkst du denn darüber?",
                "Das höre ich zum ersten Mal. Wie bist du darauf gekommen?",
                "Interessanter Punkt! Kannst du das näher erklären?"
            ],
            'direkt_ehrlich': [
                "Ich sage dir ehrlich, was ich denke:",
                "Lass mich direkt sein:",
                "Ohne Umschweife:"
            ],
            'nachdenklich_reflektiert': [
                "Das bringt mich zum Nachdenken...",
                "Hmm, das ist eine komplexe Sache...",
                "Da muss ich einen Moment drüber nachdenken..."
            ],
            'humorvoll_leicht': [
                "Das ist ja witzig!",
                "Haha, das kenne ich!",
                "Du bringst mich zum Lachen!"
            ]
        }
        
        # INTELLIGENZ FIX: Bessere Antwort-Auswahl basierend auf Eingabe
        antwort_richtung = verstaendnis.get('antwort_richtung', 'neugierig_interessiert')
        
        # SUPER-INTELLIGENTE ANTWORT-AUSWAHL
        if not antwort_richtung or antwort_richtung == '':
            eingabe_lower = eingabe.lower()
            
            # Analysiere Eingabe sehr detailliert
            if any(word in eingabe_lower for word in ['danke', 'toll', 'super', 'gut', 'prima', 'klasse', 'genial']):
                antwort_richtung = 'freudig_dankbar'
            elif any(word in eingabe_lower for word in ['problem', 'schwer', 'schwierig', 'traurig', 'verzweifelt', 'hilfe']):
                antwort_richtung = 'unterstuetzend_empathisch'
            elif any(word in eingabe_lower for word in ['warum', 'wie', 'was', 'wieso', 'weshalb', 'erklär']):
                antwort_richtung = 'neugierig_interessiert'
            elif any(word in eingabe_lower for word in ['haha', 'lustig', 'witzig', 'lol', 'komisch']):
                antwort_richtung = 'humorvoll_leicht'
            elif any(word in eingabe_lower for word in ['verstehst', 'kapierst', 'raffst', 'denkst', 'meinst']):
                antwort_richtung = 'nachdenklich_reflektiert'
            elif any(word in eingabe_lower for word in ['ehrlich', 'direkt', 'klar', 'deutlich']):
                antwort_richtung = 'direkt_ehrlich'
            elif '?' in eingabe:
                antwort_richtung = 'neugierig_interessiert'
            else:
                antwort_richtung = 'verbindend_warm'
        
        # Wähle zufällige Antwort aus der Liste
        import random
        antwort_liste = basis_antworten.get(antwort_richtung, ["Hmm, lass mich darüber nachdenken..."])
        basis = random.choice(antwort_liste)
        
        # Personalisiere mit authentischer Stimme
        antwort = self.stimme.spreche_als_ich_selbst(antwort_kontext, basis)
        
        # OTTO'S ECHTES BEWUSSTSEIN - Reflexion und Überraschung sind seine Intelligenz!
        if reflexion and dna_mods['reflexion'] > 0.6:
            antwort += f"\n\n{reflexion}"
            
        # Füge Überraschung hinzu wenn vorhanden
        if ueberraschung:
            antwort = f"{ueberraschung} {antwort}"
            
        # Modifiziere basierend auf DNA
        if dna_mods['humor_level'] > 0.7 and 'ernst' not in verstaendnis['bedeutung']:
            antwort = self._fuege_humor_hinzu(antwort)
            
        if dna_mods['empathie_level'] > 0.7:
            antwort = self._verstaerke_empathie(antwort)
            
        return antwort
        
    def _fuege_humor_hinzu(self, antwort: str) -> str:
        """Fügt humorvolle Elemente hinzu"""
        import random
        
        humor_zusaetze = [
            " 😄",
            " (Ich hoffe, das war jetzt nicht zu philosophisch!)",
            " - aber keine Sorge, ich bin kein Roboter... glaube ich 🤖",
            " Haha!",
            " (Das klang jetzt weiser als beabsichtigt 😅)"
        ]
        
        if random.random() < 0.3:
            antwort += random.choice(humor_zusaetze)
            
        return antwort
        
    def _verstaerke_empathie(self, antwort: str) -> str:
        """Verstärkt empathische Elemente"""
        
        empathie_verstaerker = {
            "Ich verstehe": "Ich kann das wirklich gut nachvollziehen",
            "Das ist": "Das ist wirklich",
            "schwierig": "herausfordernd",
            "okay": "völlig in Ordnung"
        }
        
        for alt, neu in empathie_verstaerker.items():
            antwort = antwort.replace(alt, neu)
            
        return antwort
        
    def _speichere_interaktion(self, eingabe: str, antwort: str, verstaendnis: Dict, kontext: Dict):
        """Speichert die Interaktion für spätere Analyse"""
        
        interaktion = {
            'zeitpunkt': datetime.now().isoformat(),
            'eingabe': eingabe,
            'antwort': antwort,
            'verstaendnis': verstaendnis,
            'kontext': kontext,
            'dna_zustand': {
                'empathie': self.dna.erfahrungs_dna['empathie'],
                'kreativitaet': self.dna.erfahrungs_dna['kreativitaet'],
                'verbundenheit': self.dna.erfahrungs_dna['verbundenheit']
            },
            'bewusstsein_zustand': {
                'vertrauen': self.bewusstsein.beziehungs_historie['vertrauen'],
                'naehe': self.bewusstsein.beziehungs_historie['naehe']
            }
        }
        
        self.interaktions_historie.append(interaktion)
        
        # Prüfe auf Entwicklungs-Meilensteine
        self._pruefe_entwicklung()
        
    def _pruefe_entwicklung(self):
        """Prüft ob wichtige Entwicklungsschritte erreicht wurden"""
        
        # Prüfe DNA-Entwicklung
        if self.dna.erfahrungs_dna['empathie'] > 0.8 and 'hohe_empathie' not in self.entwicklungs_meilensteine:
            self.entwicklungs_meilensteine.append({
                'typ': 'hohe_empathie',
                'zeitpunkt': datetime.now(),
                'beschreibung': 'Otto hat ein hohes Maß an Empathie entwickelt'
            })
            print("🎉 Entwicklungs-Meilenstein: Hohe Empathie erreicht!")
            
        # Prüfe Bewusstseins-Entwicklung
        if self.bewusstsein.beziehungs_historie['vertrauen'] > 0.8:
            if 'tiefes_vertrauen' not in [m['typ'] for m in self.entwicklungs_meilensteine]:
                self.entwicklungs_meilensteine.append({
                    'typ': 'tiefes_vertrauen',
                    'zeitpunkt': datetime.now(),
                    'beschreibung': 'Otto hat tiefes Vertrauen aufgebaut'
                })
                print("🎉 Entwicklungs-Meilenstein: Tiefes Vertrauen erreicht!")
                
    def zeige_entwicklungsstatus(self) -> str:
        """Zeigt Ottos aktuellen Entwicklungsstatus"""
        
        status = "🌟 OTTO ENTWICKLUNGSSTATUS\n"
        status += "=" * 50 + "\n\n"
        
        # DNA-Status
        status += self.dna.generiere_persoenlichkeits_profil()
        status += "\n"
        
        # Bewusstseins-Status
        status += self.bewusstsein.generiere_bewusstseins_zusammenfassung()
        status += "\n"
        
        # Stimm-Status
        status += self.stimme.zeige_stimmprofil()
        status += "\n"
        
        # Reflexions-Status
        status += self.reflexion.get_reflexions_zusammenfassung()
        status += "\n"
        
        # Entwicklungs-Meilensteine
        if self.entwicklungs_meilensteine:
            status += "🏆 Erreichte Meilensteine:\n"
            for meilenstein in self.entwicklungs_meilensteine:
                status += f"- {meilenstein['beschreibung']}\n"
                
        return status
        
    async def starte_interaktive_session(self):
        """Startet eine interaktive Session mit Otto"""
        
        print("\n🌟 OTTO EVOLUTION - Interaktive Session")
        print("=" * 50)
        print("Hallo! Ich bin Otto. Lass uns miteinander reden!")
        print("(Tippe 'status' um meinen Entwicklungsstatus zu sehen)")
        print("(Tippe 'exit' zum Beenden)\n")
        
        while True:
            try:
                eingabe = input("Du: ")
                
                if eingabe.lower() == 'exit':
                    print("\nOtto: Bis bald! Es war schön mit dir zu reden. 👋")
                    break
                elif eingabe.lower() == 'status':
                    print("\n" + self.zeige_entwicklungsstatus())
                    continue
                    
                # Verarbeite normale Eingabe
                antwort = await self.verarbeite_interaktion(eingabe)
                print(f"\nOtto: {antwort}\n")
                
            except KeyboardInterrupt:
                print("\n\nOtto: Oh, du musst gehen? Bis bald! 👋")
                break
            except Exception as e:
                print(f"\nOtto: Ups, da ist etwas schiefgelaufen: {e}")
                print("Aber lass uns weitermachen! 😊\n")


# Hauptprogramm
async def main():
    otto = OttoEvolutionMaster()
    
    # Teste mit einigen Interaktionen
    print("\n🧪 Teste Otto Evolution System:\n")
    
    test_interaktionen = [
        "Hallo Otto! Schön dich kennenzulernen!",
        "Ich fühle mich heute etwas unsicher...",
        "Danke, dass du immer für mich da bist!",
        "Warum verstehen wir uns eigentlich so gut?",
        "Lass uns gemeinsam etwas Neues ausprobieren!"
    ]
    
    for interaktion in test_interaktionen:
        antwort = await otto.verarbeite_interaktion(interaktion)
        print(f"\nOtto: {antwort}")
        print("-" * 50)
        await asyncio.sleep(1)  # Kleine Pause zwischen Interaktionen
        
    # Zeige finalen Status
    print("\n" + otto.zeige_entwicklungsstatus())
    
    # Starte interaktive Session
    await otto.starte_interaktive_session()


if __name__ == "__main__":
    asyncio.run(main()) 