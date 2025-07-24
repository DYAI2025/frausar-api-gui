"""
Config Service für Frausar-System
=================================

Zentrale Konfigurationsverwaltung für GUI und API.
Bietet einheitliche Konfigurationszugriffe.
"""

import logging
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)


class ConfigService:
    """
    Zentrale Konfigurationsverwaltung.
    
    Bietet:
    - Einheitliche Konfigurationszugriffe
    - Persistierung von Einstellungen
    - Validierung von Konfigurationen
    - Hot-Reloading von Konfigurationen
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialisiert den Config Service.
        
        Args:
            config_dir: Verzeichnis für Konfigurationsdateien
        """
        self.config_dir = config_dir or Path("Frausar_API_GUI/config")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Standard-Konfigurationen
        self._default_configs = {
            "agents": {
                "data_cleaning": {
                    "remove_columns_with_missing_threshold": 0.4,
                    "fill_numeric_with": "mean",
                    "fill_categorical_with": "mode",
                    "remove_duplicates": True,
                    "handle_outliers": True,
                    "outlier_threshold": 3.0,
                    "convert_dtypes": True,
                    "log_changes": True
                },
                "supervisor": {
                    "max_concurrent_agents": 3,
                    "timeout_seconds": 300,
                    "retry_attempts": 2
                }
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "cors_origins": ["*"]
            },
            "gui": {
                "theme": "default",
                "window_size": "800x600",
                "auto_save": True,
                "log_level": "INFO"
            },
            "data": {
                "upload_dir": "data/uploads",
                "result_dir": "data/results",
                "temp_dir": "data/temp",
                "max_file_size": 100 * 1024 * 1024  # 100MB
            }
        }
        
        # Geladene Konfigurationen
        self._configs = {}
        self._load_configs()
        
        logger.info(f"ConfigService initialisiert: {self.config_dir}")
    
    def _load_configs(self):
        """Lädt alle verfügbaren Konfigurationsdateien."""
        config_files = {
            "agents.yaml": "agents",
            "api.yaml": "api", 
            "gui.yaml": "gui",
            "data.yaml": "data"
        }
        
        for filename, config_key in config_files.items():
            file_path = self.config_dir / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if filename.endswith('.yaml'):
                            config = yaml.safe_load(f)
                        else:
                            config = json.load(f)
                    
                    self._configs[config_key] = config
                    logger.info(f"Konfiguration geladen: {filename}")
                    
                except Exception as e:
                    logger.error(f"Fehler beim Laden von {filename}: {e}")
                    # Fallback auf Standard-Konfiguration
                    self._configs[config_key] = self._default_configs[config_key]
            else:
                # Standard-Konfiguration verwenden
                self._configs[config_key] = self._default_configs[config_key]
                # Standard-Konfiguration speichern
                self._save_config(config_key, self._default_configs[config_key])
    
    def _save_config(self, config_key: str, config: Dict[str, Any]):
        """Speichert eine Konfiguration."""
        try:
            file_path = self.config_dir / f"{config_key}.yaml"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"Konfiguration gespeichert: {config_key}")
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Konfiguration {config_key}: {e}")
    
    def get_config(self, config_key: str, default: Any = None) -> Dict[str, Any]:
        """
        Gibt eine Konfiguration zurück.
        
        Args:
            config_key: Schlüssel der Konfiguration
            default: Standardwert falls nicht gefunden
            
        Returns:
            Konfigurations-Dictionary
        """
        return self._configs.get(config_key, default or {})
    
    def get_nested_config(self, config_key: str, *keys, default: Any = None) -> Any:
        """
        Gibt einen verschachtelten Konfigurationswert zurück.
        
        Args:
            config_key: Hauptschlüssel der Konfiguration
            *keys: Verschachtelte Schlüssel
            default: Standardwert falls nicht gefunden
            
        Returns:
            Konfigurationswert
        """
        config = self.get_config(config_key, {})
        
        for key in keys:
            if isinstance(config, dict) and key in config:
                config = config[key]
            else:
                return default
        
        return config
    
    def set_config(self, config_key: str, config: Dict[str, Any]):
        """
        Setzt eine Konfiguration.
        
        Args:
            config_key: Schlüssel der Konfiguration
            config: Neue Konfiguration
        """
        self._configs[config_key] = config
        self._save_config(config_key, config)
        
        logger.info(f"Konfiguration aktualisiert: {config_key}")
    
    def update_config(self, config_key: str, updates: Dict[str, Any]):
        """
        Aktualisiert eine bestehende Konfiguration.
        
        Args:
            config_key: Schlüssel der Konfiguration
            updates: Zu aktualisierende Werte
        """
        current_config = self.get_config(config_key, {})
        current_config.update(updates)
        self.set_config(config_key, current_config)
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Gibt die Konfiguration für einen spezifischen Agenten zurück.
        
        Args:
            agent_name: Name des Agenten
            
        Returns:
            Agenten-Konfiguration
        """
        return self.get_nested_config("agents", agent_name, default={})
    
    def set_agent_config(self, agent_name: str, config: Dict[str, Any]):
        """
        Setzt die Konfiguration für einen spezifischen Agenten.
        
        Args:
            agent_name: Name des Agenten
            config: Neue Konfiguration
        """
        agents_config = self.get_config("agents", {})
        agents_config[agent_name] = config
        self.set_config("agents", agents_config)
    
    def get_api_config(self) -> Dict[str, Any]:
        """Gibt die API-Konfiguration zurück."""
        return self.get_config("api")
    
    def get_gui_config(self) -> Dict[str, Any]:
        """Gibt die GUI-Konfiguration zurück."""
        return self.get_config("gui")
    
    def get_data_config(self) -> Dict[str, Any]:
        """Gibt die Daten-Konfiguration zurück."""
        return self.get_config("data")
    
    def reload_configs(self):
        """Lädt alle Konfigurationen neu."""
        self._load_configs()
        logger.info("Alle Konfigurationen neu geladen")
    
    def export_config(self, config_key: str, format: str = "yaml") -> str:
        """
        Exportiert eine Konfiguration als String.
        
        Args:
            config_key: Schlüssel der Konfiguration
            format: Export-Format (yaml, json)
            
        Returns:
            Konfiguration als String
        """
        config = self.get_config(config_key, {})
        
        if format.lower() == "json":
            return json.dumps(config, indent=2, ensure_ascii=False)
        else:
            return yaml.dump(config, default_flow_style=False, allow_unicode=True)
    
    def import_config(self, config_key: str, config_data: str, format: str = "yaml"):
        """
        Importiert eine Konfiguration aus einem String.
        
        Args:
            config_key: Schlüssel der Konfiguration
            config_data: Konfigurationsdaten als String
            format: Import-Format (yaml, json)
        """
        try:
            if format.lower() == "json":
                config = json.loads(config_data)
            else:
                config = yaml.safe_load(config_data)
            
            self.set_config(config_key, config)
            
        except Exception as e:
            logger.error(f"Fehler beim Importieren der Konfiguration {config_key}: {e}")
            raise
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Gibt eine Zusammenfassung aller Konfigurationen zurück."""
        summary = {
            "config_dir": str(self.config_dir),
            "total_configs": len(self._configs),
            "config_keys": list(self._configs.keys()),
            "last_modified": datetime.now().isoformat()
        }
        
        return summary


# Globale Instanz
_config_service = None

def get_config_service() -> ConfigService:
    """Gibt die globale ConfigService-Instanz zurück."""
    global _config_service
    if _config_service is None:
        _config_service = ConfigService()
    return _config_service 