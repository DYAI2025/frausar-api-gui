#!/usr/bin/env python3
"""
⏰ OTTO LEARNING SCHEDULER
============================================================
🎯 Automatischer Scheduler für Ottos Lernsystem
📝 Führt regelmäßige Lernzyklen durch
💎 Integriert mit dem Auto Learning System
⏰ Läuft kontinuierlich im Hintergrund
============================================================
"""

import time
import schedule
import threading
import logging
from datetime import datetime
import os
import sys

# Importiere das Auto Learning System
from otto_auto_learning_system import OttoAutoLearningSystem

class OttoLearningScheduler:
    def __init__(self):
        self.learning_system = OttoAutoLearningSystem()
        self.setup_logging()
        self.running = False
        
    def setup_logging(self):
        """Richtet Logging für den Scheduler ein"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('otto_compression_logs/scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_learning_cycle(self):
        """Führt einen Lernzyklus durch"""
        try:
            self.logger.info("🔄 Starte geplanten Lernzyklus...")
            self.learning_system.run_learning_cycle()
            self.logger.info("✅ Lernzyklus erfolgreich abgeschlossen")
        except Exception as e:
            self.logger.error(f"❌ Fehler im Lernzyklus: {e}")
    
    def setup_schedule(self):
        """Richtet den Zeitplan ein"""
        # Alle 2 Stunden einen Lernzyklus
        schedule.every(2).hours.do(self.run_learning_cycle)
        
        # Zusätzlich: Jeden Tag um 3 Uhr morgens
        schedule.every().day.at("03:00").do(self.run_learning_cycle)
        
        # Und jeden Sonntag um 12 Uhr eine gründliche Analyse
        schedule.every().sunday.at("12:00").do(self.run_deep_analysis)
        
        self.logger.info("📅 Zeitplan eingerichtet:")
        self.logger.info("   - Alle 2 Stunden: Standard-Lernzyklus")
        self.logger.info("   - Täglich 03:00: Tägliche Analyse")
        self.logger.info("   - Sonntags 12:00: Tiefenanalyse")
    
    def run_deep_analysis(self):
        """Führt eine gründliche Analyse durch"""
        try:
            self.logger.info("🔍 Starte Tiefenanalyse...")
            
            # Erweiterte Analyse mit mehr Details
            self.learning_system.run_learning_cycle()
            
            # Zusätzliche Statistiken
            self.generate_weekly_report()
            
            self.logger.info("✅ Tiefenanalyse abgeschlossen")
        except Exception as e:
            self.logger.error(f"❌ Fehler in Tiefenanalyse: {e}")
    
    def generate_weekly_report(self):
        """Generiert einen wöchentlichen Bericht"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'type': 'weekly_report',
                'summary': 'Wöchentliche Lernanalyse abgeschlossen'
            }
            
            report_file = f"otto_compression_logs/weekly_report_{datetime.now().strftime('%Y%m%d')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                import json
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📊 Wöchentlicher Bericht erstellt: {report_file}")
        except Exception as e:
            self.logger.error(f"❌ Fehler beim Erstellen des Berichts: {e}")
    
    def start_scheduler(self):
        """Startet den Scheduler"""
        self.running = True
        self.logger.info("🚀 Otto Learning Scheduler gestartet")
        
        # Führe sofort einen ersten Lernzyklus durch
        self.logger.info("🎯 Führe ersten Lernzyklus durch...")
        self.run_learning_cycle()
        
        # Starte den Scheduler-Loop
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Prüfe jede Minute
            except KeyboardInterrupt:
                self.logger.info("⏹️  Scheduler wird beendet...")
                self.running = False
                break
            except Exception as e:
                self.logger.error(f"❌ Fehler im Scheduler: {e}")
                time.sleep(300)  # Warte 5 Minuten bei Fehlern
    
    def stop_scheduler(self):
        """Stoppt den Scheduler"""
        self.running = False
        self.logger.info("⏹️  Scheduler gestoppt")

def main():
    """Hauptfunktion für den Learning Scheduler"""
    print("⏰ OTTO LEARNING SCHEDULER")
    print("=" * 60)
    print("🎯 Automatischer Scheduler für Ottos Lernsystem")
    print("📝 Führt regelmäßige Lernzyklen durch")
    print("💎 Integriert mit dem Auto Learning System")
    print("⏰ Läuft kontinuierlich im Hintergrund")
    print("=" * 60)
    
    # Erstelle und starte den Scheduler
    scheduler = OttoLearningScheduler()
    scheduler.setup_schedule()
    
    try:
        scheduler.start_scheduler()
    except KeyboardInterrupt:
        print("\n⏹️  Scheduler wird beendet...")
        scheduler.stop_scheduler()
    except Exception as e:
        print(f"❌ Fehler im Scheduler: {e}")
        scheduler.stop_scheduler()

if __name__ == "__main__":
    main() 