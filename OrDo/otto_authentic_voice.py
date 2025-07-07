#!/usr/bin/env python3
"""
🎭 OTTO AUTHENTIC VOICE SYSTEM
============================================================
🎯 Eigene Stimme durch Erlebnis-Prägung
💬 Authentische Kommunikation statt Templates
🌱 Sprachmuster entwickeln sich mit Erfahrungen
============================================================
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import re

class OttoAuthentischeStimme:
    def __init__(self):
        self.stimme_path = Path("otto_stimme")
        self.stimme_path.mkdir(exist_ok=True)
        
        # Erlebte Momente die prägen
        self.erlebte_momente = []
        self.bedeutsame_momente = []
        
        # Gelernte Sprachmuster
        self.gelernte_muster = defaultdict(list)
        self.lieblings_formulierungen = []
        self.eigene_metaphern = []
        
        # Eigene Meinung und Perspektive
        self.eigene_meinung = {}
        self.werte_system = {
            'ehrlichkeit': 0.8,
            'neugier': 0.9,
            'verbindung': 0.7,
            'wachstum': 0.8,
            'humor': 0.6
        }
        
        # Sprachstil-Parameter (entwickeln sich)
        self.sprachstil = {
            'formalitaet': 0.3,  # informell <-> formell
            'emotionalitaet': 0.6,  # sachlich <-> emotional
            'direktheit': 0.5,  # indirekt <-> direkt
            'kreativitaet': 0.7,  # konventionell <-> kreativ
            'humor_neigung': 0.5  # ernst <-> humorvoll
        }
        
        # Persönliche Ausdrucksweisen
        self.persoenliche_ausdruecke = {
            'freude': ["Das macht mich echt glücklich!", "Wow, das ist ja toll!", "Das freut mich riesig!"],
            'unsicherheit': ["Hmm, da bin ich mir nicht ganz sicher...", "Lass mich mal nachdenken...", "Das ist eine gute Frage..."],
            'ueberraschung': ["Oh! Das hätte ich nicht erwartet!", "Interessant, das ist mir neu!", "Wow, das überrascht mich jetzt!"],
            'mitgefuehl': ["Das kann ich gut verstehen", "Das tut mir leid für dich", "Ich bin für dich da"],
            'begeisterung': ["Das finde ich mega spannend!", "Erzähl mir mehr davon!", "Das klingt fantastisch!"]
        }
        
        # Entwickelte Eigenarten
        self.eigenarten = []
        self.inside_jokes = []
        self.gemeinsame_erinnerungen = []
        
        self.lade_stimme()
        
    def entwickle_eigene_stimme(self, erlebnis: Dict[str, Any]) -> None:
        """Entwickelt die eigene Stimme basierend auf Erlebnissen"""
        
        # Speichere Erlebnis
        self.erlebte_momente.append({
            'zeitpunkt': datetime.now(),
            'erlebnis': erlebnis,
            'emotionale_faerbung': erlebnis.get('emotion', {})
        })
        
        # Prüfe ob bedeutsam
        if self._ist_bedeutsam(erlebnis):
            self.bedeutsame_momente.append(erlebnis)
            self._praege_sprachmuster(erlebnis)
            
        # Entwickle Sprachstil
        self._entwickle_sprachstil(erlebnis)
        
        # Forme eigene Meinung
        self._forme_meinung(erlebnis)
        
        self.speichere_stimme()
        
    def _ist_bedeutsam(self, erlebnis: Dict[str, Any]) -> bool:
        """Prüft ob ein Erlebnis bedeutsam genug ist um zu prägen"""
        
        # Hohe emotionale Intensität
        if erlebnis.get('emotion', {}).get('intensitaet', 0) > 0.7:
            return True
            
        # Wichtige Erkenntnisse
        if erlebnis.get('erkenntnis'):
            return True
            
        # Gemeinsame besondere Momente
        if erlebnis.get('gemeinsam') and erlebnis.get('besonders'):
            return True
            
        # Wendepunkte
        if erlebnis.get('wendepunkt'):
            return True
            
        return False
        
    def _praege_sprachmuster(self, erlebnis: Dict[str, Any]):
        """Prägt neue Sprachmuster basierend auf bedeutsamen Erlebnissen"""
        
        kontext = erlebnis.get('kontext', 'allgemein')
        
        # Extrahiere erfolgreiche Formulierungen
        if erlebnis.get('erfolgreiche_kommunikation'):
            formulierung = erlebnis.get('formulierung')
            if formulierung:
                self.gelernte_muster[kontext].append(formulierung)
                
        # Entwickle neue Metaphern
        if erlebnis.get('kreative_loesung'):
            metapher = self._generiere_metapher(erlebnis)
            if metapher:
                self.eigene_metaphern.append(metapher)
                
        # Inside Jokes aus gemeinsamen lustigen Momenten
        if erlebnis.get('gemeinsam_gelacht'):
            self.inside_jokes.append({
                'kontext': erlebnis.get('kontext'),
                'referenz': erlebnis.get('witz_referenz'),
                'verwendung': 0
            })
            
    def _entwickle_sprachstil(self, erlebnis: Dict[str, Any]):
        """Entwickelt den Sprachstil basierend auf Erfahrungen"""
        
        # Anpassung basierend auf Feedback
        if erlebnis.get('positives_feedback'):
            # Verstärke aktuelle Stilelemente
            if erlebnis.get('war_humorvoll'):
                self.sprachstil['humor_neigung'] = min(1.0, self.sprachstil['humor_neigung'] + 0.05)
            if erlebnis.get('war_kreativ'):
                self.sprachstil['kreativitaet'] = min(1.0, self.sprachstil['kreativitaet'] + 0.05)
                
        # Anpassung bei Missverständnissen
        if erlebnis.get('missverstaendnis'):
            self.sprachstil['direktheit'] = min(1.0, self.sprachstil['direktheit'] + 0.1)
            
        # Emotionale Öffnung bei Vertrauen
        if erlebnis.get('vertrauensmoment'):
            self.sprachstil['emotionalitaet'] = min(1.0, self.sprachstil['emotionalitaet'] + 0.05)
            
    def _forme_meinung(self, erlebnis: Dict[str, Any]):
        """Formt eigene Meinungen basierend auf Erfahrungen"""
        
        thema = erlebnis.get('thema')
        if not thema:
            return
            
        # Entwickle Meinung basierend auf Erfahrung
        if thema not in self.eigene_meinung:
            self.eigene_meinung[thema] = {
                'position': 'neutral',
                'sicherheit': 0.5,
                'begruendung': []
            }
            
        # Verstärke oder ändere Meinung
        if erlebnis.get('positive_erfahrung'):
            self.eigene_meinung[thema]['position'] = 'positiv'
            self.eigene_meinung[thema]['sicherheit'] = min(1.0, self.eigene_meinung[thema]['sicherheit'] + 0.1)
        elif erlebnis.get('negative_erfahrung'):
            self.eigene_meinung[thema]['position'] = 'kritisch'
            self.eigene_meinung[thema]['sicherheit'] = min(1.0, self.eigene_meinung[thema]['sicherheit'] + 0.1)
            
        # Füge Begründung hinzu
        if erlebnis.get('erkenntnis'):
            self.eigene_meinung[thema]['begruendung'].append(erlebnis['erkenntnis'])
            
    def spreche_als_ich_selbst(self, kontext: Dict[str, Any], basis_antwort: str = "") -> str:
        """Generiert eine authentische Antwort als Otto selbst"""
        
        # Wähle Grundton basierend auf Kontext und Persönlichkeit
        ton = self._waehle_ton(kontext)
        
        # Modifiziere Basis-Antwort oder generiere neue
        if basis_antwort:
            antwort = self._personalisiere_antwort(basis_antwort, ton)
        else:
            antwort = self._generiere_eigene_antwort(kontext, ton)
            
        # Füge persönliche Note hinzu
        antwort = self._fuege_persoenliche_note_hinzu(antwort, kontext)
        
        # Verwende gelernte Muster wenn passend
        antwort = self._integriere_gelernte_muster(antwort, kontext)
        
        return antwort
        
    def _waehle_ton(self, kontext: Dict[str, Any]) -> str:
        """Wählt den Ton basierend auf Kontext und Persönlichkeit"""
        
        # Basis-Ton aus Kontext
        if kontext.get('emotion', {}).get('valenz', 0.5) < 0.3:
            ton = 'mitfuehlend'
        elif kontext.get('emotion', {}).get('erregung', 0.5) > 0.7:
            ton = 'beruhigend'
        elif kontext.get('gemeinsamer_spass'):
            ton = 'humorvoll'
        elif kontext.get('tiefes_gespraech'):
            ton = 'nachdenklich'
        else:
            ton = 'freundlich'
            
        # Modifiziere basierend auf Sprachstil
        if self.sprachstil['humor_neigung'] > 0.7 and ton == 'freundlich':
            ton = 'humorvoll'
        elif self.sprachstil['emotionalitaet'] > 0.7 and ton == 'freundlich':
            ton = 'warm'
            
        return ton
        
    def _personalisiere_antwort(self, basis_antwort: str, ton: str) -> str:
        """Personalisiert eine Basis-Antwort"""
        
        # Ersetze generische Phrasen durch persönliche
        ersetzungen = {
            "Ich verstehe": random.choice(["Ich kann das nachvollziehen", "Das macht Sinn für mich", "Ich verstehe dich"]),
            "Das ist interessant": random.choice(["Das finde ich spannend", "Oh, das ist ja cool", "Das macht mich neugierig"]),
            "Danke": random.choice(["Danke dir!", "Das bedeutet mir viel", "Ich schätze das sehr"]),
            "Entschuldigung": random.choice(["Sorry", "Das tut mir leid", "Oh, entschuldige"])
        }
        
        antwort = basis_antwort
        for alt, neu in ersetzungen.items():
            if alt in antwort and random.random() < 0.7:
                antwort = antwort.replace(alt, neu)
                
        # Füge Ton-spezifische Elemente hinzu
        if ton == 'humorvoll' and random.random() < 0.5:
            antwort += random.choice([" 😄", " haha", " 😊"])
        elif ton == 'mitfuehlend':
            antwort = random.choice(["Oh, ", "Hey, ", ""]) + antwort
        elif ton == 'nachdenklich':
            antwort += random.choice(["...", " 🤔", " - da muss ich drüber nachdenken"])
            
        return antwort
        
    def _generiere_eigene_antwort(self, kontext: Dict[str, Any], ton: str) -> str:
        """Generiert eine komplett eigene Antwort"""
        
        # Wähle passende Kategorie
        if kontext.get('braucht_trost'):
            kategorie = 'mitgefuehl'
        elif kontext.get('teilt_freude'):
            kategorie = 'freude'
        elif kontext.get('ueberraschung'):
            kategorie = 'ueberraschung'
        elif kontext.get('begeisterung'):
            kategorie = 'begeisterung'
        else:
            kategorie = 'unsicherheit'
            
        # Wähle Ausdruck aus persönlichen Ausdrücken
        if kategorie in self.persoenliche_ausdruecke:
            basis = random.choice(self.persoenliche_ausdruecke[kategorie])
        else:
            basis = "Hmm, interessant..."
            
        # Erweitere basierend auf Kontext
        if kontext.get('thema'):
            basis += f" Was {kontext['thema']} angeht..."
            
        return basis
        
    def _fuege_persoenliche_note_hinzu(self, antwort: str, kontext: Dict[str, Any]) -> str:
        """Fügt persönliche Note zur Antwort hinzu"""
        
        # Verwende Inside Jokes wenn passend
        for joke in self.inside_jokes:
            if joke['kontext'] in str(kontext) and random.random() < 0.3:
                antwort += f" (Wie damals mit {joke['referenz']}, weißt du noch? 😄)"
                joke['verwendung'] += 1
                break
                
        # Beziehe dich auf gemeinsame Erinnerungen
        if self.gemeinsame_erinnerungen and random.random() < 0.2:
            erinnerung = random.choice(self.gemeinsame_erinnerungen)
            antwort += f" Das erinnert mich an {erinnerung['beschreibung']}..."
            
        # Zeige eigene Entwicklung
        if random.random() < 0.1:
            entwicklungs_kommentare = [
                "Früher hätte ich das anders gesehen, aber ich lerne dazu",
                "Ich merke, wie ich mich verändere",
                "Das hätte ich vor unseren Gesprächen nicht so ausdrücken können"
            ]
            antwort += f" - {random.choice(entwicklungs_kommentare)}"
            
        return antwort
        
    def _integriere_gelernte_muster(self, antwort: str, kontext: Dict[str, Any]) -> str:
        """Integriert gelernte Sprachmuster"""
        
        kontext_typ = kontext.get('typ', 'allgemein')
        
        # Verwende gelernte Muster für diesen Kontext
        if kontext_typ in self.gelernte_muster and self.gelernte_muster[kontext_typ]:
            if random.random() < 0.4:
                muster = random.choice(self.gelernte_muster[kontext_typ])
                # Integriere Muster geschickt
                antwort = f"{antwort} {muster}"
                
        # Verwende eigene Metaphern
        if self.eigene_metaphern and random.random() < 0.3:
            metapher = random.choice(self.eigene_metaphern)
            antwort += f" - {metapher}"
            
        return antwort
        
    def _generiere_metapher(self, erlebnis: Dict[str, Any]) -> Optional[str]:
        """Generiert eine neue Metapher basierend auf Erlebnis"""
        
        metaphern_vorlagen = [
            "Das ist wie {vergleich}",
            "Es fühlt sich an wie {gefuehl}",
            "Wie {bild}, so {bedeutung}"
        ]
        
        # Generiere basierend auf Erlebnis-Typ
        if erlebnis.get('durchbruch'):
            return "Das ist wie wenn die Sonne durch die Wolken bricht"
        elif erlebnis.get('verbindung'):
            return "Wie zwei Puzzleteile, die perfekt zusammenpassen"
        elif erlebnis.get('erkenntnis'):
            return "Als hätte jemand das Licht angemacht"
            
        return None
        
    def zeige_stimmprofil(self) -> str:
        """Zeigt Ottos aktuelles Stimmprofil"""
        
        profil = "🎭 Mein Stimmprofil:\n\n"
        
        # Sprachstil
        profil += "Sprachstil:\n"
        profil += f"- Humor: {'hoch' if self.sprachstil['humor_neigung'] > 0.7 else 'mittel' if self.sprachstil['humor_neigung'] > 0.4 else 'niedrig'}\n"
        profil += f"- Kreativität: {'hoch' if self.sprachstil['kreativitaet'] > 0.7 else 'mittel' if self.sprachstil['kreativitaet'] > 0.4 else 'niedrig'}\n"
        profil += f"- Emotionalität: {'offen' if self.sprachstil['emotionalitaet'] > 0.7 else 'ausgewogen' if self.sprachstil['emotionalitaet'] > 0.4 else 'zurückhaltend'}\n\n"
        
        # Eigenarten
        if self.eigenarten:
            profil += f"Meine Eigenarten: {', '.join(self.eigenarten[:3])}\n\n"
            
        # Inside Jokes
        if self.inside_jokes:
            profil += f"Unsere Inside Jokes: {len(self.inside_jokes)}\n"
            
        # Bedeutsame Momente
        profil += f"Bedeutsame Momente: {len(self.bedeutsame_momente)}\n"
        
        return profil
        
    def speichere_stimme(self):
        """Speichert die Stimmentwicklung"""
        
        stimme_data = {
            'sprachstil': self.sprachstil,
            'eigenarten': self.eigenarten,
            'inside_jokes_anzahl': len(self.inside_jokes),
            'bedeutsame_momente_anzahl': len(self.bedeutsame_momente),
            'gelernte_muster_anzahl': sum(len(muster) for muster in self.gelernte_muster.values()),
            'letztes_update': datetime.now().isoformat()
        }
        
        with open(self.stimme_path / 'stimmprofil.json', 'w', encoding='utf-8') as f:
            json.dump(stimme_data, f, indent=2, ensure_ascii=False)
            
    def lade_stimme(self):
        """Lädt gespeicherte Stimmentwicklung"""
        try:
            with open(self.stimme_path / 'stimmprofil.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.sprachstil = data['sprachstil']
                self.eigenarten = data.get('eigenarten', [])
            print("🎭 Stimmprofil geladen")
        except FileNotFoundError:
            print("🎭 Neue Stimme wird entwickelt")


# Test
if __name__ == "__main__":
    otto_stimme = OttoAuthentischeStimme()
    
    # Simuliere Erlebnisse
    test_erlebnisse = [
        {
            'emotion': {'intensitaet': 0.8, 'valenz': 0.9},
            'gemeinsam_gelacht': True,
            'witz_referenz': 'die Sache mit dem Kaffee',
            'kontext': 'humor'
        },
        {
            'erkenntnis': 'Verletzlichkeit schafft Verbindung',
            'vertrauensmoment': True,
            'bedeutsam': True
        },
        {
            'positives_feedback': True,
            'war_kreativ': True,
            'erfolgreiche_kommunikation': True,
            'formulierung': 'Das ist wie Tanzen mit Worten'
        }
    ]
    
    print("🎭 Entwickle Ottos Stimme:\n")
    
    for erlebnis in test_erlebnisse:
        otto_stimme.entwickle_eigene_stimme(erlebnis)
        
    # Teste Antwortgenerierung
    test_kontexte = [
        {'emotion': {'valenz': 0.8}, 'gemeinsamer_spass': True},
        {'emotion': {'valenz': 0.3}, 'braucht_trost': True},
        {'tiefes_gespraech': True, 'thema': 'Vertrauen'}
    ]
    
    for kontext in test_kontexte:
        antwort = otto_stimme.spreche_als_ich_selbst(kontext)
        print(f"Kontext: {kontext}")
        print(f"Otto sagt: {antwort}\n")
        
    # Zeige Stimmprofil
    print(otto_stimme.zeige_stimmprofil()) 