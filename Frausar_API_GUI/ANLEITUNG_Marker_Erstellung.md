# 🎯 Einfache Marker-Erstellung - Anleitung

## 🚀 Schnellstart

1. **Doppelklick auf**: `start_simple_marker_gui.command`
2. **Verzeichnis wählen**: Wählen Sie Ihr Marker-Verzeichnis
3. **Text einfügen**: Kopieren Sie Marker-Text und fügen Sie ihn ein (Ctrl+V)
4. **Marker erstellen**: Klicken Sie auf "🚀 Alle Marker erstellen"

## ✨ Features

### ✅ Copy-Paste-Funktionalität
- **Ctrl+V**: Text einfügen
- **Ctrl+A**: Alles auswählen
- Unterstützt mehrere Marker (getrennt durch `---`)

### ✅ Automatische Fehlerbehebung
- Korrigiert häufige Tippfehler (`beschreibg` → `description`)
- Fügt fehlende Standardwerte hinzu
- Generiert automatische IDs falls fehlend

### ✅ Benutzerfreundlich
- Keine störenden Fehlermeldungen
- Fehler werden in separatem Bereich angezeigt
- Status-Anzeige für Feedback
- Textfeld wird nach erfolgreicher Erstellung geleert

## 📝 Marker-Format

```yaml
id: A_mein_marker
level: 1
description: Beschreibung meines Markers
version: 1.0.0
status: draft
author: mein_name
---
id: S_weiterer_marker
level: 2
description: Ein weiterer Marker
version: 1.0.0
status: draft
author: mein_name
```

## 🎯 Workflow

1. **Text kopieren** (aus Dokument, Chat, etc.)
2. **In GUI einfügen** (Ctrl+V)
3. **"Alle Marker erstellen" klicken**
4. **Fertig!** Marker werden als YAML-Dateien gespeichert

## 🔧 Fehlerbehandlung

- **Syntax-Fehler**: Werden automatisch behoben
- **Fehlende Felder**: Standardwerte werden hinzugefügt
- **Tippfehler**: Häufige Fehler werden korrigiert
- **Fehler-Anzeige**: Nur bei echten Problemen sichtbar

## 🎉 Ergebnis

- Marker werden als `{id}.yaml` Dateien gespeichert
- Jeder Marker in separater Datei
- UTF-8 Encoding für Umlaute
- Sofort einsatzbereit

---

**Das ist es! Einfach, funktional und sofort einsatzbereit.** 🚀 