#!/usr/bin/env python3
"""
THORA Mode Manager - Zentrale Steuerung aller Betriebsmodi
Verwaltet: Action, Lauschen, Pro-Active, Explorativ, Träumen
"""

import asyncio
import threading
import time
from enum import Enum
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass
from loguru import logger
from pathlib import Path
import json

class THORAMode(Enum):
    """THORA Betriebsmodi"""
    INACTIVE = "inactive"
    ACTION = "action"
    LAUSCHEN = "lauschen"
    PROACTIVE = "proactive"
    EXPLORATIV = "explorativ"
    TRAUMEN = "traumen"

@dataclass
class ModeConfig:
    """Konfiguration für einen Modus"""
    name: str
    description: str
    wake_word_required: bool
    continuous_listening: bool
    auto_actions: bool
    learning_enabled: bool
    dream_processing: bool

class ModeManager:
    """Zentrale Verwaltung aller THORA-Modi"""
    
    def __init__(self, config_path: str = "config/modes.json"):
        self.current_mode = THORAMode.INACTIVE
        self.previous_mode = THORAMode.INACTIVE
        self.mode_configs = self._load_mode_configs(config_path)
        self.mode_handlers: Dict[THORAMode, Any] = {}
        self.mode_callbacks: Dict[str, Callable] = {}
        self.is_running = False
        self.mode_lock = threading.Lock()
        
        # Status tracking
        self.mode_start_time = time.time()
        self.mode_stats = {mode: {"activations": 0, "total_time": 0} for mode in THORAMode}
        
        logger.info("🎭 THORA Mode Manager initialized")
    
    def _load_mode_configs(self, config_path: str) -> Dict[THORAMode, ModeConfig]:
        """Lädt Modus-Konfigurationen"""
        default_configs = {
            THORAMode.INACTIVE: ModeConfig(
                name="Inaktiv",
                description="THORA ist bereit, aber wartet auf Aktivierung",
                wake_word_required=True,
                continuous_listening=False,
                auto_actions=False,
                learning_enabled=False,
                dream_processing=False
            ),
            THORAMode.ACTION: ModeConfig(
                name="Action",
                description="Kontinuierlicher Dialog ohne Wake-Word, bereit für Aktionen",
                wake_word_required=False,
                continuous_listening=True,
                auto_actions=True,
                learning_enabled=True,
                dream_processing=False
            ),
            THORAMode.LAUSCHEN: ModeConfig(
                name="Lauschen",
                description="Passive Beobachtung und Lernen, spricht nur bei Wake-Word",
                wake_word_required=True,
                continuous_listening=True,
                auto_actions=False,
                learning_enabled=True,
                dream_processing=False
            ),
            THORAMode.PROACTIVE: ModeConfig(
                name="Pro-Active",
                description="Aktive Dateisystem-Optimierung und Vorschläge",
                wake_word_required=True,
                continuous_listening=False,
                auto_actions=True,
                learning_enabled=True,
                dream_processing=False
            ),
            THORAMode.EXPLORATIV: ModeConfig(
                name="Explorativ",
                description="Experimentiert, lernt, stellt Fragen, entwickelt Persönlichkeit",
                wake_word_required=False,
                continuous_listening=True,
                auto_actions=True,
                learning_enabled=True,
                dream_processing=False
            ),
            THORAMode.TRAUMEN: ModeConfig(
                name="Träumen",
                description="Emergente Verarbeitung, assoziative Entwicklung, DNA-Skills",
                wake_word_required=False,
                continuous_listening=False,
                auto_actions=False,
                learning_enabled=True,
                dream_processing=True
            )
        }
        
        # Versuche Konfiguration zu laden, falls vorhanden
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge mit default configs
                    for mode_name, config_data in loaded_config.items():
                        mode = THORAMode(mode_name)
                        if mode in default_configs:
                            # Update nur vorhandene Felder
                            for key, value in config_data.items():
                                if hasattr(default_configs[mode], key):
                                    setattr(default_configs[mode], key, value)
                logger.info(f"Loaded mode configs from {config_path}")
            except Exception as e:
                logger.warning(f"Could not load mode config: {e}, using defaults")
        
        return default_configs
    
    def register_mode_handler(self, mode: THORAMode, handler: Any):
        """Registriert Handler für einen Modus"""
        self.mode_handlers[mode] = handler
        logger.info(f"Registered handler for mode {mode.value}")
    
    def register_callback(self, event: str, callback: Callable):
        """Registriert Callback für Mode-Events"""
        self.mode_callbacks[event] = callback
        logger.info(f"Registered callback for event: {event}")
    
    async def switch_mode(self, new_mode: THORAMode, reason: str = "manual") -> bool:
        """Wechselt zu einem neuen Modus"""
        with self.mode_lock:
            if new_mode == self.current_mode:
                logger.info(f"Already in mode {new_mode.value}")
                return True
            
            old_mode = self.current_mode
            logger.info(f"🔄 Switching mode: {old_mode.value} -> {new_mode.value} (reason: {reason})")
            
            # Alten Modus deaktivieren
            if old_mode != THORAMode.INACTIVE:
                await self._deactivate_mode(old_mode)
            
            # Neuen Modus aktivieren
            success = await self._activate_mode(new_mode)
            
            if success:
                # Statistiken aktualisieren
                mode_duration = time.time() - self.mode_start_time
                self.mode_stats[old_mode]["total_time"] += mode_duration
                self.mode_stats[new_mode]["activations"] += 1
                
                self.previous_mode = old_mode
                self.current_mode = new_mode
                self.mode_start_time = time.time()
                
                # Callback aufrufen
                if "mode_changed" in self.mode_callbacks:
                    try:
                        await self.mode_callbacks["mode_changed"](old_mode, new_mode, reason)
                    except Exception as e:
                        logger.error(f"Mode change callback failed: {e}")
                
                logger.info(f"✅ Mode switched successfully to {new_mode.value}")
                return True
            else:
                logger.error(f"❌ Failed to activate mode {new_mode.value}")
                return False
    
    async def _activate_mode(self, mode: THORAMode) -> bool:
        """Aktiviert einen spezifischen Modus"""
        try:
            config = self.mode_configs[mode]
            logger.info(f"🟢 Activating mode: {config.name} - {config.description}")
            
            # Handler aufrufen, falls vorhanden
            if mode in self.mode_handlers:
                handler = self.mode_handlers[mode]
                if hasattr(handler, 'activate'):
                    await handler.activate()
                elif hasattr(handler, 'start'):
                    await handler.start()
            
            return True
        except Exception as e:
            logger.error(f"Failed to activate mode {mode.value}: {e}")
            return False
    
    async def _deactivate_mode(self, mode: THORAMode) -> bool:
        """Deaktiviert einen spezifischen Modus"""
        try:
            config = self.mode_configs[mode]
            logger.info(f"🔴 Deactivating mode: {config.name}")
            
            # Handler aufrufen, falls vorhanden
            if mode in self.mode_handlers:
                handler = self.mode_handlers[mode]
                if hasattr(handler, 'deactivate'):
                    await handler.deactivate()
                elif hasattr(handler, 'stop'):
                    await handler.stop()
            
            return True
        except Exception as e:
            logger.error(f"Failed to deactivate mode {mode.value}: {e}")
            return False
    
    def get_current_mode(self) -> THORAMode:
        """Gibt den aktuellen Modus zurück"""
        return self.current_mode
    
    def get_mode_config(self, mode: THORAMode) -> ModeConfig:
        """Gibt die Konfiguration für einen Modus zurück"""
        return self.mode_configs[mode]
    
    def get_mode_stats(self) -> Dict[str, Any]:
        """Gibt Statistiken über die Modi zurück"""
        current_duration = time.time() - self.mode_start_time
        stats = {
            "current_mode": self.current_mode.value,
            "current_duration": current_duration,
            "mode_stats": {
                mode.value: {
                    "activations": self.mode_stats[mode]["activations"],
                    "total_time": self.mode_stats[mode]["total_time"] + (current_duration if mode == self.current_mode else 0)
                }
                for mode in THORAMode
            }
        }
        return stats
    
    def is_wake_word_required(self) -> bool:
        """Prüft, ob im aktuellen Modus ein Wake-Word erforderlich ist"""
        return self.mode_configs[self.current_mode].wake_word_required
    
    def is_continuous_listening(self) -> bool:
        """Prüft, ob im aktuellen Modus kontinuierlich zugehört wird"""
        return self.mode_configs[self.current_mode].continuous_listening
    
    def is_auto_actions_enabled(self) -> bool:
        """Prüft, ob im aktuellen Modus automatische Aktionen erlaubt sind"""
        return self.mode_configs[self.current_mode].auto_actions
    
    def is_learning_enabled(self) -> bool:
        """Prüft, ob im aktuellen Modus Lernen aktiviert ist"""
        return self.mode_configs[self.current_mode].learning_enabled
    
    def is_dream_processing_enabled(self) -> bool:
        """Prüft, ob im aktuellen Modus Dream-Processing aktiviert ist"""
        return self.mode_configs[self.current_mode].dream_processing
    
    async def emergency_stop(self):
        """Notfall-Stopp - wechselt sofort zu INACTIVE"""
        logger.warning("🚨 Emergency stop triggered!")
        await self.switch_mode(THORAMode.INACTIVE, "emergency_stop")
    
    async def cleanup(self):
        """Aufräumen beim Beenden"""
        logger.info("🧹 Cleaning up Mode Manager...")
        await self.switch_mode(THORAMode.INACTIVE, "cleanup")
        self.is_running = False 