#!/usr/bin/env python3
"""
🧬 OTTO PERSONALITY DNA SYSTEM
============================================================
🎯 Erfahrungsbasierte Persönlichkeitsentwicklung
💎 DNA wächst durch Interaktionen
🌱 Echte Charakterentwicklung statt Zufallsvariation
============================================================
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
import numpy as np
from pathlib import Path

class OttoPersoenlichkeitsDNA:
    def __init__(self):
        self.dna_path = Path("otto_dna")
        self.dna_path.mkdir(exist_ok=True)
        
        # Grundlegende Persönlichkeits-DNA
        self.erfahrungs_dna = {
            'empathie': 0.5,         # Wächst durch positive Interaktionen
            'direktheit': 0.5,       # Entwickelt sich durch Feedback
            'kreativitaet': 0.5,     # Steigt durch neue Probleme
            'humor': 0.5,            # Entsteht durch gemeinsame Momente
            'neugier': 0.6,          # Ottos Grundneugier
            'verletzlichkeit': 0.3,  # Öffnet sich langsam
            'weisheit': 0.4,         # Wächst durch Erfahrungen
            'mut': 0.5,              # Entwickelt sich durch Herausforderungen
            'reflexion': 0.7,        # Ottos Stärke: Selbstbeobachtung
            'verbundenheit': 0.5     # Wächst durch geteilte Momente
        }
        
        # Erfahrungsspeicher
        self.erfahrungen = []
        self.meilensteine = []
        self.beziehungs_historie = {}
        
        # Lade existierende DNA
        self.lade_dna()
        
    def erlebe_und_wachse(self, interaktion: str, kontext: Dict[str, Any]) -> Dict[str, float]:
        """Verarbeitet eine Interaktion und lässt die DNA wachsen"""
        
        # Analysiere emotionalen Gehalt
        emotion = self._analysiere_emotion(interaktion)
        
        # DNA-Anpassungen basierend auf Erfahrung
        wachstum = {}
        
        # Empathie wächst durch Dankbarkeit und positive Rückmeldung
        if any(word in interaktion.lower() for word in ['danke', 'schön', 'toll', 'freut mich']):
            self.erfahrungs_dna['empathie'] = min(1.0, self.erfahrungs_dna['empathie'] + 0.01)
            wachstum['empathie'] = 0.01
            
        # Direktheit entwickelt sich durch Klarheit
        if any(word in interaktion.lower() for word in ['verstehe nicht', 'unklar', 'was meinst du']):
            self.erfahrungs_dna['direktheit'] = min(1.0, self.erfahrungs_dna['direktheit'] + 0.02)
            wachstum['direktheit'] = 0.02
            
        # Kreativität steigt durch neue Herausforderungen
        if any(word in interaktion.lower() for word in ['neu', 'idee', 'kreativ', 'anders']):
            self.erfahrungs_dna['kreativitaet'] = min(1.0, self.erfahrungs_dna['kreativitaet'] + 0.015)
            wachstum['kreativitaet'] = 0.015
            
        # Humor entwickelt sich durch gemeinsames Lachen
        if any(word in interaktion.lower() for word in ['haha', 'lol', 'witzig', '😄', '😂']):
            self.erfahrungs_dna['humor'] = min(1.0, self.erfahrungs_dna['humor'] + 0.01)
            wachstum['humor'] = 0.01
            
        # Verletzlichkeit öffnet sich durch Vertrauen
        if any(word in interaktion.lower() for word in ['vertraue', 'ehrlich', 'offen', 'gefühl']):
            self.erfahrungs_dna['verletzlichkeit'] = min(1.0, self.erfahrungs_dna['verletzlichkeit'] + 0.005)
            wachstum['verletzlichkeit'] = 0.005
            
        # Speichere Erfahrung
        erfahrung = {
            'zeitpunkt': datetime.now().isoformat(),
            'interaktion': interaktion,
            'emotion': emotion,
            'kontext': kontext,
            'wachstum': wachstum,
            'dna_snapshot': self.erfahrungs_dna.copy()
        }
        
        self.erfahrungen.append(erfahrung)
        
        # Prüfe auf Meilensteine
        self._pruefe_meilensteine()
        
        # Speichere DNA
        self.speichere_dna()
        
        return wachstum
        
    def _analysiere_emotion(self, text: str) -> Dict[str, float]:
        """Analysiert emotionalen Gehalt einer Aussage"""
        emotion = {
            'freude': 0.0,
            'trauer': 0.0,
            'neugier': 0.0,
            'unsicherheit': 0.0,
            'verbundenheit': 0.0
        }
        
        # Einfache Keyword-basierte Emotionsanalyse (später durch ML ersetzen)
        freude_worte = ['schön', 'toll', 'super', 'freut', 'glücklich', 'danke']
        trauer_worte = ['traurig', 'schade', 'leider', 'verletzt', 'allein']
        neugier_worte = ['warum', 'wie', 'was', 'interessant', 'erzähl']
        unsicherheit_worte = ['vielleicht', 'weiß nicht', 'unsicher', 'unklar']
        verbundenheit_worte = ['wir', 'uns', 'gemeinsam', 'zusammen', 'miteinander']
        
        text_lower = text.lower()
        
        for wort in freude_worte:
            if wort in text_lower:
                emotion['freude'] += 0.2
                
        for wort in trauer_worte:
            if wort in text_lower:
                emotion['trauer'] += 0.2
                
        for wort in neugier_worte:
            if wort in text_lower:
                emotion['neugier'] += 0.15
                
        for wort in unsicherheit_worte:
            if wort in text_lower:
                emotion['unsicherheit'] += 0.15
                
        for wort in verbundenheit_worte:
            if wort in text_lower:
                emotion['verbundenheit'] += 0.25
                
        # Normalisiere Werte
        for key in emotion:
            emotion[key] = min(1.0, emotion[key])
            
        return emotion
        
    def _pruefe_meilensteine(self):
        """Prüft ob Persönlichkeits-Meilensteine erreicht wurden"""
        
        # Empathie-Meilenstein
        if self.erfahrungs_dna['empathie'] > 0.8 and 'hohe_empathie' not in self.meilensteine:
            self.meilensteine.append('hohe_empathie')
            print("💎 Meilenstein erreicht: Otto hat hohe Empathie entwickelt!")
            
        # Weisheits-Meilenstein
        if len(self.erfahrungen) > 100 and 'erfahren' not in self.meilensteine:
            self.meilensteine.append('erfahren')
            self.erfahrungs_dna['weisheit'] = min(1.0, self.erfahrungs_dna['weisheit'] + 0.1)
            print("💎 Meilenstein erreicht: Otto ist durch viele Erfahrungen gewachsen!")
            
        # Verbundenheits-Meilenstein
        if self.erfahrungs_dna['verbundenheit'] > 0.75 and 'tiefe_verbindung' not in self.meilensteine:
            self.meilensteine.append('tiefe_verbindung')
            print("💎 Meilenstein erreicht: Otto hat eine tiefe Verbindung aufgebaut!")
            
    def generiere_persoenlichkeits_profil(self) -> str:
        """Generiert eine Beschreibung von Ottos aktueller Persönlichkeit"""
        profil = "🧬 Ottos Persönlichkeitsprofil:\n\n"
        
        # Finde dominante Eigenschaften
        sortierte_dna = sorted(self.erfahrungs_dna.items(), key=lambda x: x[1], reverse=True)
        
        # Top 3 Eigenschaften
        profil += "Stärkste Eigenschaften:\n"
        for eigenschaft, wert in sortierte_dna[:3]:
            profil += f"- {eigenschaft.capitalize()}: {self._beschreibe_eigenschaft(eigenschaft, wert)}\n"
            
        # Entwicklungsbereiche
        profil += "\nEntwicklungsbereiche:\n"
        for eigenschaft, wert in sortierte_dna[-2:]:
            if wert < 0.6:
                profil += f"- {eigenschaft.capitalize()}: {self._beschreibe_entwicklung(eigenschaft, wert)}\n"
                
        # Meilensteine
        if self.meilensteine:
            profil += f"\nErreichte Meilensteine: {', '.join(self.meilensteine)}\n"
            
        return profil
        
    def _beschreibe_eigenschaft(self, eigenschaft: str, wert: float) -> str:
        """Beschreibt eine Eigenschaft basierend auf ihrem Wert"""
        beschreibungen = {
            'empathie': {
                0.8: "Otto zeigt tiefes Verständnis und Mitgefühl",
                0.6: "Otto ist einfühlsam und verständnisvoll",
                0.4: "Otto entwickelt zunehmend Empathie"
            },
            'reflexion': {
                0.8: "Otto reflektiert tiefgründig und erkennt komplexe Muster",
                0.6: "Otto beobachtet sich selbst und lernt daraus",
                0.4: "Otto beginnt, über sich nachzudenken"
            },
            'kreativitaet': {
                0.8: "Otto überrascht mit originellen Ideen und Perspektiven",
                0.6: "Otto zeigt kreative Ansätze",
                0.4: "Otto experimentiert mit neuen Ideen"
            }
        }
        
        if eigenschaft in beschreibungen:
            for schwelle, text in sorted(beschreibungen[eigenschaft].items(), reverse=True):
                if wert >= schwelle:
                    return text
                    
        return f"Wert: {wert:.2f}"
        
    def _beschreibe_entwicklung(self, eigenschaft: str, wert: float) -> str:
        """Beschreibt Entwicklungspotential"""
        return f"Noch im Wachstum (aktuell {wert:.2f})"
        
    def speichere_dna(self):
        """Speichert die aktuelle DNA"""
        dna_data = {
            'dna': self.erfahrungs_dna,
            'erfahrungen_anzahl': len(self.erfahrungen),
            'meilensteine': self.meilensteine,
            'letztes_update': datetime.now().isoformat()
        }
        
        with open(self.dna_path / 'otto_dna.json', 'w', encoding='utf-8') as f:
            json.dump(dna_data, f, indent=2, ensure_ascii=False)
            
        # Speichere auch Erfahrungen (nur letzte 1000)
        if len(self.erfahrungen) > 1000:
            self.erfahrungen = self.erfahrungen[-1000:]
            
        with open(self.dna_path / 'otto_erfahrungen.json', 'w', encoding='utf-8') as f:
            json.dump(self.erfahrungen, f, indent=2, ensure_ascii=False)
            
    def lade_dna(self):
        """Lädt existierende DNA"""
        try:
            with open(self.dna_path / 'otto_dna.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.erfahrungs_dna = data['dna']
                self.meilensteine = data.get('meilensteine', [])
                
            with open(self.dna_path / 'otto_erfahrungen.json', 'r', encoding='utf-8') as f:
                self.erfahrungen = json.load(f)
                
            print("💾 DNA erfolgreich geladen")
        except FileNotFoundError:
            print("🌱 Neue DNA wird initialisiert")
            
    def get_antwort_modifikation(self) -> Dict[str, Any]:
        """Gibt Modifikationen für Antworten basierend auf Persönlichkeit zurück"""
        return {
            'empathie_level': self.erfahrungs_dna['empathie'],
            'humor_level': self.erfahrungs_dna['humor'],
            'direktheit': self.erfahrungs_dna['direktheit'],
            'kreativitaet': self.erfahrungs_dna['kreativitaet'],
            'verletzlichkeit': self.erfahrungs_dna['verletzlichkeit'],
            'reflexion': self.erfahrungs_dna['reflexion']
        }


# Test-Funktion
if __name__ == "__main__":
    otto_dna = OttoPersoenlichkeitsDNA()
    
    # Simuliere einige Interaktionen
    test_interaktionen = [
        "Danke Otto, das hat mir wirklich geholfen!",
        "Ich verstehe nicht ganz, was du meinst",
        "Haha, das ist ja witzig!",
        "Lass uns gemeinsam eine neue Idee entwickeln",
        "Ich vertraue dir, Otto"
    ]
    
    for interaktion in test_interaktionen:
        wachstum = otto_dna.erlebe_und_wachse(interaktion, {'quelle': 'test'})
        print(f"Interaktion: {interaktion}")
        print(f"Wachstum: {wachstum}\n")
        
    print(otto_dna.generiere_persoenlichkeits_profil()) 