# 🧠 Otto Auto Learning System

## Übersicht

Das **Otto Auto Learning System** ist ein automatisches Lern- und Verdichtungssystem, das Ottos Jammeldateien analysiert, Muster erkennt und Kristalle erstellt.

## 🎯 Funktionalitäten

### Automatisches Lernen
- **Jammeldateien-Analyse**: Analysiert alle Jammeldateien in `otto_jam_files/`
- **Mustererkennung**: Erkennt Keywords, Emotionen und Themencluster
- **Kristall-Erstellung**: Erstellt verdichtete Erkenntnisse als Kristalle
- **Cluster-Identifikation**: Gruppiert ähnliche Inhalte in Cluster

### Zeitplan
- **Alle 2 Stunden**: Standard-Lernzyklus
- **Täglich 03:00**: Tägliche Analyse
- **Sonntags 12:00**: Tiefenanalyse mit wöchentlichem Bericht

## 📁 Dateistruktur

```
OrDo/
├── otto_auto_learning_system.py      # Hauptsystem
├── otto_learning_scheduler.py         # Automatischer Scheduler
├── otto_integrated_learning.py       # Integration mit Otto
├── otto_jam_files/                   # Jammeldateien
├── otto_crystals/                    # Erstellte Kristalle
├── otto_clusters/                    # Identifizierte Cluster
├── otto_compression_logs/            # Lern-Logs und Statistiken
└── otto_markers/                     # Marker-Definitionen
```

## 🚀 Verwendung

### 1. Einmaliger Lernzyklus
```bash
cd OrDo
python3 otto_auto_learning_system.py
```

### 2. Kontinuierlicher Scheduler
```bash
cd OrDo
python3 otto_learning_scheduler.py
```

### 3. Integriertes System
```bash
cd OrDo
python3 otto_integrated_learning.py
```

## 📊 Ausgabe

Das System erstellt:

### Kristalle (`otto_crystals/`)
```json
{
  "id": "crystal_20250707_045856",
  "created_at": "2025-07-07T04:58:56",
  "insights": {
    "keywords": [["wichtig", 5], ["system", 3]],
    "emotion_markers": {"freude": 2, "ärger": 1},
    "topic_clusters": ["technologie", "arbeit"]
  },
  "confidence": 0.8
}
```

### Cluster (`otto_clusters/`)
```json
{
  "id": "cluster_topic_technologie_20250707_045856",
  "type": "topic",
  "name": "technologie",
  "entries": 5,
  "confidence": 0.6
}
```

### Lernstatistiken (`otto_compression_logs/`)
- `learning_stats_YYYYMMDD_HHMMSS.json`
- `otto_learning.log`
- `scheduler.log`

## ⚙️ Konfiguration

### Marker hinzufügen
1. Erstelle YAML-Dateien in `otto_markers/`
2. Das System lädt sie automatisch

### Jammeldateien hinzufügen
1. Lege JSON/YAML/TXT-Dateien in `otto_jam_files/`
2. Das System analysiert sie automatisch

## 🔧 Erweiterte Funktionen

### Eigene Marker erstellen
```python
from otto_integrated_learning import OttoIntegratedLearning

learning = OttoIntegratedLearning()
marker_id = learning.create_marker_from_insight({
    'pattern': 'dein_muster',
    'confidence': 0.8
})
```

### Manueller Lernzyklus
```python
learning = OttoIntegratedLearning()
learning.run_manual_learning_cycle()
```

## 📈 Monitoring

### Lernstatistiken abrufen
```python
insights = learning.get_learning_insights()
print(f"Kristalle: {insights['crystals_count']}")
print(f"Cluster: {insights['clusters_count']}")
```

## 🛠️ Troubleshooting

### Häufige Probleme

1. **YAML-Fehler**: Einige Marker-Dateien haben YAML-Syntax-Fehler
   - Lösung: Überprüfe die YAML-Syntax in den Marker-Dateien

2. **Fehlende Ordner**: Das System erstellt Ordner automatisch
   - Lösung: Keine Aktion erforderlich

3. **Keine Jammeldateien**: System funktioniert auch ohne Jammeldateien
   - Lösung: Erstelle Jammeldateien in `otto_jam_files/`

### Logs überprüfen
```bash
tail -f otto_compression_logs/otto_learning.log
tail -f otto_compression_logs/scheduler.log
```

## 🔮 Zukunftsvisionen

- **Web-Interface**: Dashboard für Lernstatistiken
- **Erweiterte ML**: Deep Learning für bessere Mustererkennung
- **API-Integration**: REST-API für externe Systeme
- **Visualisierung**: Grafische Darstellung von Clustern und Trends

## 📝 Changelog

### Version 1.0.0 (2025-07-07)
- ✅ Automatisches Lernsystem
- ✅ Scheduler für regelmäßige Ausführung
- ✅ Integration mit Ottos Hauptsystem
- ✅ Kristall- und Cluster-Erstellung
- ✅ Logging und Statistiken

---

**Entwickelt für Otto - Der lernende KI-Agent** 🤖 