"""
Base Agent für AI-Agenten im Frausar-System
===========================================

Grundlegende Agenten-Architektur mit Event-basierter Kommunikation
und modularer Struktur für einfache Erweiterbarkeit.
"""

import asyncio
import logging
import threading
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from pathlib import Path
import pandas as pd
from datetime import datetime

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Basis-Klasse für alle AI-Agenten im Frausar-System.
    
    Bietet:
    - Event-basierte Kommunikation
    - Asynchrone Verarbeitung
    - Logging und Error-Handling
    - Modulare Erweiterbarkeit
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialisiert einen neuen Agenten.
        
        Args:
            name: Name des Agenten
            config: Konfigurations-Dictionary
        """
        self.name = name
        self.config = config or {}
        self.status = "idle"  # idle, running, completed, error
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None
        
        # Event-basierte Kommunikation
        self._callbacks = {}
        self._lock = threading.Lock()
        
        logger.info(f"Agent {self.name} initialisiert")
    
    def register_callback(self, event: str, callback):
        """Registriert einen Callback für ein Event."""
        with self._lock:
            if event not in self._callbacks:
                self._callbacks[event] = []
            self._callbacks[event].append(callback)
    
    def _trigger_event(self, event: str, data: Any = None):
        """Löst ein Event aus und ruft alle registrierten Callbacks auf."""
        with self._lock:
            callbacks = self._callbacks.get(event, [])
        
        for callback in callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Fehler in Event-Callback {event}: {e}")
    
    @abstractmethod
    async def process(self, data: Any, **kwargs) -> Any:
        """
        Hauptverarbeitungsmethode - muss von Subklassen implementiert werden.
        
        Args:
            data: Eingabedaten für den Agenten
            **kwargs: Zusätzliche Parameter
            
        Returns:
            Verarbeitete Daten
        """
        pass
    
    async def run(self, data: Any, **kwargs) -> Dict[str, Any]:
        """
        Führt den Agenten aus mit vollständigem Error-Handling und Logging.
        
        Args:
            data: Eingabedaten
            **kwargs: Zusätzliche Parameter
            
        Returns:
            Dictionary mit Status, Ergebnis und Metadaten
        """
        self.start_time = datetime.now()
        self.status = "running"
        self.error = None
        
        logger.info(f"Agent {self.name} startet Verarbeitung")
        self._trigger_event("started", {"agent": self.name, "data": data})
        
        try:
            # Asynchrone Verarbeitung
            result = await self.process(data, **kwargs)
            
            self.status = "completed"
            self.result = result
            self.end_time = datetime.now()
            
            logger.info(f"Agent {self.name} erfolgreich abgeschlossen")
            self._trigger_event("completed", {
                "agent": self.name,
                "result": result,
                "duration": self.end_time - self.start_time
            })
            
            return {
                "status": "success",
                "agent": self.name,
                "result": result,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.end_time - self.start_time
            }
            
        except Exception as e:
            self.status = "error"
            self.error = str(e)
            self.end_time = datetime.now()
            
            logger.error(f"Agent {self.name} Fehler: {e}")
            self._trigger_event("error", {
                "agent": self.name,
                "error": str(e),
                "duration": self.end_time - self.start_time
            })
            
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e),
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.end_time - self.start_time
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Gibt den aktuellen Status des Agenten zurück."""
        return {
            "name": self.name,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "error": self.error,
            "has_result": self.result is not None
        }
    
    def reset(self):
        """Setzt den Agenten zurück in den Ausgangszustand."""
        self.status = "idle"
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None
        logger.info(f"Agent {self.name} zurückgesetzt")


class AgentResult:
    """Container für Agenten-Ergebnisse mit Metadaten."""
    
    def __init__(self, data: Any, metadata: Optional[Dict[str, Any]] = None):
        self.data = data
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert das Ergebnis in ein Dictionary."""
        return {
            "data": self.data,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        } 