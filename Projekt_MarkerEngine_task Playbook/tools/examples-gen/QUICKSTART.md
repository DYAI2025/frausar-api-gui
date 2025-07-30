# 🚀 Quickstart: Semantischer Wächter & Beispiel-Generator

> Sofortiger Einstieg in 3 Minuten

## ⚡ Sofort starten

### 1. Demo ausführen
```bash
cd "claude_curser/Projekt_MarkerEngine_task Playbook/tools/examples-gen"
python3 demo_semantic_guardian.py
```

### 2. Tests ausführen
```bash
python3 test_semantic_guardian.py
```

### 3. Eigenen Marker verarbeiten
```bash
python3 semantic_guardian.py deine_marker_datei.yaml --examples 5
```

## 🎯 Typische Anwendungsfälle

### Fall 1: Einzelne Marker-Datei erweitern
```bash
# Fügt 3 neue Beispiele hinzu
python3 semantic_guardian.py marker.yaml --examples 3

# Mit Statistiken
python3 semantic_guardian.py marker.yaml --examples 3 --stats
```

### Fall 2: Batch-Verarbeitung (Python)
```python
from semantic_guardian import MarkerExampleProcessor
from pathlib import Path

processor = MarkerExampleProcessor()

# Alle YAML-Dateien in einem Ordner
for yaml_file in Path("marker_ordner").glob("*.yaml"):
    result = processor.process_marker_file(yaml_file, num_examples=3)
    print(f"{yaml_file.name}: {'✅' if result['success'] else '❌'}")
```

### Fall 3: Validierung ohne Generierung
```python
from semantic_guardian import SemanticGuardian
import yaml

guardian = SemanticGuardian()

with open("marker.yaml") as f:
    marker = yaml.safe_load(f)

report = guardian.validate_marker(marker)
print(f"Status: {report.result.value}")
print(f"Geeignet: {report.is_suitable_for_examples}")
```

## ✅ Erwartete Ergebnisse

### Erfolgreiche Verarbeitung
```
✅ GENERIERUNG ERFOLGREICH!
📊 3 neue Beispiele hinzugefügt
🎯 SEMANTISCHE QUALITÄT: HOCH
```

### Ablehnung ungültiger Marker
```
❌ GENERIERUNG ABGELEHNT: Marker-Frame ist semantisch nicht eindeutig.
❌ Schema-Fehler: Verbotene Legacy-Felder gefunden
```

## 🔧 Häufige Probleme

### Problem: "Keine gültigen Beispiele generiert"
**Lösung:** Frame prüfen und Signale spezifischer gestalten

### Problem: "Schema-Verletzung"
**Lösung:** Legacy-Felder entfernen (`level`, `marker_name`, etc.)

### Problem: "Zu wenige Beispiele"
**Lösung:** Niedrigere Anzahl anfordern oder Frame verbessern

## 📋 Checkliste für perfekte Marker

- ✅ ID hat korrektes Präfix (A_, S_, C_, MM_)
- ✅ Frame vollständig (signal, concept, pragmatics, narrative)
- ✅ Genau ein Struktur-Block (pattern/composed_of/detect_class)
- ✅ Keine Legacy-Felder
- ✅ Spezifische, klare Signale
- ✅ Kohärente Frame-Dimensionen

## 🎉 Fertig!

Ihr **Semantischer Wächter** ist einsatzbereit und schützt die Integrität Ihrer MarkerEngine Knowledge-Base!