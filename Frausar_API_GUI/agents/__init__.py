"""
AI-Agenten Module für Frausar-System
====================================

Dieses Modul enthält die Basis-Agenten-Architektur und spezialisierte Agenten
für Data Science Aufgaben.
"""

from .base_agent import BaseAgent
from .data_cleaning_agent import DataCleaningAgent
from .supervisor_agent import SupervisorAgent

__all__ = [
    'BaseAgent',
    'DataCleaningAgent', 
    'SupervisorAgent'
] 