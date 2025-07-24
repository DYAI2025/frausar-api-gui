"""
Data Cleaning Agent für Frausar-System
======================================

AI-gestützter Agent für automatische Datenbereinigung und -vorverarbeitung.
Verwendet Pandas für effiziente Datenverarbeitung und bietet konfigurierbare
Bereinigungsstrategien.
"""

import logging
import pandas as pd
import numpy as np
from typing import Any, Dict, Optional, List, Union
from pathlib import Path
import json

from .base_agent import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


class DataCleaningAgent(BaseAgent):
    """
    AI-gestützter Agent für automatische Datenbereinigung.
    
    Führt folgende Bereinigungsaufgaben durch:
    - Fehlende Werte behandeln
    - Datentypen konvertieren
    - Duplikate entfernen
    - Ausreißer identifizieren
    - Spalten mit zu vielen fehlenden Werten entfernen
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialisiert den Data Cleaning Agent.
        
        Args:
            config: Konfigurations-Dictionary mit Bereinigungsoptionen
        """
        default_config = {
            "remove_columns_with_missing_threshold": 0.4,  # 40% fehlende Werte
            "fill_numeric_with": "mean",  # mean, median, mode
            "fill_categorical_with": "mode",  # mode, most_frequent
            "remove_duplicates": True,
            "handle_outliers": True,
            "outlier_threshold": 3.0,  # Standardabweichungen
            "convert_dtypes": True,
            "log_changes": True
        }
        
        if config:
            default_config.update(config)
        
        super().__init__("DataCleaningAgent", default_config)
        
        # Tracking für Änderungen
        self.changes_log = []
        self.original_shape = None
        self.cleaned_shape = None
    
    async def process(self, data: Union[pd.DataFrame, str, Path], **kwargs) -> AgentResult:
        """
        Führt die Datenbereinigung durch.
        
        Args:
            data: DataFrame oder Pfad zu CSV/Excel-Datei
            **kwargs: Zusätzliche Parameter
            
        Returns:
            AgentResult mit bereinigten Daten und Metadaten
        """
        # Daten laden falls nötig
        if isinstance(data, (str, Path)):
            df = await self._load_data(data)
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise ValueError(f"Nicht unterstützter Datentyp: {type(data)}")
        
        self.original_shape = df.shape
        logger.info(f"Starte Datenbereinigung für DataFrame mit Shape: {self.original_shape}")
        
        # Bereinigungs-Pipeline
        df_cleaned = await self._clean_dataframe(df)
        
        self.cleaned_shape = df_cleaned.shape
        
        # Metadaten sammeln
        metadata = {
            "original_shape": self.original_shape,
            "cleaned_shape": self.cleaned_shape,
            "rows_removed": self.original_shape[0] - self.cleaned_shape[0],
            "columns_removed": self.original_shape[1] - self.cleaned_shape[1],
            "changes_log": self.changes_log,
            "cleaning_config": self.config
        }
        
        logger.info(f"Datenbereinigung abgeschlossen. "
                   f"Zeilen: {self.original_shape[0]} → {self.cleaned_shape[0]}, "
                   f"Spalten: {self.original_shape[1]} → {self.cleaned_shape[1]}")
        
        return AgentResult(df_cleaned, metadata)
    
    async def _load_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """Lädt Daten aus verschiedenen Dateiformaten."""
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
            
            logger.info(f"Daten erfolgreich geladen: {file_path} -> Shape: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Fehler beim Laden der Datei {file_path}: {e}")
            raise
    
    async def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Führt die eigentliche Datenbereinigung durch."""
        df_cleaned = df.copy()
        
        # 1. Spalten mit zu vielen fehlenden Werten entfernen
        if self.config["remove_columns_with_missing_threshold"] > 0:
            df_cleaned = await self._remove_high_missing_columns(df_cleaned)
        
        # 2. Datentypen konvertieren
        if self.config["convert_dtypes"]:
            df_cleaned = await self._convert_dtypes(df_cleaned)
        
        # 3. Fehlende Werte behandeln
        df_cleaned = await self._handle_missing_values(df_cleaned)
        
        # 4. Duplikate entfernen
        if self.config["remove_duplicates"]:
            df_cleaned = await self._remove_duplicates(df_cleaned)
        
        # 5. Ausreißer behandeln
        if self.config["handle_outliers"]:
            df_cleaned = await self._handle_outliers(df_cleaned)
        
        return df_cleaned
    
    async def _remove_high_missing_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Entfernt Spalten mit zu vielen fehlenden Werten."""
        threshold = self.config["remove_columns_with_missing_threshold"]
        missing_ratio = df.isnull().sum() / len(df)
        columns_to_remove = missing_ratio[missing_ratio > threshold].index.tolist()
        
        if columns_to_remove:
            df_cleaned = df.drop(columns=columns_to_remove)
            self.changes_log.append({
                "operation": "remove_high_missing_columns",
                "columns_removed": columns_to_remove,
                "missing_ratio_threshold": threshold
            })
            logger.info(f"Spalten mit >{threshold*100}% fehlenden Werten entfernt: {columns_to_remove}")
        else:
            df_cleaned = df
        
        return df_cleaned
    
    async def _convert_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Konvertiert Datentypen automatisch."""
        # Numerische Spalten
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                pass
        
        # Datum-Spalten erkennen und konvertieren
        date_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col], errors='raise')
                    date_columns.append(col)
                except:
                    pass
        
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        if date_columns:
            self.changes_log.append({
                "operation": "convert_dtypes",
                "date_columns_converted": date_columns
            })
        
        return df
    
    async def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Behandelt fehlende Werte basierend auf Datentyp."""
        df_cleaned = df.copy()
        
        for column in df_cleaned.columns:
            if df_cleaned[column].isnull().any():
                if pd.api.types.is_numeric_dtype(df_cleaned[column]):
                    # Numerische Spalten
                    fill_method = self.config["fill_numeric_with"]
                    if fill_method == "mean":
                        fill_value = df_cleaned[column].mean()
                    elif fill_method == "median":
                        fill_value = df_cleaned[column].median()
                    else:
                        fill_value = df_cleaned[column].mode().iloc[0] if not df_cleaned[column].mode().empty else 0
                    
                    df_cleaned[column].fillna(fill_value, inplace=True)
                    
                else:
                    # Kategorische Spalten
                    fill_method = self.config["fill_categorical_with"]
                    if fill_method == "mode":
                        fill_value = df_cleaned[column].mode().iloc[0] if not df_cleaned[column].mode().empty else "Unknown"
                    else:
                        fill_value = "Unknown"
                    
                    df_cleaned[column].fillna(fill_value, inplace=True)
                
                self.changes_log.append({
                    "operation": "fill_missing_values",
                    "column": column,
                    "fill_method": fill_method,
                    "missing_count": df[column].isnull().sum()
                })
        
        return df_cleaned
    
    async def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Entfernt Duplikate."""
        original_count = len(df)
        df_cleaned = df.drop_duplicates()
        removed_count = original_count - len(df_cleaned)
        
        if removed_count > 0:
            self.changes_log.append({
                "operation": "remove_duplicates",
                "duplicates_removed": removed_count
            })
            logger.info(f"{removed_count} Duplikate entfernt")
        
        return df_cleaned
    
    async def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Behandelt Ausreißer in numerischen Spalten."""
        df_cleaned = df.copy()
        threshold = self.config["outlier_threshold"]
        outlier_columns = []
        
        for column in df_cleaned.select_dtypes(include=[np.number]).columns:
            Q1 = df_cleaned[column].quantile(0.25)
            Q3 = df_cleaned[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outliers = (df_cleaned[column] < lower_bound) | (df_cleaned[column] > upper_bound)
            
            if outliers.any():
                # Ausreißer durch Median ersetzen
                median_value = df_cleaned[column].median()
                df_cleaned.loc[outliers, column] = median_value
                outlier_columns.append(column)
                
                self.changes_log.append({
                    "operation": "handle_outliers",
                    "column": column,
                    "outliers_replaced": outliers.sum(),
                    "replacement_value": median_value
                })
        
        if outlier_columns:
            logger.info(f"Ausreißer in Spalten behandelt: {outlier_columns}")
        
        return df_cleaned
    
    def get_summary(self) -> Dict[str, Any]:
        """Gibt eine Zusammenfassung der Bereinigungsaktivitäten zurück."""
        if not self.result:
            return {"error": "Keine Bereinigung durchgeführt"}
        
        return {
            "original_shape": self.original_shape,
            "cleaned_shape": self.cleaned_shape,
            "changes_made": len(self.changes_log),
            "changes_log": self.changes_log,
            "config_used": self.config
        }
    
    def save_cleaned_data(self, file_path: Union[str, Path], format: str = "csv"):
        """Speichert die bereinigten Daten."""
        if not self.result or not self.result.data:
            raise ValueError("Keine bereinigten Daten verfügbar")
        
        file_path = Path(file_path)
        
        try:
            if format.lower() == "csv":
                self.result.data.to_csv(file_path, index=False)
            elif format.lower() == "excel":
                self.result.data.to_excel(file_path, index=False)
            elif format.lower() == "json":
                self.result.data.to_json(file_path, orient="records")
            else:
                raise ValueError(f"Nicht unterstütztes Format: {format}")
            
            logger.info(f"Bereinigte Daten gespeichert: {file_path}")
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern: {e}")
            raise 