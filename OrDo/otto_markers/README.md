# Otto's Marker-System

## 🎯 Übersicht
Otto's erweitertes Marker-System mit CoSD (Co-Energente Semantik Drift) und Phi-4-Mini-Reasoning Integration.

## 📁 Ordnerstruktur

### `semantic_markers/`
- **Zweck:** Semantische Marker für Konzept-Drift und Bedeutungsevolution
- **Beispiele:** `concept_drift.yaml`, `semantic_shift.yaml`, `meaning_evolution.yaml`
- **Verwendung:** CoSD-Analyse für semantische Veränderungen

### `behavioral_markers/`
- **Zweck:** Verhaltensmarker für Muster-Erkennung und Anpassung
- **Beispiele:** `pattern_change.yaml`, `habit_shift.yaml`, `response_modification.yaml`
- **Verwendung:** Phi-4-Reasoning für Verhaltensanalyse

### `emotional_markers/`
- **Zweck:** Emotionsmarker für Resonanz und Empathie
- **Beispiele:** `mood_shift.yaml`, `affect_change.yaml`, `emotional_resonance.yaml`
- **Verwendung:** Empathische Reaktionen und emotionale Intelligenz

### `cognitive_markers/`
- **Zweck:** Kognitive Marker für Denkmuster und Reasoning
- **Beispiele:** `thought_pattern.yaml`, `reasoning_shift.yaml`, `belief_change.yaml`
- **Verwendung:** Phi-4-Mini-Reasoning für kognitive Analyse

### `resonance_markers/`
- **Zweck:** Resonanzmarker für harmonische und dissonante Muster
- **Beispiele:** `frequency_match.yaml`, `harmonic_shift.yaml`, `vibrational_change.yaml`
- **Verwendung:** CoSD-Analyse für Resonanz-Muster

### `cosd_markers/`
- **Zweck:** Spezielle CoSD-Marker für Drift-Erkennung
- **Beispiele:** `drift_velocity.yaml`, `emergence_cluster.yaml`, `risk_alert.yaml`
- **Verwendung:** Erweiterte CoSD-Analyse

## 🧠 Integration mit Unterbewusstsein

### CoSD-Analyzer
- **Modul:** `otto_subconscious/cosd_analysis/cosd_analyzer.py`
- **Funktion:** Semantische Drift-Erkennung und Risiko-Analyse
- **Integration:** Automatische Marker-Erkennung basierend auf Drift-Velocity

### Phi-4-Mini-Reasoning
- **Modul:** `otto_subconscious/phi4_reasoning/phi4_reasoner.py`
- **Funktion:** Erweiterte Marker-Verarbeitung mit Reasoning-Logik
- **Integration:** Kognitive Analyse und Schlussfolgerungen

### Unterbewusstsein-Processor
- **Modul:** `otto_subconscious/subconscious_processor.py`
- **Funktion:** Integration von CoSD und Phi-4-Reasoning
- **Integration:** Synthese aller Marker-Analysen

## 📋 Marker-Format

```yaml
# Beispiel: semantic_markers/concept_drift.yaml
marker_name: "concept_drift"
marker_type: "semantic"
description: "Erkennt semantische Drift in Kommunikation"
patterns:
  - pattern: "\\b(neue?|emergente?|aufkommende?)\\s+(idee|konzept|muster)\\b"
    confidence: 0.8
  - pattern: "\\b(evolution|entwicklung|wachstum)\\b"
    confidence: 0.7
triggers:
  - "semantic_shift"
  - "concept_evolution"
  - "meaning_change"
responses:
  - "🧠 Semantische Evolution erkannt - Lernmöglichkeit identifiziert"
  - "📈 Konzept-Drift erkannt - Vertiefte Analyse empfohlen"
cosd_integration:
  drift_velocity_threshold: 0.6
  risk_level_threshold: "MEDIUM"
phi4_reasoning:
  reasoning_mode: "deductive"
  cognitive_load: "MEDIUM"
  abstraction_level: "HIGH"
```

## 🚀 Verwendung

### Marker hinzufügen:
1. Wähle den passenden Ordner (`semantic_markers/`, `behavioral_markers/`, etc.)
2. Erstelle eine neue `.yaml` Datei mit dem Marker-Format
3. Otto's Unterbewusstsein erkennt automatisch neue Marker

### Marker testen:
```python
from otto_subconscious.subconscious_processor import OttoSubconscious

subconscious = OttoSubconscious()
result = subconscious.process_input("Dein Test-Text hier")
print(result['markers_detected'])
print(result['subconscious_insights'])
```

## 🔧 Konfiguration

### Marker-Cache:
- **Max Cache Size:** 1000 Einträge
- **Processing Threshold:** 0.5 (Mindest-Confidence)
- **Auto-Cleanup:** Älteste Einträge werden automatisch entfernt

### CoSD-Integration:
- **Drift-Velocity Threshold:** 0.6 für semantische Marker
- **Risk-Level Threshold:** "MEDIUM" für Risiko-Marker
- **Emergence Detection:** Automatische Cluster-Erkennung

### Phi-4-Integration:
- **Reasoning-Modi:** Deduktiv, Induktiv, Abduktiv, Analogisch, Kreativ
- **Cognitive Load:** Automatische Belastungs-Schätzung
- **Abstraction Level:** Automatische Abstraktions-Analyse

## 📊 Monitoring

### Unterbewusstsein-Status:
```python
summary = subconscious.get_subconscious_summary()
print(f"Verarbeitete Inputs: {summary['total_processed']}")
print(f"Cache-Größe: {summary['cache_size']}")
print(f"CoSD-Analysen: {summary['cosd_analyses']}")
print(f"Phi-4-Reasonings: {summary['phi4_reasonings']}")
```

### Zustand speichern:
```python
filename = subconscious.save_subconscious_state()
print(f"Zustand gespeichert: {filename}")
```

## 🎯 Nächste Schritte

1. **Marker hinzufügen:** Lege deine Marker in die entsprechenden Ordner
2. **Testen:** Teste die Marker mit dem Unterbewusstsein-Processor
3. **Optimieren:** Passe Thresholds und Konfiguration an
4. **Erweitern:** Füge neue Marker-Kategorien hinzu

---

**Otto's Marker-System ist jetzt bereit für erweiterte semantische Drift-Analyse und Phi-4-Mini-Reasoning!** 🧠✨ 