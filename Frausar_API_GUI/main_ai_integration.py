#!/usr/bin/env python3
"""
Hauptskript für Frausar AI-Integration
======================================

Startet sowohl die GUI als auch die FastAPI parallel.
Bietet eine einheitliche Schnittstelle für beide Frontends.
"""

import sys
import os
import asyncio
import threading
import logging
import signal
from pathlib import Path
from typing import Optional

# Pfad für Imports - Wichtig für relative Imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(project_root))

# Services importieren
try:
    from services import get_data_service, get_agent_service, get_config_service
    from agents import DataCleaningAgent, SupervisorAgent
except ImportError as e:
    print(f"Import-Fehler: {e}")
    print(f"Current dir: {current_dir}")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

# FastAPI importieren
try:
    from api.main import app
    import uvicorn
except ImportError as e:
    print(f"FastAPI Import-Fehler: {e}")
    sys.exit(1)

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrausarAIIntegration:
    """
    Hauptklasse für die AI-Integration.
    
    Verwaltet:
    - FastAPI-Server
    - GUI-Integration
    - Service-Koordination
    - Graceful Shutdown
    """
    
    def __init__(self):
        """Initialisiert die AI-Integration."""
        self.config_service = get_config_service()
        self.data_service = get_data_service()
        self.agent_service = get_agent_service()
        
        # Server-Instanzen
        self.api_server = None
        self.api_thread = None
        self.gui_thread = None
        
        # Shutdown-Flag
        self.shutdown_event = threading.Event()
        
        # Signal-Handler
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("Frausar AI-Integration initialisiert")
    
    def _signal_handler(self, signum, frame):
        """Signal-Handler für Graceful Shutdown."""
        logger.info(f"Signal {signum} empfangen - Starte Graceful Shutdown")
        self.shutdown()
    
    def start_api_server(self):
        """Startet den FastAPI-Server in einem separaten Thread."""
        try:
            api_config = self.config_service.get_api_config()
            host = api_config.get("host", "0.0.0.0")
            port = api_config.get("port", 8000)
            debug = api_config.get("debug", False)
            
            logger.info(f"Starte FastAPI-Server auf {host}:{port}")
            
            # Uvicorn-Server konfigurieren
            config = uvicorn.Config(
                app=app,
                host=host,
                port=port,
                log_level="info" if debug else "warning",
                access_log=True
            )
            
            self.api_server = uvicorn.Server(config)
            
            # Server in separatem Thread starten
            self.api_thread = threading.Thread(
                target=self._run_api_server,
                daemon=True
            )
            self.api_thread.start()
            
            logger.info("FastAPI-Server erfolgreich gestartet")
            
        except Exception as e:
            logger.error(f"Fehler beim Starten des API-Servers: {e}")
            raise
    
    def _run_api_server(self):
        """Interne Methode zum Ausführen des API-Servers."""
        try:
            self.api_server.run()
        except Exception as e:
            logger.error(f"API-Server Fehler: {e}")
    
    def start_gui(self):
        """Startet die GUI-Integration."""
        try:
            # TODO: GUI-Integration implementieren
            # Für Phase 1: Stub-Implementierung
            logger.info("GUI-Integration wird in Phase 2 implementiert")
            
            # GUI-Thread simulieren
            self.gui_thread = threading.Thread(
                target=self._run_gui_stub,
                daemon=True
            )
            self.gui_thread.start()
            
        except Exception as e:
            logger.error(f"Fehler beim Starten der GUI: {e}")
            raise
    
    def _run_gui_stub(self):
        """Stub-Implementierung für GUI."""
        logger.info("GUI-Stub läuft - GUI-Integration folgt in Phase 2")
        
        # Einfache Konsolen-Interface für Phase 1
        while not self.shutdown_event.is_set():
            try:
                print("\n" + "="*50)
                print("Frausar AI-Integration - Phase 1")
                print("="*50)
                print("1. API-Status anzeigen")
                print("2. Agenten-Status anzeigen")
                print("3. Daten-Status anzeigen")
                print("4. Demo-Datenbereinigung starten")
                print("5. Beenden")
                print("="*50)
                
                choice = input("Wähle eine Option (1-5): ").strip()
                
                if choice == "1":
                    self._show_api_status()
                elif choice == "2":
                    self._show_agent_status()
                elif choice == "3":
                    self._show_data_status()
                elif choice == "4":
                    import asyncio
                    asyncio.run(self._run_demo_cleaning())
                elif choice == "5":
                    self.shutdown()
                    break
                else:
                    print("Ungültige Option!")
                    
            except KeyboardInterrupt:
                self.shutdown()
                break
            except Exception as e:
                logger.error(f"Fehler in GUI-Stub: {e}")
    
    def _show_api_status(self):
        """Zeigt API-Status an."""
        try:
            import requests
            response = requests.get("http://localhost:8000/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                print(f"\nAPI-Status: {status['system_status']}")
                print(f"Version: {status['api_version']}")
                print(f"Uptime: {status['uptime']:.1f} Sekunden")
                print(f"Aktive Agenten: {status['active_agents']}")
            else:
                print(f"API-Fehler: {response.status_code}")
        except Exception as e:
            print(f"API nicht erreichbar: {e}")
    
    def _show_agent_status(self):
        """Zeigt Agenten-Status an."""
        summary = self.agent_service.get_agent_summary()
        print(f"\nAgenten-Status:")
        print(f"Gesamt: {summary['total_agents']}")
        print(f"Status-Verteilung: {summary['status_counts']}")
        
        for name, info in summary['agents'].items():
            print(f"  {name}: {info['status']} ({info['type']})")
    
    def _show_data_status(self):
        """Zeigt Daten-Status an."""
        summary = self.data_service.get_data_summary()
        print(f"\nDaten-Status:")
        print(f"Einträge: {summary['total_entries']}")
        print(f"Datentypen: {summary['data_types']}")
        
        if summary['recent_entries']:
            print("Letzte Einträge:")
            for entry in summary['recent_entries'][:5]:
                print(f"  {entry['key']}: {entry['type']} ({entry['timestamp']})")
    
    async def _run_demo_cleaning(self):
        """Führt eine Demo-Datenbereinigung durch."""
        try:
            demo_file = Path("Frausar_API_GUI/data/demo_data.csv")
            if not demo_file.exists():
                print("Demo-Datei nicht gefunden!")
                return
            
            print(f"\nStarte Demo-Datenbereinigung für: {demo_file}")
            
            # Agenten ausführen
            result = await self.agent_service.run_agent("data_cleaning", demo_file)
            
            if result["status"] == "success":
                print("✅ Datenbereinigung erfolgreich!")
                print(f"Original: {result['result'].metadata['original_shape']}")
                print(f"Bereinigt: {result['result'].metadata['cleaned_shape']}")
                print(f"Änderungen: {len(result['result'].metadata['changes_log'])}")
                
                # Daten speichern
                cleaned_df = result["result"].data
                output_file = Path("Frausar_API_GUI/data/cleaned_demo_data.csv")
                cleaned_df.to_csv(output_file, index=False)
                print(f"Bereinigte Daten gespeichert: {output_file}")
                
            else:
                print(f"❌ Datenbereinigung fehlgeschlagen: {result['error']}")
                
        except Exception as e:
            print(f"❌ Fehler bei Demo-Bereinigung: {e}")
    
    def start(self):
        """Startet die gesamte AI-Integration."""
        try:
            logger.info("Starte Frausar AI-Integration...")
            
            # Services initialisieren
            logger.info("Initialisiere Services...")
            
            # API-Server starten
            self.start_api_server()
            
            # GUI starten
            self.start_gui()
            
            logger.info("Frausar AI-Integration erfolgreich gestartet")
            logger.info("API verfügbar unter: http://localhost:8000")
            logger.info("API-Docs verfügbar unter: http://localhost:8000/docs")
            
            # Hauptschleife
            try:
                while not self.shutdown_event.is_set():
                    self.shutdown_event.wait(1)
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt empfangen")
                self.shutdown()
            
        except Exception as e:
            logger.error(f"Fehler beim Starten der AI-Integration: {e}")
            self.shutdown()
            raise
    
    def shutdown(self):
        """Führt Graceful Shutdown durch."""
        logger.info("Starte Graceful Shutdown...")
        
        # Shutdown-Event setzen
        self.shutdown_event.set()
        
        # API-Server stoppen
        if self.api_server:
            logger.info("Stoppe API-Server...")
            self.api_server.should_exit = True
        
        # Threads warten
        if self.api_thread and self.api_thread.is_alive():
            self.api_thread.join(timeout=5)
        
        if self.gui_thread and self.gui_thread.is_alive():
            self.gui_thread.join(timeout=5)
        
        logger.info("Graceful Shutdown abgeschlossen")
        sys.exit(0)


def main():
    """Hauptfunktion."""
    try:
        # Logs-Verzeichnis erstellen
        log_dir = Path("Frausar_API_GUI/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # AI-Integration starten
        integration = FrausarAIIntegration()
        integration.start()
        
    except Exception as e:
        logger.error(f"Kritischer Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 