# Start-Commands Übersicht

Dieses Verzeichnis enthält alle One-Click-Start-Commands für das Frausar-System.

## 🚀 Verfügbare Commands

### 🎯 Marker-Erstellung (NEU - Empfohlen)
- **`start_simple_marker_gui.command`** - **EINFACHE & FUNKTIONALE Marker-Erstellung**
  - ✅ Copy-Paste-Funktionalität (Ctrl+V)
  - ✅ Automatische Fehlerbehebung
  - ✅ Sofortige Verarbeitung
  - ✅ "Alle Marker erstellen" Button
  - ✅ Keine störenden Fehlermeldungen
  - ✅ Demo-Marker zum Testen

### Enhanced Smart Marker System (Neu)
- **`start_enhanced_smart_marker_gui.command`** - Startet die Enhanced Smart Marker GUI
  - Vollständige GUI mit Import Bridge Integration
  - Live-Suche mit Fuzzy-Matching
  - Marker-Übersicht und Statistiken
  - Inline-Editor für Marker-Bearbeitung
  - Multi-Format-Support (.txt, .py, .json, .yaml, .yml)

### AI-Integration (Phase 1)
- **`start_frausar_ai.command`** - Startet die Frausar AI-Integration
  - FastAPI-Server auf http://localhost:8000
  - DataCleaningAgent mit Pandas-Integration
  - Direkte API-Start ohne interaktives Menü
  - API-Docs: http://localhost:8000/docs

- **`test_frausar_ai.command`** - Führt automatisierte Tests für die AI-Integration aus
  - Testet API-Verfügbarkeit
  - Testet Datei-Upload und -Verarbeitung
  - Testet Datenbereinigung
  - Startet API automatisch falls nötig

- **`start_ai_integration.command`** - Legacy: Interaktives Menü (Phase 1)
- **`start_ai_tests.command`** - Legacy: Tests mit interaktivem Menü

### Bestehende Systeme
- **`start_frausar_gui.command`** - Startet die ursprüngliche Frausar GUI
  - Marker_assist_bot/frausar_gui.py

- **`start_frausar_api_gui.command`** - Startet die neue Frausar API GUI
  - Frausar_API_GUI/main.py

- **`start_kimi.command`** - Startet Kimi K2
  - K2_cli/kimi_.py

- **`🌙 Kimi K2 Elegant.command`** - Elegante Kimi K2 Version

### Aliase
- **`start_cockpit.command Alias`** - Alias für ME_Test_cockpit
- **`start_frausar.command Alias`** - Alias für ursprüngliche Frausar GUI
- **`start_frausar_ai.command Alias`** - Alias für Frausar AI-Integration
- **`test_frausar_ai.command Alias`** - Alias für Frausar AI-Tests

### Wartung
- **`fix_permissions.command`** - Setzt alle Berechtigungen automatisch
  - Führt bei Berechtigungsproblemen aus
  - Macht alle Commands ausführbar

## 🎯 Verwendung

### Einfacher Start
Doppelklick auf einen der `.command`-Dateien startet das entsprechende System.

### Terminal-Start
```bash
# Enhanced Smart Marker GUI starten (EMPFOHLEN)
./start_enhanced_smart_marker_gui.command

# AI-Integration starten
./start_frausar_ai.command

# Tests ausführen
./test_frausar_ai.command

# Legacy Commands
./start_ai_integration.command
./start_ai_tests.command

# Bestehende Systeme
./start_frausar_gui.command
./start_frausar_api_gui.command
./start_kimi.command
```

## 🚨 Berechtigungsprobleme beheben

Falls Sie die Fehlermeldung "keine Zugriffsrechte" erhalten:

### Automatische Behebung
```bash
# Doppelklick auf:
fix_permissions.command
```

### Manuelle Behebung
```bash
# Alle Berechtigungen setzen
chmod +x _STARTING_/*.command
chmod +x K2_cli/*.command
chmod +x Frausar_API_GUI/*.command
chmod +x Marker_assist_bot/*.py
```

## 📋 System-Status

### Enhanced Smart Marker System
- ✅ **Vollständig implementiert**
- ✅ **Import Bridge Integration**
- ✅ **Live-Suche und Fuzzy-Matching**
- ✅ **Multi-Format-Support**
- ✅ **One-Click-Start verfügbar**
- ✅ **Tests verfügbar**
- ✅ **Berechtigungen korrekt gesetzt**

### AI-Integration (Phase 1)
- ✅ **Vollständig implementiert**
- ✅ **One-Click-Start verfügbar**
- ✅ **API-Dokumentation verfügbar**
- ✅ **Tests verfügbar**
- ✅ **Berechtigungen korrekt gesetzt**
- ✅ **GUI-Integration verfügbar**

### Bestehende Systeme
- ✅ **Alle funktionsfähig**
- ✅ **One-Click-Start verfügbar**
- ✅ **Berechtigungen korrekt gesetzt**

## 🔧 Technische Details

### AI-Integration
- **Python**: ≥3.10 erforderlich
- **Port**: 8000 (konfigurierbar)
- **Abhängigkeiten**: Automatische Installation
- **Logs**: Frausar_API_GUI/logs/ai_integration.log

### Kompatibilität
- **macOS**: Alle Commands getestet
- **Linux**: Sollte funktionieren (zsh/bash)
- **Windows**: Nicht getestet (WSL empfohlen)

## 🚨 Fehlerbehebung

### Python-Version
```bash
# Prüfen
python3 --version

# Sollte ≥3.10 sein
```

### Port-Konflikte
```bash
# Prüfen ob Port 8000 belegt ist
lsof -i :8000

# Prozess beenden falls nötig
kill -9 <PID>
```

### Berechtigungen
```bash
# Commands ausführbar machen
chmod +x *.command

# Oder automatisch:
./fix_permissions.command
```

### Import-Fehler
```bash
# Abhängigkeiten installieren
pip3 install -r Frausar_API_GUI/requirements_ai.txt

# Python-Pfad prüfen
python3 -c "import sys; print(sys.path)"
```

## 📞 Support

Bei Problemen:
1. **Berechtigungen**: `./fix_permissions.command` ausführen
2. **Logs prüfen**: `tail -f Frausar_API_GUI/logs/ai_integration.log`
3. **API-Status**: `curl http://localhost:8000/status`
4. **Python-Version**: `python3 --version`
5. **Abhängigkeiten**: `pip3 list | grep fastapi` 