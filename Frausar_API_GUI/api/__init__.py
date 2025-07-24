"""
FastAPI Integration für Frausar-System
======================================

REST-API für AI-Agenten-Integration mit Endpunkten für:
- Datei-Upload
- Datenbereinigung
- Ergebnis-Abruf
- Status-Monitoring
"""

from .main import app
from .models import UploadResponse, CleanResponse, StatusResponse

__all__ = [
    'app',
    'UploadResponse',
    'CleanResponse', 
    'StatusResponse'
] 