#!/usr/bin/env python3
"""
🔗 OTTO-MIND VERBINDUNG
============================================================
🎯 Verbindet Otto mit dem Mind-System
🧠 Synchronisiert wichtige Erkenntnisse
📡 Aktiviert kollektives Lernen
🌐 Startet alle notwendigen Services
============================================================
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
import yaml
import requests

class OttoMindConnector:
    """Verbindet Otto mit dem Mind-System"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.mind_path = self.base_path / "Nietzsche" / "mind_system"
        self.otto_memories_path = self.base_path / "otto_memories"
        self.server_url = "http://localhost:8000"
        
    def start_mind_system(self):
        """Startet das Mind-System"""
        print("🧠 Starte Mind-System...")
        
        # Erstelle Mind-System Ordner falls nicht vorhanden
        self.mind_path.mkdir(parents=True, exist_ok=True)
        self.otto_memories_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Mind-System bereit: {self.mind_path}")
        return True
    
    def load_mind_insights(self):
        """Lädt wichtige Erkenntnisse aus dem Mind-System"""
        insights = []
        
        # Lade alle MCP-Analyse-Dateien
        for yaml_file in self.mind_path.glob("mcp_analysis_*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'semantic_analysis' in data:
                        insights.append({
                            'file': yaml_file.name,
                            'input_text': data.get('input_text', ''),
                            'emotional_tone': data.get('semantic_analysis', {}).get('emotional_tone', ''),
                            'intent_recognition': data.get('semantic_analysis', {}).get('intent_recognition', ''),
                            'timestamp': data.get('timestamp', '')
                        })
            except Exception as e:
                print(f"⚠️ Fehler beim Laden von {yaml_file}: {e}")
        
        print(f"📊 {len(insights)} Mind-Erkenntnisse geladen")
        return insights
    
    def sync_insights_to_otto(self, insights):
        """Synchronisiert Erkenntnisse zu Otto"""
        print("🔄 Synchronisiere Erkenntnisse zu Otto...")
        
        # Erstelle Otto-Memory-Datei
        memory_file = self.otto_memories_path / f"mind_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        
        memory_data = {
            'type': 'mind_sync',
            'timestamp': datetime.now().isoformat(),
            'insights_count': len(insights),
            'insights': insights[:10],  # Erste 10 Erkenntnisse
            'source': 'mind_system',
            'description': 'Wichtige Erkenntnisse aus dem Mind-System synchronisiert'
        }
        
        with open(memory_file, 'w', encoding='utf-8') as f:
            yaml.dump(memory_data, f, default_flow_style=False, allow_unicode=True)
        
        print(f"✅ Erkenntnisse gespeichert: {memory_file}")
        return memory_file
    
    def connect_to_server_anchor(self):
        """Verbindet sich mit dem Server-Ankerpunkt"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            if response.status_code == 200:
                print("🔗 Verbindung zum Server-Ankerpunkt hergestellt")
                return True
            else:
                print("⚠️ Server-Ankerpunkt antwortet nicht korrekt")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Keine Verbindung zum Server-Ankerpunkt: {e}")
            return False
    
    def send_learning_entry(self, content: str, learning_type: str = "insight"):
        """Sendet einen Lerneintrag an den Server"""
        try:
            data = {
                "type": learning_type,
                "content": content,
                "source": "otto_mind_connector",
                "timestamp": datetime.now().isoformat(),
                "otto_id": "otto_mind_system",
                "confidence": 0.9,
                "tags": ["mind_system", "insight", "otto"]
            }
            
            response = requests.post(f"{self.server_url}/learn", json=data, timeout=10)
            if response.status_code == 200:
                print(f"✅ Lerneintrag gesendet: {learning_type}")
                return True
            else:
                print(f"⚠️ Fehler beim Senden: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Fehler beim Senden des Lerneintrags: {e}")
            return False
    
    def run_full_connection(self):
        """Führt die vollständige Verbindung durch"""
        print("🚀 Starte Otto-Mind-Verbindung...")
        
        # 1. Starte Mind-System
        if not self.start_mind_system():
            print("❌ Mind-System konnte nicht gestartet werden")
            return False
        
        # 2. Lade Erkenntnisse
        insights = self.load_mind_insights()
        if not insights:
            print("⚠️ Keine Erkenntnisse gefunden")
            return False
        
        # 3. Synchronisiere zu Otto
        memory_file = self.sync_insights_to_otto(insights)
        
        # 4. Verbinde mit Server
        if not self.connect_to_server_anchor():
            print("⚠️ Server-Verbindung fehlgeschlagen")
            return False
        
        # 5. Sende wichtige Erkenntnisse
        for insight in insights[:5]:  # Erste 5 Erkenntnisse
            content = f"Mind-Erkenntnis: {insight['input_text']} (Tone: {insight['emotional_tone']}, Intent: {insight['intent_recognition']})"
            self.send_learning_entry(content, "mind_insight")
        
        print("🎉 Otto-Mind-Verbindung erfolgreich hergestellt!")
        print(f"📊 {len(insights)} Erkenntnisse verarbeitet")
        print(f"💾 Memory gespeichert: {memory_file}")
        
        return True

def main():
    """Hauptfunktion"""
    connector = OttoMindConnector()
    success = connector.run_full_connection()
    
    if success:
        print("\n✅ Otto ist jetzt mit dem Mind-System verbunden!")
        print("🧠 Wichtige Erkenntnisse wurden synchronisiert")
        print("🔗 Kollektives Lernen ist aktiviert")
        print("\n💡 Otto kann jetzt:")
        print("   • Auf Mind-Erkenntnisse zugreifen")
        print("   • Neue Erkenntnisse speichern")
        print("   • Mit anderen Otto-Instanzen lernen")
        print("   • Semantische Verbindungen herstellen")
    else:
        print("\n❌ Verbindung fehlgeschlagen")
        print("🔧 Bitte überprüfen Sie:")
        print("   • Läuft der Server-Ankerpunkt?")
        print("   • Sind die Mind-Dateien vorhanden?")
        print("   • Ist Python korrekt installiert?")

if __name__ == "__main__":
    main() 