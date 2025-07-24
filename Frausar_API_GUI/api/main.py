"""
FastAPI Hauptanwendung für AI-Agenten-Integration
=================================================

REST-API mit Endpunkten für:
- POST /upload - Datei-Upload
- POST /clean - Datenbereinigung starten
- GET /result - Bereinigte Daten abrufen
- GET /status - System-Status
- GET /agent/{agent_name}/status - Agenten-Status
"""

import os
import time
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd

# Relative Imports für das Frausar-System
import sys
sys.path.append(str(Path(__file__).parent.parent))

from agents import DataCleaningAgent, SupervisorAgent
from .models import (
    UploadResponse, CleanRequest, CleanResponse, 
    StatusResponse, AgentStatusResponse, ResultResponse
)

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI App
app = FastAPI(
    title="Frausar AI-Agenten API",
    description="REST-API für AI-gestützte Datenanalyse und -bereinigung",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globale Variablen
UPLOAD_DIR = Path("Frausar_API_GUI/data/uploads")
RESULT_DIR = Path("Frausar_API_GUI/data/results")
START_TIME = time.time()

# Verzeichnisse erstellen
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# Agenten-Instanzen
data_cleaning_agent = DataCleaningAgent()
supervisor_agent = SupervisorAgent()
supervisor_agent.register_agent(data_cleaning_agent)

# Aktuelle Verarbeitung
current_processing = {
    "filename": None,
    "status": "idle",
    "result": None,
    "error": None
}


@app.on_event("startup")
async def startup_event():
    """Startup-Event für die FastAPI-Anwendung."""
    logger.info("Frausar AI-Agenten API gestartet")
    logger.info(f"Upload-Verzeichnis: {UPLOAD_DIR}")
    logger.info(f"Ergebnis-Verzeichnis: {RESULT_DIR}")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root-Endpunkt mit API-Informationen."""
    return {
        "message": "Frausar AI-Agenten API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "/status"
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Lädt eine Datei hoch für die Verarbeitung.
    
    Unterstützte Formate: CSV, Excel (xlsx, xls), JSON
    """
    try:
        # Datei-Validierung
        if not file.filename:
            raise HTTPException(status_code=400, detail="Kein Dateiname angegeben")
        
        # Dateiendung prüfen
        allowed_extensions = {'.csv', '.xlsx', '.xls', '.json'}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Nicht unterstütztes Dateiformat. Erlaubt: {allowed_extensions}"
            )
        
        # Datei speichern
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = UPLOAD_DIR / safe_filename
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        file_size = len(content)
        
        logger.info(f"Datei erfolgreich hochgeladen: {safe_filename} ({file_size} Bytes)")
        
        return UploadResponse(
            success=True,
            filename=safe_filename,
            file_size=file_size,
            upload_time=datetime.now(),
            message=f"Datei {file.filename} erfolgreich hochgeladen"
        )
        
    except Exception as e:
        logger.error(f"Fehler beim Upload: {e}")
        raise HTTPException(status_code=500, detail=f"Upload-Fehler: {str(e)}")


@app.post("/clean", response_model=CleanResponse)
async def clean_data(request: CleanRequest, background_tasks: BackgroundTasks):
    """
    Startet die Datenbereinigung mit dem DataCleaningAgent.
    
    Läuft asynchron im Hintergrund.
    """
    try:
        # Datei-Prüfung
        file_path = UPLOAD_DIR / request.filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"Datei nicht gefunden: {request.filename}")
        
        # Status aktualisieren
        current_processing["filename"] = request.filename
        current_processing["status"] = "running"
        current_processing["result"] = None
        current_processing["error"] = None
        
        # Agenten-Konfiguration aktualisieren falls angegeben
        if request.config:
            data_cleaning_agent.config.update(request.config)
        
        # Asynchrone Verarbeitung starten
        background_tasks.add_task(process_data_cleaning, request.filename, request.config)
        
        return CleanResponse(
            success=True,
            agent_name=data_cleaning_agent.name,
            original_shape=[0, 0],  # Wird während der Verarbeitung aktualisiert
            cleaned_shape=[0, 0],
            changes_made=0,
            processing_time=0.0,
            message="Datenbereinigung gestartet - Status über /status abfragen"
        )
        
    except Exception as e:
        logger.error(f"Fehler beim Starten der Datenbereinigung: {e}")
        current_processing["status"] = "error"
        current_processing["error"] = str(e)
        
        raise HTTPException(status_code=500, detail=f"Fehler: {str(e)}")


