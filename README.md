# Frausar Marker Tools - Semantic Enhanced v3.1

Dieses Repository enthält ein schlankes Toolset zur Verwaltung von Markern im YAML-Format nach dem Lean‑Deep 3.1 Schema mit semantischen Erweiterungen für GPT-Agenten.

## 🧠 Neue semantische Funktionalitäten

**Optimierte Hive-Qualität und Organisation des Wissensspeichers für GPTs**
- **Semantische Suche und Klassifikation** in Wissensdomänen
- **Agent-Profile und Selbstkenntnis** für angeschlossene Agenten
- **Projekt-Kontext und Beziehungen** zwischen Markern
- **Automatische Dokumentationsgenerierung** für schnelle Orientierung
- **Erweiterbares Schema** für zukünftige Anforderungen

## 🚀 Quick Start

### Smart Marker GUI (Erweitert)

```bash
python smart_marker_gui.py
```

Mit der GUI kannst du schnell Vorlagen erzeugen, Marker bearbeiten, validieren und semantisch anreichern. Die Dateien werden im Ordner `markers` gespeichert.

### Knowledge CLI (Neu)

```bash
# Semantische Suche
python knowledge_cli.py search "emotional analysis"

# Nach Wissensdomäne filtern
python knowledge_cli.py domain emotional_analysis

# Agent-spezifische Marker
python knowledge_cli.py agent analyzer

# Dokumentation generieren
python knowledge_cli.py docs --output agent_guide.md

# Knowledge-Index neu aufbauen
python knowledge_cli.py rebuild
```

### Semantische Demo

```bash
python semantic_demo.py
```

Demonstriert alle neuen semantischen Funktionalitäten.

## 🎯 Kommandozeile

Für Skripte oder automatisierte Abläufe steht `cli_demo.py` bereit.

```bash
python cli_demo.py --create 1 --name EXAMPLE_MARKER
```

## 📚 Dokumentation

- **[LEAN_DEEP_V3_1_GUIDE.md](LEAN_DEEP_V3_1_GUIDE.md)** - Vollständige v3.1 Schema Dokumentation
- **[SEMANTIC_ENHANCEMENT_GUIDE.md](SEMANTIC_ENHANCEMENT_GUIDE.md)** - Semantische Erweiterungen für Agenten
- **[MARKER_TOOL_GUIDE.md](MARKER_TOOL_GUIDE.md)** - Detaillierte Tool-Anleitung
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Migrationshilfen

## 🤖 Für GPT-Agenten

Das System ermöglicht Agenten:

1. **Schnelle Informationssuche** durch semantische Klassifikation
2. **Selbstkenntnis** über eigene Fähigkeiten und Marker
3. **Projekt-Bewusstsein** für kontextuelle Arbeit
4. **Beziehungserkennung** zwischen Wissensbereichen
5. **Automatische Dokumentation** für neue Agenten

### Beispiel Agent-Integration

```python
from marker_tool import MarkerTool
from knowledge_registry import KnowledgeRegistry

# Agent-spezifische Marker finden
tool = MarkerTool()
results = tool.search_markers_semantically(
    "time pressure", 
    knowledge_domain="time_management",
    agent_type="analyzer"
)

# Selbstdokumentation generieren
docs = tool.generate_knowledge_documentation("emotional_analyzer")
```

## 🔧 System-Architektur

- **marker_v3_1_manager.py** - Kern v3.1 Schema mit semantischen Erweiterungen
- **knowledge_registry.py** - Zentrales semantisches Registry-System
- **marker_tool.py** - Erweiterte Marker-Verwaltung mit Suchfunktionen
- **knowledge_cli.py** - Command-Line Interface für Agenten
- **smart_marker_gui.py** - Grafische Benutzeroberfläche

## ✅ Weitere Informationen

Das v3.1 Schema sowie Hilfestellungen findest du in `marker_v3_1_manager.py` und der Datei `LEAN_DEEP_V3_1_GUIDE.md`.

Die semantischen Erweiterungen sind vollständig rückwärtskompatibel - alle bestehenden Marker funktionieren weiterhin ohne Änderungen.
