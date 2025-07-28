# Frausar API GUI

Dieses Projekt enthält eine grafische Oberfläche zur Verwaltung von "Markern" im YAML-Format.

## Smart Marker GUI starten

```bash
python smart_marker_gui.py
```

### Marker hinzufügen
1. Links kannst du über den **Template-Generator** ein Grundgerüst erzeugen.
2. Bearbeite das YAML im Textfeld oder füge eigene Marker ein.
3. Mit **Marker erstellen** wird der Inhalt geprüft und als YAML-Datei im `markers` Verzeichnis gespeichert.

### Marker-Übersicht
- Rechts befindet sich eine Übersicht aller gespeicherten Marker-Dateien.
- Angezeigt werden der **Dateiname** und die zugehörige **Kategorie**.
- Durch Auswahl eines Eintrags werden die Details im unteren Bereich geladen.

Weitere Informationen zum v3.1 Marker-Format findest du im Repository unter `marker_v3_1_manager.py`.