async def process_data_cleaning(filename: str, config: Optional[Dict[str, Any]] = None):
    """Hintergrund-Task für die Datenbereinigung."""
    try:
        start_time = time.time()
        file_path = UPLOAD_DIR / filename
        
        logger.info(f"Starte Datenbereinigung für: {filename}")
        
        # Agenten ausführen
        result = await data_cleaning_agent.run(file_path, **(config or {}))
        
        processing_time = time.time() - start_time
        
        if result["status"] == "success":
            # Ergebnis speichern
            result_filename = f"cleaned_{filename}"
            result_path = RESULT_DIR / result_filename
            
            # Daten speichern
            cleaned_df = result["result"].data
            cleaned_df.to_csv(result_path, index=False)
            
            # Status aktualisieren
            current_processing["status"] = "completed"
            current_processing["result"] = {
                "filename": result_filename,
                "original_shape": result["result"].metadata["original_shape"],
                "cleaned_shape": result["result"].metadata["cleaned_shape"],
                "changes_made": len(result["result"].metadata["changes_log"]),
                "processing_time": processing_time,
                "file_path": str(result_path)
            }
            
            logger.info(f"Datenbereinigung abgeschlossen: {result_filename}")
            
        else:
            current_processing["status"] = "error"
            current_processing["error"] = result["error"]
            logger.error(f"Datenbereinigung fehlgeschlagen: {result['error']}")
            
    except Exception as e:
        current_processing["status"] = "error"
        current_processing["error"] = str(e)
        logger.error(f"Fehler in Datenbereinigung: {e}")


@app.get("/result", response_model=ResultResponse)
async def get_result():
    """Gibt die bereinigten Daten zurück."""
    try:
        if current_processing["status"] != "completed":
            raise HTTPException(
                status_code=400, 
                detail=f"Keine bereinigten Daten verfügbar. Status: {current_processing['status']}"
            )
        
        result_info = current_processing["result"]
        file_path = Path(result_info["file_path"])
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Ergebnisdatei nicht gefunden")
        
        # Daten laden und Vorschau erstellen
        df = pd.read_csv(file_path)
        preview_data = df.head(10).to_dict("records")
        
        return ResultResponse(
            success=True,
            data_preview=preview_data,
            total_rows=len(df),
            total_columns=len(df.columns),
            columns=df.columns.tolist(),
            metadata=result_info,
            download_url=f"/download/{result_info['filename']}"
        )
        
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Ergebnisse: {e}")
        raise HTTPException(status_code=500, detail=f"Fehler: {str(e)}")


@app.get("/download/{filename}")
async def download_result(filename: str):
    """Download-Endpunkt für bereinigte Daten."""
    try:
        file_path = RESULT_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Datei nicht gefunden")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="text/csv"
        )
        
    except Exception as e:
        logger.error(f"Fehler beim Download: {e}")
        raise HTTPException(status_code=500, detail=f"Download-Fehler: {str(e)}")


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Gibt den System-Status zurück."""
    uptime = time.time() - START_TIME
    
    active_agents = []
    for agent in supervisor_agent.get_managed_agents():
        if agent.status in ["running", "completed"]:
            active_agents.append(agent.name)
    
    return StatusResponse(
        system_status="running",
        api_version="1.0.0",
        uptime=uptime,
        active_agents=active_agents,
        last_activity=datetime.now() if active_agents else None
    )


@app.get("/agent/{agent_name}/status", response_model=AgentStatusResponse)
async def get_agent_status(agent_name: str):
    """Gibt den Status eines spezifischen Agenten zurück."""
    agent_status = supervisor_agent.get_agent_status(agent_name)
    
    if not agent_status:
        raise HTTPException(status_code=404, detail=f"Agent nicht gefunden: {agent_name}")
    
    return AgentStatusResponse(**agent_status)


@app.get("/health")
async def health_check():
    """Health-Check-Endpunkt."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time() - START_TIME
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 