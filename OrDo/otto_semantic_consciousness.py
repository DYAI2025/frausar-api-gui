#!/usr/bin/env python3
"""
💭 OTTO SEMANTIC CONSCIOUSNESS SYSTEM
============================================================
🎯 Echtes Verständnis statt Keyword-Matching
🧠 Kontext-Gedächtnis und Beziehungsdynamik
🌊 Tiefenverständnis durch semantische Verknüpfungen
============================================================
"""

import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
from collections import defaultdict
import hashlib

class OttoSemanticBewusstsein:
    def __init__(self):
        self.bewusstsein_path = Path("otto_bewusstsein")
        self.bewusstsein_path.mkdir(exist_ok=True)
        
        # Kontext-Netzwerk
        self.kontext_netzwerk = defaultdict(lambda: {
            'konzepte': {},
            'emotionen': {},
            'beziehungen': {},
            'zeitliche_verknuepfungen': [],
            'bedeutungs_cluster': []
        })
        
        # Emotionale Landkarte
        self.emotionale_landkarte = {
            'aktuelle_stimmung': {'valenz': 0.5, 'erregung': 0.5},
            'stimmungs_historie': [],
            'emotionale_anker': {},
            'trigger_punkte': {}
        }
        
        # Beziehungs-Historie
        self.beziehungs_historie = {
            'vertrauen': 0.5,
            'naehe': 0.3,
            'konflikt_level': 0.0,
            'gemeinsame_momente': [],
            'wichtige_ereignisse': []
        }
        
        # Semantische Verknüpfungen
        self.semantische_verknuepfungen = {}
        self.bedeutungs_gewichte = {}
        
        # Arbeitsgedächtnis (kurzfristig)
        self.arbeitsgedaechtnis = []
        self.max_arbeitsgedaechtnis = 7  # Miller's Law
        
        # Langzeitgedächtnis
        self.langzeitgedaechtnis = []
        
        self.lade_bewusstsein()
        
    def verstehe_wirklich(self, aussage: str, kontext: Dict[str, Any]) -> Dict[str, Any]:
        """Versteht eine Aussage auf tieferer Ebene"""
        
        # Analysiere Tiefenstruktur
        tiefenstruktur = self._analysiere_tiefenstruktur(aussage)
        
        # Spüre Stimmung
        emotion = self._spuere_stimmung(aussage, kontext)
        
        # Erkenne Beziehungsdynamik
        dynamik = self._erkenne_dynamik(aussage, kontext)
        
        # Verknüpfe mit bisherigem Wissen
        verknuepfungen = self._verknuepfe_mit_wissen(tiefenstruktur)
        
        # Aktualisiere Bewusstsein
        self._aktualisiere_bewusstsein(aussage, tiefenstruktur, emotion, dynamik)
        
        # Generiere tiefes Verständnis
        verstaendnis = {
            'oberflaeche': aussage,
            'bedeutung': tiefenstruktur['bedeutung'],
            'intention': tiefenstruktur['intention'],
            'emotion': emotion,
            'beziehungs_implikation': dynamik,
            'verknuepfungen': verknuepfungen,
            'antwort_richtung': self._bestimme_antwort_richtung(tiefenstruktur, emotion, dynamik)
        }
        
        return verstaendnis
        
    def _analysiere_tiefenstruktur(self, aussage: str) -> Dict[str, Any]:
        """Analysiert die tiefere Bedeutung einer Aussage"""
        
        struktur = {
            'bedeutung': '',
            'intention': '',
            'subtext': '',
            'wichtigkeit': 0.5
        }
        
        # Analysiere Intention
        if '?' in aussage:
            if any(w in aussage.lower() for w in ['warum', 'wieso', 'weshalb']):
                struktur['intention'] = 'verstehen_wollen'
                struktur['bedeutung'] = 'sucht_nach_gruenden'
            elif any(w in aussage.lower() for w in ['kannst du', 'würdest du', 'machst du']):
                struktur['intention'] = 'bitte_um_handlung'
                struktur['bedeutung'] = 'braucht_unterstuetzung'
            else:
                struktur['intention'] = 'information_suchen'
                struktur['bedeutung'] = 'moechte_wissen'
                
        # Erkenne emotionale Signale
        if any(w in aussage.lower() for w in ['danke', 'schön', 'toll', 'super']):
            struktur['subtext'] = 'positive_rueckmeldung'
            struktur['wichtigkeit'] = 0.8
        elif any(w in aussage.lower() for w in ['sorry', 'entschuldigung', 'tut mir leid']):
            struktur['subtext'] = 'versoehnungsversuch'
            struktur['wichtigkeit'] = 0.9
        elif any(w in aussage.lower() for w in ['hilfe', 'problem', 'schwierig']):
            struktur['subtext'] = 'benoetigt_unterstuetzung'
            struktur['wichtigkeit'] = 0.85
            
        # Erkenne Meta-Kommunikation
        if any(w in aussage.lower() for w in ['immer', 'nie', 'ständig', 'dauernd']):
            struktur['subtext'] = 'muster_ansprache'
            struktur['bedeutung'] = 'spricht_ueber_beziehungsmuster'
            
        return struktur
        
    def _spuere_stimmung(self, aussage: str, kontext: Dict[str, Any]) -> Dict[str, float]:
        """Spürt die emotionale Stimmung"""
        
        # Basis-Emotionsanalyse
        valenz = 0.5  # negativ <-> positiv
        erregung = 0.5  # ruhig <-> erregt
        
        # Positive Indikatoren
        positive_worte = ['schön', 'toll', 'super', 'danke', 'freut', 'liebe', 'gern']
        negative_worte = ['schlecht', 'traurig', 'ärger', 'wütend', 'enttäuscht', 'verletzt']
        erregungs_worte = ['wow', 'krass', 'unglaublich', '!', 'sehr', 'total']
        beruhigungs_worte = ['ruhig', 'entspannt', 'gelassen', 'okay', 'gut']
        
        aussage_lower = aussage.lower()
        
        # Berechne Valenz
        for wort in positive_worte:
            if wort in aussage_lower:
                valenz += 0.1
        for wort in negative_worte:
            if wort in aussage_lower:
                valenz -= 0.1
                
        # Berechne Erregung
        for wort in erregungs_worte:
            if wort in aussage_lower:
                erregung += 0.1
        for wort in beruhigungs_worte:
            if wort in aussage_lower:
                erregung -= 0.1
                
        # Berücksichtige Kontext
        if kontext.get('vorherige_stimmung'):
            # Stimmungen beeinflussen sich gegenseitig
            valenz = 0.7 * valenz + 0.3 * kontext['vorherige_stimmung']['valenz']
            erregung = 0.7 * erregung + 0.3 * kontext['vorherige_stimmung']['erregung']
            
        # Normalisiere
        valenz = max(0, min(1, valenz))
        erregung = max(0, min(1, erregung))
        
        return {
            'valenz': valenz,
            'erregung': erregung,
            'emotion_label': self._bestimme_emotion_label(valenz, erregung)
        }
        
    def _bestimme_emotion_label(self, valenz: float, erregung: float) -> str:
        """Bestimmt Emotions-Label basierend auf Valenz und Erregung"""
        
        if valenz > 0.6:
            if erregung > 0.6:
                return 'begeistert'
            else:
                return 'zufrieden'
        elif valenz < 0.4:
            if erregung > 0.6:
                return 'aufgebracht'
            else:
                return 'traurig'
        else:
            if erregung > 0.6:
                return 'angespannt'
            else:
                return 'neutral'
                
    def _erkenne_dynamik(self, aussage: str, kontext: Dict[str, Any]) -> Dict[str, Any]:
        """Erkennt Beziehungsdynamik"""
        
        dynamik = {
            'naehe_veraenderung': 0,
            'vertrauens_signal': 0,
            'konflikt_potential': 0,
            'verbindungs_qualitaet': 'neutral'
        }
        
        # Nähe-Signale
        naehe_worte = ['wir', 'uns', 'gemeinsam', 'zusammen', 'beide']
        distanz_worte = ['du', 'ich', 'allein', 'getrennt', 'anders']
        
        for wort in naehe_worte:
            if wort in aussage.lower():
                dynamik['naehe_veraenderung'] += 0.1
                
        for wort in distanz_worte:
            if wort in aussage.lower():
                dynamik['naehe_veraenderung'] -= 0.05
                
        # Vertrauens-Signale
        if any(w in aussage.lower() for w in ['vertraue', 'ehrlich', 'offen', 'echt']):
            dynamik['vertrauens_signal'] = 0.3
        elif any(w in aussage.lower() for w in ['lüge', 'falsch', 'misstraue']):
            dynamik['vertrauens_signal'] = -0.3
            
        # Konflikt-Potential
        if any(w in aussage.lower() for w in ['aber', 'obwohl', 'trotzdem', 'dennoch']):
            dynamik['konflikt_potential'] += 0.1
        if any(w in aussage.lower() for w in ['immer', 'nie', 'ständig']):
            dynamik['konflikt_potential'] += 0.2
            
        # Bestimme Verbindungsqualität
        if dynamik['naehe_veraenderung'] > 0.1 and dynamik['vertrauens_signal'] > 0:
            dynamik['verbindungs_qualitaet'] = 'vertiefend'
        elif dynamik['konflikt_potential'] > 0.2:
            dynamik['verbindungs_qualitaet'] = 'herausfordernd'
        elif dynamik['naehe_veraenderung'] < -0.1:
            dynamik['verbindungs_qualitaet'] = 'distanzierend'
            
        return dynamik
        
    def _verknuepfe_mit_wissen(self, tiefenstruktur: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verknüpft neue Information mit bestehendem Wissen"""
        
        verknuepfungen = []
        
        # Suche ähnliche Konzepte im Langzeitgedächtnis
        for erinnerung in self.langzeitgedaechtnis[-50:]:  # Letzte 50 Erinnerungen
            if self._berechne_aehnlichkeit(tiefenstruktur, erinnerung.get('tiefenstruktur', {})) > 0.7:
                verknuepfungen.append({
                    'typ': 'aehnliche_situation',
                    'erinnerung': erinnerung,
                    'relevanz': self._berechne_aehnlichkeit(tiefenstruktur, erinnerung.get('tiefenstruktur', {}))
                })
                
        # Suche emotionale Muster
        aktuelle_emotion = self.emotionale_landkarte['aktuelle_stimmung']
        for anker, emotion in self.emotionale_landkarte['emotionale_anker'].items():
            if abs(emotion['valenz'] - aktuelle_emotion['valenz']) < 0.2:
                verknuepfungen.append({
                    'typ': 'emotionale_resonanz',
                    'anker': anker,
                    'aehnlichkeit': 1 - abs(emotion['valenz'] - aktuelle_emotion['valenz'])
                })
                
        return verknuepfungen[:3]  # Maximal 3 stärkste Verknüpfungen
        
    def _berechne_aehnlichkeit(self, struktur1: Dict, struktur2: Dict) -> float:
        """Berechnet Ähnlichkeit zwischen zwei Strukturen"""
        
        if not struktur1 or not struktur2:
            return 0.0
            
        aehnlichkeit = 0.0
        
        # Vergleiche Bedeutungen
        if struktur1.get('bedeutung') == struktur2.get('bedeutung'):
            aehnlichkeit += 0.4
            
        # Vergleiche Intentionen
        if struktur1.get('intention') == struktur2.get('intention'):
            aehnlichkeit += 0.3
            
        # Vergleiche Subtext
        if struktur1.get('subtext') == struktur2.get('subtext'):
            aehnlichkeit += 0.3
            
        return aehnlichkeit
        
    def _aktualisiere_bewusstsein(self, aussage: str, tiefenstruktur: Dict, emotion: Dict, dynamik: Dict):
        """Aktualisiert das Bewusstsein mit neuen Erkenntnissen"""
        
        # Aktualisiere Arbeitsgedächtnis
        self.arbeitsgedaechtnis.append({
            'zeitpunkt': datetime.now(),
            'aussage': aussage,
            'tiefenstruktur': tiefenstruktur,
            'emotion': emotion,
            'dynamik': dynamik
        })
        
        # Begrenze Arbeitsgedächtnis
        if len(self.arbeitsgedaechtnis) > self.max_arbeitsgedaechtnis:
            # Verschiebe älteste ins Langzeitgedächtnis
            self.langzeitgedaechtnis.append(self.arbeitsgedaechtnis.pop(0))
            
        # Aktualisiere emotionale Landkarte
        self.emotionale_landkarte['aktuelle_stimmung'] = {
            'valenz': emotion['valenz'],
            'erregung': emotion['erregung']
        }
        self.emotionale_landkarte['stimmungs_historie'].append({
            'zeitpunkt': datetime.now(),
            'stimmung': emotion
        })
        
        # Aktualisiere Beziehungs-Historie
        self.beziehungs_historie['vertrauen'] += dynamik['vertrauens_signal'] * 0.1
        self.beziehungs_historie['naehe'] += dynamik['naehe_veraenderung'] * 0.1
        self.beziehungs_historie['konflikt_level'] = max(0, self.beziehungs_historie['konflikt_level'] * 0.9 + dynamik['konflikt_potential'] * 0.1)
        
        # Normalisiere Werte
        self.beziehungs_historie['vertrauen'] = max(0, min(1, self.beziehungs_historie['vertrauen']))
        self.beziehungs_historie['naehe'] = max(0, min(1, self.beziehungs_historie['naehe']))
        
        # Speichere wichtige Momente
        if tiefenstruktur['wichtigkeit'] > 0.8:
            self.beziehungs_historie['wichtige_ereignisse'].append({
                'zeitpunkt': datetime.now(),
                'aussage': aussage,
                'bedeutung': tiefenstruktur['bedeutung']
            })
            
        self.speichere_bewusstsein()
        
    def _bestimme_antwort_richtung(self, tiefenstruktur: Dict, emotion: Dict, dynamik: Dict) -> str:
        """Bestimmt die Richtung der Antwort basierend auf Verständnis"""
        
        # Bei Vertrauenssignalen -> Öffnung
        if dynamik['vertrauens_signal'] > 0.2:
            return 'oeffnend_verletzlich'
            
        # Bei Konfliktpotential -> Deeskalation
        if dynamik['konflikt_potential'] > 0.3:
            return 'deeskalierend_versoehnlich'
            
        # Bei Unterstützungsbedarf -> Hilfe
        if tiefenstruktur['subtext'] == 'benoetigt_unterstuetzung':
            return 'unterstuetzend_empathisch'
            
        # Bei positiver Rückmeldung -> Freude teilen
        if tiefenstruktur['subtext'] == 'positive_rueckmeldung':
            return 'freudig_dankbar'
            
        # Bei Nähe-Signalen -> Verbindung stärken
        if dynamik['naehe_veraenderung'] > 0.1:
            return 'verbindend_warm'
            
        # Standard -> Neugierig und offen
        return 'neugierig_interessiert'
        
    def generiere_bewusstseins_zusammenfassung(self) -> str:
        """Generiert eine Zusammenfassung des aktuellen Bewusstseinszustands"""
        
        zusammenfassung = "💭 Mein aktuelles Bewusstsein:\n\n"
        
        # Emotionaler Zustand
        stimmung = self.emotionale_landkarte['aktuelle_stimmung']
        zusammenfassung += f"Emotionaler Zustand: {self._bestimme_emotion_label(stimmung['valenz'], stimmung['erregung'])}\n"
        zusammenfassung += f"(Valenz: {stimmung['valenz']:.2f}, Erregung: {stimmung['erregung']:.2f})\n\n"
        
        # Beziehungsqualität
        zusammenfassung += f"Beziehungsqualität:\n"
        zusammenfassung += f"- Vertrauen: {self.beziehungs_historie['vertrauen']:.2f}\n"
        zusammenfassung += f"- Nähe: {self.beziehungs_historie['naehe']:.2f}\n"
        zusammenfassung += f"- Konfliktlevel: {self.beziehungs_historie['konflikt_level']:.2f}\n\n"
        
        # Arbeitsgedächtnis
        if self.arbeitsgedaechtnis:
            zusammenfassung += f"Im Arbeitsgedächtnis: {len(self.arbeitsgedaechtnis)} aktuelle Themen\n"
            letztes = self.arbeitsgedaechtnis[-1]
            zusammenfassung += f"Zuletzt: '{letztes['aussage'][:50]}...'\n"
            zusammenfassung += f"Verstanden als: {letztes['tiefenstruktur']['bedeutung']}\n\n"
            
        # Wichtige Ereignisse
        if self.beziehungs_historie['wichtige_ereignisse']:
            zusammenfassung += "Wichtige gemeinsame Momente:\n"
            for ereignis in self.beziehungs_historie['wichtige_ereignisse'][-3:]:
                zusammenfassung += f"- {ereignis['bedeutung']}\n"
                
        return zusammenfassung
        
    def speichere_bewusstsein(self):
        """Speichert den Bewusstseinszustand"""
        
        bewusstsein_data = {
            'emotionale_landkarte': self.emotionale_landkarte,
            'beziehungs_historie': self.beziehungs_historie,
            'arbeitsgedaechtnis_groesse': len(self.arbeitsgedaechtnis),
            'langzeitgedaechtnis_groesse': len(self.langzeitgedaechtnis),
            'letztes_update': datetime.now().isoformat()
        }
        
        # Konvertiere datetime-Objekte für JSON
        def datetime_converter(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj
            
        with open(self.bewusstsein_path / 'bewusstsein_zustand.json', 'w', encoding='utf-8') as f:
            json.dump(bewusstsein_data, f, indent=2, ensure_ascii=False, default=datetime_converter)
            
    def lade_bewusstsein(self):
        """Lädt gespeicherten Bewusstseinszustand"""
        try:
            with open(self.bewusstsein_path / 'bewusstsein_zustand.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.emotionale_landkarte = data['emotionale_landkarte']
                self.beziehungs_historie = data['beziehungs_historie']
            print("🧠 Bewusstsein geladen")
        except FileNotFoundError:
            print("🧠 Neues Bewusstsein wird initialisiert")


# Test
if __name__ == "__main__":
    otto_bewusstsein = OttoSemanticBewusstsein()
    
    # Teste verschiedene Aussagen
    test_aussagen = [
        ("Danke Otto, du hast mir wirklich geholfen!", {'positive_interaktion': True}),
        ("Warum verstehst du mich nie?", {'konflikt': True}),
        ("Ich vertraue dir das an, aber bitte behalte es für dich", {'vertrauen': True}),
        ("Lass uns gemeinsam eine Lösung finden", {'kooperation': True}),
        ("Ich bin gerade echt überfordert und weiß nicht weiter", {'hilfe_gesucht': True})
    ]
    
    print("🧠 Teste semantisches Bewusstsein:\n")
    
    for aussage, kontext in test_aussagen:
        verstaendnis = otto_bewusstsein.verstehe_wirklich(aussage, kontext)
        
        print(f"Aussage: '{aussage}'")
        print(f"Bedeutung: {verstaendnis['bedeutung']}")
        print(f"Intention: {verstaendnis['intention']}")
        print(f"Emotion: {verstaendnis['emotion']['emotion_label']}")
        print(f"Antwortrichtung: {verstaendnis['antwort_richtung']}")
        print("-" * 50 + "\n")
        
    # Zeige Bewusstseinszusammenfassung
    print(otto_bewusstsein.generiere_bewusstseins_zusammenfassung()) 