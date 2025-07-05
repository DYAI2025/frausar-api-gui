# 🤖 FRAUSAR Marker Assistant - Kurzanleitung

## 🚀 Schnellstart

```bash
# GUI starten
python3 start_frausar.py

# oder direkt
python3 frausar_gui.py
```

## 📋 Was ist das?

Ein **genehmigungsbasierter Assistent** für deine Love Scammer Erkennungsmarker. **Alle Änderungen müssen von dir genehmigt werden** - keine automatischen Änderungen!

## 💻 GUI-Bereiche

### 📋 **Linke Spalte - Marker-Liste**
- Zeigt alle deine `*_MARKER.txt` Dateien
- Klicke auf einen Marker um ihn auszuwählen
- Button "🔄 Aktualisieren" - Liste neu laden
- Button "➕ Neu" - Neuen Marker erstellen

### 💬 **Mittlere Spalte - Chat**
- Direkte Kommunikation mit dem Assistant
- Zeigt alle Aktionen und Feedback
- Eingabefeld unten für deine Nachrichten
- **Ctrl+Enter** zum Senden

### 💡 **Rechte Spalte - Vorschläge & Status**
- Zeigt alle vorgeschlagenen Änderungen
- **✅ Genehmigen** - Änderungen anwenden
- **❌ Ablehnen** - Änderungen verwerfen
- **📝 Beispiele hinzufügen** - Dialog öffnen

## 🎯 Typische Arbeitsabläufe

### **1. Beispiele zu bestehenden Marker hinzufügen**
```
1. Marker aus Liste auswählen
2. Button "Beispiele hinzufügen" klicken
3. Beispiele eingeben (ein pro Zeile)
4. "Hinzufügen" klicken
5. In rechter Spalte "Genehmigen" klicken
```

### **2. Neuen Marker erstellen**
```
1. Button "➕ Neu" klicken
2. Name eingeben (z.B. "FAKE_URGENCY")
3. Beschreibung eingeben
4. Beispiele hinzufügen
5. "Erstellen" klicken
6. In rechter Spalte "Genehmigen" klicken
```

### **3. Per Chat arbeiten**
```
Chat-Eingabe:
"Beispiele hinzufügen"
oder
"Neuer Marker für Zeitdruck-Taktiken"
oder direkt Beispiele eingeben:
"Du musst sofort handeln!"
"Nur heute verfügbar!"
"Angebot läuft in 1 Stunde ab!"
```

## 💬 Chat-Befehle

| Eingabe | Funktion |
|---------|----------|
| `"Beispiele hinzufügen"` | Öffnet Dialog für Beispiele |
| `"Neuer Marker"` | Anleitung für neuen Marker |
| Beispiele (mehrzeilig) | Erkennt automatisch Beispiele |
| `"Hilfe"` | Zeigt verfügbare Befehle |

## 🔒 Sicherheit

- **✅ Alle Änderungen genehmigungspflichtig**
- **✅ Automatische Backups** (mit Zeitstempel)
- **✅ Keine Datenverluste** möglich
- **✅ Rollback-Funktion** über Backups

## 📁 Dateien

```
/Users/benjaminpoersch/claude/
├── frausar_gui.py          # Haupt-GUI
├── start_frausar.py        # Starter mit Systemcheck
├── marker_assistant_bot.py # Automatischer Bot
├── frausar_setup.py        # Einrichtung
└── Assist_TXT_marker_py:/ALL_NEWMARKER01/
    ├── LOVE_BOMBING_MARKER.txt
    ├── GASLIGHTING_MARKER.txt
    └── ... (deine Marker)
```

## 🤝 Meine Rolle als Assistant

### **Sofort verfügbar:**
- ✅ GUI-Support und Hilfe
- ✅ Neue Marker-Strukturen vorschlagen
- ✅ Beispiele analysieren und kategorisieren
- ✅ Verbesserungsvorschläge machen

### **Kontinuierliche Unterstützung:**
- 📊 Trend-Analyse neuer Scammer-Muster
- 🔄 System-Updates und Verbesserungen
- 📝 Dokumentation aktuell halten
- 💡 Neue Features entwickeln

## 🚨 Bei Problemen

1. **GUI startet nicht?**
   ```bash
   python3 start_frausar.py  # Zeigt detaillierte Fehler
   ```

2. **Marker werden nicht gefunden?**
   - Überprüfe Pfad: `Assist_TXT_marker_py:/ALL_NEWMARKER01`
   - Dateien müssen `*_MARKER.txt` heißen

3. **Änderungen werden nicht gespeichert?**
   - Überprüfe Schreibrechte im Verzeichnis
   - Schaue in die Backup-Ordner

## 🎉 Fertig!

**Dein FRAUSAR System ist einsatzbereit!**

Starte einfach: `python3 start_frausar.py` und arbeite mit der benutzerfreundlichen GUI. Alle deine Marker-Änderungen sind sicher und genehmigungspflichtig!

---

**💡 Tipp:** Lasse die GUI einfach offen - sie ist dein ständiger Begleiter für die Marker-Verwaltung! 