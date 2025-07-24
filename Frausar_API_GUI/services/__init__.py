"""
Shared Services für Frausar-System
==================================

Gemeinsame Services für GUI und API mit:
- Datenhaltung
- Agenten-Management
- Event-Handling
- Konfigurations-Management
"""

from .data_service import DataService, get_data_service
from .agent_service import AgentService, get_agent_service
from .config_service import ConfigService, get_config_service

__all__ = [
    'DataService',
    'AgentService', 
    'ConfigService',
    'get_data_service',
    'get_agent_service',
    'get_config_service'
] 