# Tax Calculator Storage

Ein einfaches, sicheres Datenverarbeitungstool für steuerrelevante Berechnungen und Dateiverwaltung.

## Übersicht

Tax Calculator Storage ist eine minimalistische Desktop-Anwendung für die sichere Handhabung verschiedener Dateiformate. Die Anwendung bietet grundlegende Dateiverarbeitungsfunktionen mit Zugangscode-Schutz und eignet sich für die Verwaltung sensibler Daten.

## Funktionen

- **Multi-Format-Unterstützung**: CSV, SIP, TXT, XML, JSON, DAT Dateien
- **Sichere Verarbeitung**: Starke Verschlüsselung mit Zugangscode-Schutz
- **Format-Erhaltung**: Ursprüngliches Dateiformat bleibt bei Extraktion erhalten
- **Lokale Verarbeitung**: Keine Netzwerkverbindungen erforderlich
- **Einfache Benutzeroberfläche**: Sauberes, professionelles Design
- **Plattformübergreifend**: Windows, macOS, Linux Unterstützung

## Installation

### Schnellstart (Empfohlen)

1. Laden Sie die entsprechende ausführbare Datei herunter:
   - Windows: `TaxCalculatorStorage.exe`
   - macOS: `TaxCalculatorStorage.app`
2. Doppelklick zum Ausführen - keine Installation erforderlich

### Aus Quellcode

```bash
# Abhängigkeiten installieren
pip install cryptography

# Anwendung starten
python3 tax_calculator.py
```

### Standalone erstellen

```bash
# Build-Skript ausführen
python3 build_tax_calculator.py
```

## Verwendung

### Dateien verarbeiten

1. Klicken Sie **"Browse Data File"** um Eingabedatei auszuwählen
2. Wählen Sie aus unterstützten Formaten (CSV, SIP, TXT, XML, JSON, DAT)
3. Klicken Sie **"Process Data"** Button
4. Geben Sie Zugangscode ein wenn aufgefordert
5. Bestätigen Sie den Zugangscode
6. Wählen Sie Speicherort für verarbeitete Datei (.dat Format)

### Dateien extrahieren

1. Klicken Sie **"Browse Processed File"** um .dat Datei auszuwählen
2. Klicken Sie **"Extract Data"** Button
3. Geben Sie den bei der Verarbeitung verwendeten Zugangscode ein
4. Wählen Sie Speicherort für extrahierte Datei
5. Ursprüngliches Format wird beibehalten

## Dateiformate

- **Eingabe**: CSV (.csv), SIP (.sip), Text (.txt), XML (.xml), JSON (.json), Data (.dat)
- **Verarbeitet**: Verschlüsselte Datendateien (.dat)
- **Ausgabe**: Ursprüngliches Format erhalten

## Sicherheitsfeatures

- **Verschlüsselung**: Fernet (AES 128 + HMAC SHA256)
- **Schlüssel-Ableitung**: PBKDF2 mit SHA256 (100.000 Iterationen)
- **Lokale Verarbeitung**: Keine Cloud-Verbindungen
- **Zugangsschutz**: Starke passwort-basierte Verschlüsselung

## Test-Dateien

Verwenden Sie den mitgelieferten Test-Datei-Generator um Beispieldaten zu erstellen:

```bash
python3 test_files_creator.py
```

Dies erstellt anonymisierte Test-Dateien in verschiedenen Formaten zu Testzwecken.

## Systemanforderungen

- **Betriebssystem**: Windows 10+, macOS 10.14+, oder Linux
- **Python**: 3.8+ (für Quellcode-Version)
- **Festplattenspeicher**: 50MB verfügbarer Speicher
- **Arbeitsspeicher**: 512MB RAM minimum

## Wichtige Hinweise

- Zugangscodes sind groß-/kleinschreibungssensitiv
- Verlorene Zugangscodes können nicht wiederhergestellt werden
- Verarbeitete Dateien benötigen den korrekten Zugangscode zur Extraktion
- Bewahren Sie Zugangscodes sicher und getrennt von verarbeiteten Dateien auf
- Alle Verarbeitung erfolgt lokal

## Technische Spezifikationen

- **Verschlüsselungsalgorithmus**: Fernet (symmetrische Verschlüsselung)
- **Schlüssel-Ableitungsfunktion**: PBKDF2 mit SHA256
- **Salt-Länge**: 16 Bytes (zufällig generiert)
- **Schlüssel-Ableitungsiterationen**: 100.000
- **Unterstützte Dateikodierungen**: UTF-8, Latin-1

## Problembehandlung

**Datei nicht erkannt:**
- Stellen Sie sicher, dass die Datei im unterstützten Format vorliegt
- Überprüfen Sie Dateiberechtigungen
- Vergewissern Sie sich, dass die Datei nicht beschädigt ist

**Verarbeitung fehlgeschlagen:**
- Überprüfen Sie verfügbaren Festplattenspeicher
- Prüfen Sie Dateizugriffsberechtigungen
- Stellen Sie sicher, dass das Dateiformat gültig ist

**Extraktion fehlgeschlagen:**
- Überprüfen Sie den korrekten Zugangscode
- Prüfen Sie Integrität der verarbeiteten Datei
- Stellen Sie sicher, dass ausreichend Festplattenspeicher vorhanden ist

## Datenschutz & Sicherheit

- Keine Telemetrie oder Datensammlung
- Alle Verarbeitung erfolgt lokal
- Keine Netzwerkverbindungen erforderlich
- Test-Daten sind vollständig anonymisiert
- Keine persönlichen Informationen gespeichert

## Lizenz

Diese Software wird wie besehen für Datenverarbeitungszwecke bereitgestellt. Verwenden Sie sie in Übereinstimmung mit geltenden Datenschutzbestimmungen.

## Mitwirken

Dieses Projekt begrüßt Beiträge. Bitte stellen Sie sicher, dass alle Beiträge die Datenschutz- und Sicherheitsstandards des Projekts einhalten.

---

*Diese Anwendung ist für legitime Datenverarbeitungszwecke konzipiert. Benutzer sind für die Einhaltung geltender Gesetze und Vorschriften verantwortlich.* 