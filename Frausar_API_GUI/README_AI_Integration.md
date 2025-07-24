# Frausar AI-Integration - Phase 1

## Übersicht

Die Frausar AI-Integration erweitert das bestehende Frausar-System um AI-gestützte Datenanalyse und -bereinigung. Phase 1 implementiert einen vollständigen Data Cleaning Agent mit sowohl GUI- als auch FastAPI-Schnittstelle.

## 🏗️ Architektur

```
Frausar AI-Integration
├── agents/                 # AI-Agenten
│   ├── base_agent.py      # Basis-Agenten-Klasse
│   ├── data_cleaning_agent.py  # Data Cleaning Agent
│   └── supervisor_agent.py     # Agenten-Orchestrierung (Stub)
├── api/                   # FastAPI-Integration
│   ├── main.py           # Haupt-API-Anwendung
│   └── models.py         # Pydantic-Modelle
├── services/             # Shared Services
│   ├── data_service.py   # Zentrale Datenhaltung
│   ├── agent_service.py  # Agenten-Verwaltung
│   └── config_service.py # Konfigurationsverwaltung
├── data/                 # Daten-Verzeichnisse
│   ├── uploads/          # Hochgeladene Dateien
│   ├── results/          # Verarbeitete Ergebnisse
│   └── demo_data.csv     # Beispiel-Daten
├── start_ai_integration.command  # One-Click-Start
├── start_ai_tests.command        # One-Click-Tests
└── main_ai_integration.py # Hauptskript
```

## 🚀 Installation

### Voraussetzungen

- Python ≥3.10
- pip (Python Package Manager)

### Abhängigkeiten installieren

```bash
cd Frausar_API_GUI
pip install -r requirements_ai.txt
```

### Zusätzliche Abhängigkeiten (falls nicht in requirements_ai.txt)

```bash
pip install fastapi uvicorn pandas numpy openpyxl pyyaml requests
```

## 🎯 Verwendung

### 1. One-Click-Start (Empfohlen)

#### Hauptsystem starten
```bash
# Doppelklick auf:
_STARTING_/start_ai_integration.command
```

#### Tests ausführen
```bash
# Doppelklick auf:
_STARTING_/start_ai_tests.command
```

### 2. Manueller Start

```bash
cd Frausar_API_GUI
python main_ai_integration.py
```

Das System startet:
- FastAPI-Server auf `http://localhost:8000`
- Konsolen-Interface für Phase 1
- Alle Services und Agenten

### 3. API-Zugriff

#### API-Dokumentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Verfügbare Endpunkte

##### Datei-Upload
```bash
curl -X POST "http://localhost:8000/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@demo_data.csv"
```

##### Datenbereinigung starten
```bash
curl -X POST "http://localhost:8000/clean" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{"filename": "20250101_120000_demo_data.csv"}'
```

##### Ergebnisse abrufen
```bash
curl -X GET "http://localhost:8000/result" \
     -H "accept: application/json"
```

##### System-Status
```bash
curl -X GET "http://localhost:8000/status" \
     -H "accept: application/json"
```

##### Agenten-Status
```bash
curl -X GET "http://localhost:8000/agent/data_cleaning/status" \
     -H "accept: application/json"
```

### 4. Python-Client Beispiel

```python
import requests
import pandas as pd

# API-Basis-URL
BASE_URL = "http://localhost:8000"

# 1. Datei hochladen
with open("demo_data.csv", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    upload_data = response.json()
    filename = upload_data["filename"]

# 2. Datenbereinigung starten
clean_request = {"filename": filename}
response = requests.post(f"{BASE_URL}/clean", json=clean_request)

# 3. Ergebnisse abrufen
response = requests.get(f"{BASE_URL}/result")
result_data = response.json()

# 4. Daten als DataFrame laden
df = pd.DataFrame(result_data["data_preview"])
print(f"Bereinigte Daten: {result_data['total_rows']} Zeilen, {result_data['total_columns']} Spalten")
```

## 🤖 AI-Agenten

### DataCleaningAgent

Der DataCleaningAgent führt automatische Datenbereinigung durch:

#### Funktionen
- **Fehlende Werte behandeln**: Automatische Auffüllung basierend auf Datentyp
- **Datentypen konvertieren**: Intelligente Erkennung und Konvertierung
- **Duplikate entfernen**: Automatische Duplikatserkennung
- **Ausreißer behandeln**: IQR-basierte Ausreißererkennung
- **Spalten mit zu vielen fehlenden Werten entfernen**: Konfigurierbare Schwellenwerte

#### Konfiguration

```yaml
data_cleaning:
  remove_columns_with_missing_threshold: 0.4  # 40% fehlende Werte
  fill_numeric_with: "mean"                   # mean, median, mode
  fill_categorical_with: "mode"               # mode, most_frequent
  remove_duplicates: true
  handle_outliers: true
  outlier_threshold: 3.0                      # Standardabweichungen
  convert_dtypes: true
  log_changes: true
```

