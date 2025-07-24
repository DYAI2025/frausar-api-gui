"""
Agent Service für Frausar-System
================================

Zentrale Verwaltung und Koordination der AI-Agenten.
Bietet einheitliche Schnittstelle für GUI und API.
"""

import logging
import threading
import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# Absoluten Import-Pfad hinzufügen
sys.path.append(str(Path(__file__).parent.parent))

from agents import DataCleaningAgent, SupervisorAgent, BaseAgent

logger = logging.getLogger(__name__)


class AgentService:
    """
    Zentrale Verwaltung der AI-Agenten.
    
    Bietet:
    - Agenten-Registrierung und -Verwaltung
    - Einheitliche Ausführungsschnittstelle
    - Status-Monitoring
    - Event-Handling
    """
    
    def __init__(self):
        """Initialisiert den Agent Service."""
        self._lock = threading.RLock()
        self._agents = {}
        self._supervisor = SupervisorAgent()
        self._callbacks = {}
        
        # Standard-Agenten registrieren
        self._register_default_agents()
        
        logger.info("AgentService initialisiert")
    
    def _register_default_agents(self):
        """Registriert die Standard-Agenten."""
        # Data Cleaning Agent
        data_cleaning_agent = DataCleaningAgent()
        self.register_agent("data_cleaning", data_cleaning_agent)
        
        logger.info("Standard-Agenten registriert")
    
    def register_callback(self, event: str, callback):
        """Registriert einen Callback für ein Event."""
        with self._lock:
            if event not in self._callbacks:
                self._callbacks[event] = []
            self._callbacks[event].append(callback)
    
    def _trigger_event(self, event: str, data: Any = None):
        """Löst ein Event aus."""
        with self._lock:
            callbacks = self._callbacks.get(event, [])
        
        for callback in callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Fehler in Event-Callback {event}: {e}")
    
    def register_agent(self, name: str, agent: BaseAgent):
        """
        Registriert einen neuen Agenten.
        
        Args:
            name: Eindeutiger Name des Agenten
            agent: Agenten-Instanz
        """
        with self._lock:
            self._agents[name] = agent
            self._supervisor.register_agent(agent)
        
        logger.info(f"Agent registriert: {name} ({agent.__class__.__name__})")
        self._trigger_event("agent_registered", {"name": name, "type": agent.__class__.__name__})
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Gibt einen Agenten zurück."""
        with self._lock:
            return self._agents.get(name)
    
    def list_agents(self) -> List[str]:
        """Gibt alle verfügbaren Agenten-Namen zurück."""
        with self._lock:
            return list(self._agents.keys())
    
    def get_agent_status(self, name: str) -> Optional[Dict[str, Any]]:
        """Gibt den Status eines Agenten zurück."""
        agent = self.get_agent(name)
        if agent:
            return agent.get_status()
        return None
    
    def get_all_agent_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Gibt den Status aller Agenten zurück."""
        with self._lock:
            return {name: agent.get_status() for name, agent in self._agents.items()}
    
    async def run_agent(self, agent_name: str, data: Any, **kwargs) -> Dict[str, Any]:
        """
        Führt einen Agenten aus.
        
        Args:
            agent_name: Name des Agenten
            data: Eingabedaten
            **kwargs: Zusätzliche Parameter
            
        Returns:
            Ergebnis des Agenten
        """
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent nicht gefunden: {agent_name}")
        
        logger.info(f"Starte Agent: {agent_name}")
        self._trigger_event("agent_started", {"name": agent_name})
        
        try:
            result = await agent.run(data, **kwargs)
            
            if result["status"] == "success":
                self._trigger_event("agent_completed", {
                    "name": agent_name,
                    "result": result
                })
            else:
                self._trigger_event("agent_error", {
                    "name": agent_name,
                    "error": result["error"]
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Fehler beim Ausführen von Agent {agent_name}: {e}")
            self._trigger_event("agent_error", {
                "name": agent_name,
                "error": str(e)
            })
            raise
    
    def reset_agent(self, agent_name: str):
        """Setzt einen Agenten zurück."""
        agent = self.get_agent(agent_name)
        if agent:
            agent.reset()
            logger.info(f"Agent zurückgesetzt: {agent_name}")
            self._trigger_event("agent_reset", {"name": agent_name})
    
    def reset_all_agents(self):
        """Setzt alle Agenten zurück."""
        with self._lock:
            for agent in self._agents.values():
                agent.reset()
        
        logger.info("Alle Agenten zurückgesetzt")
        self._trigger_event("all_agents_reset")
    
    def get_supervisor(self) -> SupervisorAgent:
        """Gibt den Supervisor Agent zurück."""
        return self._supervisor
    
    def get_agent_summary(self) -> Dict[str, Any]:
        """Gibt eine Zusammenfassung aller Agenten zurück."""
        with self._lock:
            summary = {
                "total_agents": len(self._agents),
                "agent_types": {},
                "status_counts": {
                    "idle": 0,
                    "running": 0,
                    "completed": 0,
                    "error": 0
                },
                "agents": {}
            }
            
            for name, agent in self._agents.items():
                agent_type = agent.__class__.__name__
                if agent_type not in summary["agent_types"]:
                    summary["agent_types"][agent_type] = 0
                summary["agent_types"][agent_type] += 1
                
                status = agent.status
                summary["status_counts"][status] += 1
                
                summary["agents"][name] = {
                    "type": agent_type,
                    "status": status,
                    "has_result": agent.result is not None
                }
            
            return summary


# Globale Instanz
_agent_service = None

def get_agent_service() -> AgentService:
    """Gibt die globale AgentService-Instanz zurück."""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service 