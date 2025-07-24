"""
Data Service für Frausar-System
===============================

Zentrale Datenhaltung und -verwaltung für GUI und API.
Bietet thread-sichere Zugriffe auf geteilte Daten.
"""

import logging
import threading
import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class DataService:
    """
    Zentrale Datenhaltung für das Frausar-System.
    
    Bietet:
    - Thread-sichere Datenzugriffe
    - Event-basierte Updates
    - Persistierung von Ergebnissen
    - Metadaten-Verwaltung
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialisiert den Data Service.
        
        Args:
            data_dir: Verzeichnis für Daten-Persistierung
        """
        self.data_dir = data_dir or Path("Frausar_API_GUI/data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Thread-sichere Datenhaltung
        self._lock = threading.RLock()
        self._data = {}
        self._metadata = {}
        self._callbacks = {}
        
        # Verzeichnisse erstellen
        self.upload_dir = self.data_dir / "uploads"
        self.result_dir = self.data_dir / "results"
        self.temp_dir = self.data_dir / "temp"
        
        for dir_path in [self.upload_dir, self.result_dir, self.temp_dir]:
            dir_path.mkdir(exist_ok=True)
        
        logger.info(f"DataService initialisiert: {self.data_dir}")
    
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
    
    def store_data(self, key: str, data: Any, metadata: Optional[Dict[str, Any]] = None):
        """
        Speichert Daten mit Metadaten.
        
        Args:
            key: Eindeutiger Schlüssel für die Daten
            data: Zu speichernde Daten
            metadata: Optionale Metadaten
        """
        with self._lock:
            self._data[key] = data
            self._metadata[key] = {
                "timestamp": datetime.now(),
                "data_type": type(data).__name__,
                **(metadata or {})
            }
        
        logger.info(f"Daten gespeichert: {key} ({type(data).__name__})")
        self._trigger_event("data_stored", {"key": key, "data_type": type(data).__name__})
    
    def get_data(self, key: str) -> Optional[Any]:
        """Gibt gespeicherte Daten zurück."""
        with self._lock:
            return self._data.get(key)
    
    def get_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """Gibt Metadaten für einen Schlüssel zurück."""
        with self._lock:
            return self._metadata.get(key)
    
    def remove_data(self, key: str):
        """Entfernt Daten und Metadaten."""
        with self._lock:
            if key in self._data:
                del self._data[key]
            if key in self._metadata:
                del self._metadata[key]
        
        logger.info(f"Daten entfernt: {key}")
        self._trigger_event("data_removed", {"key": key})
    
    def list_data_keys(self) -> List[str]:
        """Gibt alle verfügbaren Daten-Schlüssel zurück."""
        with self._lock:
            return list(self._data.keys())
    
    def save_dataframe(self, key: str, df: pd.DataFrame, filename: str, format: str = "csv"):
        """
        Speichert ein DataFrame als Datei.
        
        Args:
            key: Eindeutiger Schlüssel
            df: DataFrame
            filename: Dateiname
            format: Dateiformat (csv, excel, json)
        """
        try:
            file_path = self.result_dir / filename
            
            if format.lower() == "csv":
                df.to_csv(file_path, index=False)
            elif format.lower() == "excel":
                df.to_excel(file_path, index=False)
            elif format.lower() == "json":
                df.to_json(file_path, orient="records")
            else:
                raise ValueError(f"Nicht unterstütztes Format: {format}")
            
            # Metadaten speichern
            metadata = {
                "filename": filename,
                "file_path": str(file_path),
                "format": format,
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict()
            }
            
            self.store_data(key, df, metadata)
            
            logger.info(f"DataFrame gespeichert: {filename} ({df.shape})")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern des DataFrames: {e}")
            raise
    
    def load_dataframe(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Lädt ein DataFrame aus einer Datei.
        
        Args:
            file_path: Pfad zur Datei
            
        Returns:
            Geladenes DataFrame
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
        try:
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_path.suffix.lower() == '.json':
                df = pd.read_json(file_path)
            else:
                raise ValueError(f"Nicht unterstütztes Dateiformat: {file_path.suffix}")
            
            logger.info(f"DataFrame geladen: {file_path} ({df.shape})")
            return df
            
        except Exception as e:
            logger.error(f"Fehler beim Laden des DataFrames: {e}")
            raise
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Gibt eine Zusammenfassung aller gespeicherten Daten zurück."""
        with self._lock:
            summary = {
                "total_entries": len(self._data),
                "data_types": {},
                "recent_entries": [],
                "storage_size": 0
            }
            
            for key, data in self._data.items():
                data_type = type(data).__name__
                if data_type not in summary["data_types"]:
                    summary["data_types"][data_type] = 0
                summary["data_types"][data_type] += 1
                
                metadata = self._metadata.get(key, {})
                if "timestamp" in metadata:
                    summary["recent_entries"].append({
                        "key": key,
                        "type": data_type,
                        "timestamp": metadata["timestamp"]
                    })
            
            # Nach Zeitstempel sortieren
            summary["recent_entries"].sort(
                key=lambda x: x["timestamp"], 
                reverse=True
            )
            
            return summary
    
    def clear_all_data(self):
        """Löscht alle gespeicherten Daten."""
        with self._lock:
            self._data.clear()
            self._metadata.clear()
        
        logger.info("Alle Daten gelöscht")
        self._trigger_event("data_cleared")


# Globale Instanz
_data_service = None

def get_data_service() -> DataService:
    """Gibt die globale DataService-Instanz zurück."""
    global _data_service
    if _data_service is None:
        _data_service = DataService()
    return _data_service 