#!/usr/bin/env python3
"""
🧠 OTTO INTEGRATED LEARNING SYSTEM
============================================================
🎯 Integration des Auto Learning Systems in Ottos Hauptsystem
📝 Verbindet Jammeldateien, Marker und Kristalle
💎 Automatische Mustererkennung und Verdichtung
⏰ Läuft parallel zu Ottos Hauptprozess
============================================================
"""

import os
import json
import yaml
import time
import threading
from datetime import datetime
from typing import Dict, List, Any
import logging

# Importiere das Auto Learning System
from otto_auto_learning_system import OttoAutoLearningSystem

class OttoIntegratedLearning:
    def __init__(self):
        self.learning_system = OttoAutoLearningSystem()
        self.setup_logging()
        self.running = False
        self.learning_thread = None
        
    def setup_logging(self):
        """Richtet Logging für das integrierte Lernsystem ein"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('otto_compression_logs/integrated_learning.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def start_background_learning(self):
        """Startet das Lernsystem im Hintergrund"""
        self.running = True
        self.learning_thread = threading.Thread(target=self.learning_loop, daemon=True)
        self.learning_thread.start()
        self.logger.info("🔄 Hintergrund-Lernsystem gestartet")
    
    def stop_background_learning(self):
        """Stoppt das Hintergrund-Lernsystem"""
        self.running = False
        if self.learning_thread:
            self.learning_thread.join()
        self.logger.info("⏹️  Hintergrund-Lernsystem gestoppt")
    
    def learning_loop(self):
        """Hauptschleife für das Hintergrund-Lernen"""
        while self.running:
            try:
                # Prüfe auf neue Jammeldateien
                if self.check_for_new_jam_files():
                    self.logger.info("📝 Neue Jammeldateien gefunden - starte Lernzyklus")
                    self.learning_system.run_learning_cycle()
                
                # Warte 30 Minuten bis zur nächsten Prüfung
                time.sleep(1800)  # 30 Minuten
                
            except Exception as e:
                self.logger.error(f"❌ Fehler im Lernloop: {e}")
                time.sleep(300)  # Warte 5 Minuten bei Fehlern
    
    def check_for_new_jam_files(self) -> bool:
        """Prüft auf neue Jammeldateien"""
        jam_dir = "otto_jam_files"
        if not os.path.exists(jam_dir):
            return False
        
        # Prüfe auf Dateien, die in den letzten 30 Minuten erstellt wurden
        current_time = time.time()
        for filename in os.listdir(jam_dir):
            file_path = os.path.join(jam_dir, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if current_time - file_time < 1800:  # 30 Minuten
                    return True
        
        return False
    
    def process_realtime_jam(self, jam_content: str, jam_type: str = "conversation"):
        """Verarbeitet eine Jammeldatei in Echtzeit"""
        try:
            # Erstelle Jammeldatei
            jam_id = f"jam_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            jam_data = {
                'id': jam_id,
                'type': jam_type,
                'content': jam_content,
                'timestamp': datetime.now().isoformat(),
                'processed': False
            }
            
            # Speichere Jammeldatei
            jam_file = f"otto_jam_files/{jam_id}.json"
            with open(jam_file, 'w', encoding='utf-8') as f:
                json.dump(jam_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📝 Jammeldatei erstellt: {jam_id}")
            
            # Starte sofortigen Lernzyklus
            self.learning_system.run_learning_cycle()
            
            return jam_id
            
        except Exception as e:
            self.logger.error(f"❌ Fehler beim Verarbeiten der Jammeldatei: {e}")
            return None
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Gibt aktuelle Lern-Erkenntnisse zurück"""
        insights = {
            'crystals_count': 0,
            'clusters_count': 0,
            'recent_insights': [],
            'learning_stats': {}
        }
        
        try:
            # Zähle Kristalle
            crystals_dir = "otto_crystals"
            if os.path.exists(crystals_dir):
                crystal_files = [f for f in os.listdir(crystals_dir) if f.endswith('.json')]
                insights['crystals_count'] = len(crystal_files)
            
            # Zähle Cluster
            clusters_dir = "otto_clusters"
            if os.path.exists(clusters_dir):
                cluster_files = [f for f in os.listdir(clusters_dir) if f.endswith('.json')]
                insights['clusters_count'] = len(cluster_files)
            
            # Lade aktuelle Lernstatistiken
            stats_dir = "otto_compression_logs"
            if os.path.exists(stats_dir):
                stats_files = [f for f in os.listdir(stats_dir) if f.startswith('learning_stats_')]
                if stats_files:
                    latest_stats = max(stats_files)
                    stats_file = os.path.join(stats_dir, latest_stats)
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        insights['learning_stats'] = json.load(f)
            
        except Exception as e:
            self.logger.error(f"❌ Fehler beim Laden der Erkenntnisse: {e}")
        
        return insights
    
    def create_marker_from_insight(self, insight: Dict[str, Any]) -> str:
        """Erstellt einen neuen Marker aus einer Erkenntnis"""
        try:
            marker_id = f"marker_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            marker_data = {
                'id': marker_id,
                'created_at': datetime.now().isoformat(),
                'type': 'auto_generated',
                'insight': insight,
                'confidence': insight.get('confidence', 0.5)
            }
            
            # Speichere Marker
            marker_file = f"otto_markers/{marker_id}.yaml"
            with open(marker_file, 'w', encoding='utf-8') as f:
                yaml.dump(marker_data, f, default_flow_style=False, allow_unicode=True)
            
            self.logger.info(f"🎯 Neuer Marker erstellt: {marker_id}")
            return marker_id
            
        except Exception as e:
            self.logger.error(f"❌ Fehler beim Erstellen des Markers: {e}")
            return None
    
    def run_manual_learning_cycle(self):
        """Führt einen manuellen Lernzyklus durch"""
        try:
            self.logger.info("🎯 Starte manuellen Lernzyklus...")
            self.learning_system.run_learning_cycle()
            
            # Zeige Ergebnisse
            insights = self.get_learning_insights()
            self.logger.info(f"✅ Manueller Lernzyklus abgeschlossen:")
            self.logger.info(f"   💎 Kristalle: {insights['crystals_count']}")
            self.logger.info(f"   🎯 Cluster: {insights['clusters_count']}")
            
        except Exception as e:
            self.logger.error(f"❌ Fehler im manuellen Lernzyklus: {e}")

def main():
    """Hauptfunktion für das integrierte Lernsystem"""
    print("🧠 OTTO INTEGRATED LEARNING SYSTEM")
    print("=" * 60)
    print("🎯 Integration des Auto Learning Systems")
    print("📝 Verbindet Jammeldateien, Marker und Kristalle")
    print("💎 Automatische Mustererkennung und Verdichtung")
    print("⏰ Läuft parallel zu Ottos Hauptprozess")
    print("=" * 60)
    
    # Erstelle und starte das integrierte Lernsystem
    integrated_learning = OttoIntegratedLearning()
    
    try:
        # Starte Hintergrund-Lernen
        integrated_learning.start_background_learning()
        
        # Führe einen ersten Lernzyklus durch
        integrated_learning.run_manual_learning_cycle()
        
        # Halte das System am Laufen
        print("🔄 Integriertes Lernsystem läuft... (Strg+C zum Beenden)")
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n⏹️  Integriertes Lernsystem wird beendet...")
        integrated_learning.stop_background_learning()
    except Exception as e:
        print(f"❌ Fehler im integrierten Lernsystem: {e}")
        integrated_learning.stop_background_learning()

if __name__ == "__main__":
    main() 