### SupervisorAgent (Stub)

Der SupervisorAgent ist für Phase 2+ vorgesehen und wird die Orchestrierung mehrerer Agenten übernehmen.

## 📊 Datenformate

### Unterstützte Eingabeformate
- **CSV** (.csv)
- **Excel** (.xlsx, .xls)
- **JSON** (.json)

### Ausgabeformate
- **CSV** (Standard)
- **Excel** (.xlsx)
- **JSON** (.json)

## ⚙️ Konfiguration

### Konfigurationsdateien

Das System verwendet YAML-Konfigurationsdateien im `config/`-Verzeichnis:

- `agents.yaml` - Agenten-Konfigurationen
- `api.yaml` - API-Einstellungen
- `gui.yaml` - GUI-Einstellungen
- `data.yaml` - Datenverwaltung

### Standard-Konfigurationen

```yaml
# api.yaml
host: "0.0.0.0"
port: 8000
debug: false
cors_origins: ["*"]

# data.yaml
upload_dir: "data/uploads"
result_dir: "data/results"
temp_dir: "data/temp"
max_file_size: 104857600  # 100MB
```

## 🔧 Entwicklung

### Projektstruktur erweitern

#### Neuen Agenten hinzufügen

1. Neue Agenten-Klasse erstellen:
```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    async def process(self, data, **kwargs):
        # Implementierung
        return result
```

2. Agenten registrieren:
```python
from services import get_agent_service

agent_service = get_agent_service()
agent_service.register_agent("my_custom", MyCustomAgent())
```

#### Neue API-Endpunkte hinzufügen

1. Endpunkt in `api/main.py` hinzufügen:
```python
@app.post("/my_endpoint")
async def my_endpoint(request: MyRequest):
    # Implementierung
    return MyResponse(...)
```

2. Pydantic-Modelle in `api/models.py` definieren:
```python
class MyRequest(BaseModel):
    # Request-Felder

class MyResponse(BaseModel):
    # Response-Felder
```

### Testing

#### Automatisierte Tests

```bash
# Tests ausführen
python -m pytest Frausar_API_GUI/tests/

# Spezifische Tests
python -m pytest Frausar_API_GUI/tests/test_agents.py
```

#### Manuelle Tests

1. Demo-Daten verwenden:
```bash
# Demo-Datenbereinigung starten
python main_ai_integration.py
# Option 4 wählen
```

2. API-Tests:
```bash
# API-Status prüfen
curl http://localhost:8000/status

# Demo-Upload
curl -X POST "http://localhost:8000/upload" \
     -F "file=@data/demo_data.csv"
```

#### One-Click-Tests

```bash
# Doppelklick auf:
_STARTING_/start_ai_tests.command
```

## 📝 Logging

### Log-Dateien

- **Hauptlog**: `Frausar_API_GUI/logs/ai_integration.log`
- **API-Logs**: Uvicorn-Access-Logs (stdout)
- **Agenten-Logs**: Strukturierte Logs mit Metadaten

### Log-Level

- **INFO**: Standard-Informationen
- **DEBUG**: Detaillierte Debug-Informationen
- **WARNING**: Warnungen
- **ERROR**: Fehler

## 🚨 Fehlerbehandlung

### Häufige Fehler

1. **Port bereits belegt**
   ```
   Lösung: Port in api.yaml ändern oder anderen Prozess beenden
   ```

2. **Datei nicht gefunden**
   ```
   Lösung: Pfad prüfen, Datei existiert
   ```

3. **Import-Fehler**
   ```
   Lösung: Abhängigkeiten installieren, Python-Pfad prüfen
   ```

### Debug-Modus

```bash
# Debug-Modus aktivieren
export DEBUG=true
python main_ai_integration.py
```

## 🔮 Phase 2+ Roadmap

### Phase 2: Erweiterte Agenten
- [ ] Data Wrangling Agent
- [ ] Visualization Agent
- [ ] Multi-Agenten-Orchestrierung
- [ ] GUI-Integration (Tkinter)

### Phase 3: Produktionsreife
- [ ] Authentifizierung
- [ ] Rate Limiting
- [ ] Docker-Container
- [ ] Monitoring & Metrics

### Phase 4: Erweiterte Features
- [ ] Marker-Generierung
- [ ] Repository-Analyse
- [ ] LangChain-Integration
- [ ] Cloud-Deployment

## 📞 Support

### Dokumentation
- API-Docs: `http://localhost:8000/docs`
- Code-Dokumentation: Inline-Kommentare

### Logs analysieren
```bash
tail -f Frausar_API_GUI/logs/ai_integration.log
```

### Debug-Informationen
```bash
# System-Status
curl http://localhost:8000/status

# Agenten-Status
curl http://localhost:8000/agent/data_cleaning/status
```

## 📄 Lizenz

Teil des Frausar-Systems - Proprietär 