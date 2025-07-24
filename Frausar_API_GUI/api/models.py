"""
Pydantic Models für FastAPI-Endpunkte
=====================================

Datenmodelle für Request/Response der AI-Agenten-API.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class UploadResponse(BaseModel):
    """Response für Datei-Upload."""
    success: bool = Field(..., description="Upload erfolgreich")
    filename: str = Field(..., description="Name der hochgeladenen Datei")
    file_size: int = Field(..., description="Dateigröße in Bytes")
    upload_time: datetime = Field(..., description="Upload-Zeitpunkt")
    message: str = Field(..., description="Status-Nachricht")


class CleanRequest(BaseModel):
    """Request für Datenbereinigung."""
    filename: str = Field(..., description="Name der zu bereinigenden Datei")
    config: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Optionale Konfiguration für DataCleaningAgent"
    )


class CleanResponse(BaseModel):
    """Response für Datenbereinigung."""
    success: bool = Field(..., description="Bereinigung erfolgreich")
    agent_name: str = Field(..., description="Name des ausführenden Agenten")
    original_shape: List[int] = Field(..., description="Originale Datenform")
    cleaned_shape: List[int] = Field(..., description="Bereinigte Datenform")
    changes_made: int = Field(..., description="Anzahl der Änderungen")
    processing_time: float = Field(..., description="Verarbeitungszeit in Sekunden")
    message: str = Field(..., description="Status-Nachricht")
    error: Optional[str] = Field(default=None, description="Fehlermeldung falls vorhanden")


class StatusResponse(BaseModel):
    """Response für System-Status."""
    system_status: str = Field(..., description="Gesamtsystem-Status")
    api_version: str = Field(..., description="API-Version")
    uptime: float = Field(..., description="Laufzeit in Sekunden")
    active_agents: List[str] = Field(..., description="Aktive Agenten")
    last_activity: Optional[datetime] = Field(default=None, description="Letzte Aktivität")


class AgentStatusResponse(BaseModel):
    """Response für Agenten-Status."""
    agent_name: str = Field(..., description="Name des Agenten")
    status: str = Field(..., description="Aktueller Status")
    start_time: Optional[datetime] = Field(default=None, description="Start-Zeitpunkt")
    end_time: Optional[datetime] = Field(default=None, description="End-Zeitpunkt")
    has_result: bool = Field(..., description="Ergebnis verfügbar")
    error: Optional[str] = Field(default=None, description="Fehlermeldung falls vorhanden")


class ResultResponse(BaseModel):
    """Response für Ergebnis-Abruf."""
    success: bool = Field(..., description="Erfolgreich")
    data_preview: List[Dict[str, Any]] = Field(..., description="Datenvorschau (erste 10 Zeilen)")
    total_rows: int = Field(..., description="Gesamtanzahl Zeilen")
    total_columns: int = Field(..., description="Gesamtanzahl Spalten")
    columns: List[str] = Field(..., description="Spaltennamen")
    metadata: Dict[str, Any] = Field(..., description="Metadaten der Verarbeitung")
    download_url: Optional[str] = Field(default=None, description="Download-URL für vollständige Daten") 