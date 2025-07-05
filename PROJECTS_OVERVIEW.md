# 📁 Projekte Übersicht

Alle Projekte sind jetzt ordentlich organisiert mit eigenen Verzeichnissen und GitHub-Struktur.

## 🔒 Tax Calculator Storage

**Verzeichnis:** `tax-calculator-storage/`  
**Beschreibung:** Sicheres Tool zur Verschlüsselung verschiedener Dateiformate mit militärischer Sicherheit.

### Dateien:
- `tax_calculator.py` - Standard-Version
- `tax_calculator_secure.py` - Enhanced Security Version
- `build_tax_calculator.py` - Standard Build-Skript
- `build_secure_tax_calculator.py` - Enhanced Security Build
- `test_files_creator.py` - Anonymisierte Test-Templates
- `README.md` - Englische Dokumentation
- `README_DE.md` - Deutsche Dokumentation
- `SECURITY_TEST_REPORT.md` - Sicherheitsbericht
- `.gitignore` - Git-Konfiguration

### Features:
- ✅ Multi-Format Support (CSV, SIP, TXT, XML, JSON, DAT)
- ✅ Dual KDF (Scrypt + PBKDF2)
- ✅ 1.000.000+ Iterationen
- ✅ 32-Byte Salt
- ✅ Integritätsprüfung
- ✅ Rate Limiting
- ✅ Windows Doppelklick-Support

---

## 📊 CSV Tresor App

**Verzeichnis:** `csv-tresor-app/`  
**Beschreibung:** Einfaches Tool zur CSV-Verschlüsselung mit Passwortschutz.

### Dateien:
- `csv_tresor.py` - Hauptanwendung
- `build_csv_tresor.py` - Build-Skript
- `CSV-Tresor_README.md` - Dokumentation
- `README.md` - GitHub README
- `.gitignore` - Git-Konfiguration

### Features:
- ✅ Einfache Benutzeroberfläche
- ✅ CSV Verschlüsselung/Entschlüsselung
- ✅ PBKDF2 + Fernet Sicherheit
- ✅ Lokale Verarbeitung
- ✅ Cross-Platform

---

## 💊 InPricer

**Verzeichnis:** `inpricer/`  
**Beschreibung:** Intelligente Medikamenten-Extraktion aus CSV mit GUI, Review-Modus und Lernfunktion.

### Struktur:
```
inpricer/
├── src/
│   ├── core/          # Kern-Funktionalität
│   ├── data/          # Referenzdaten und Mappings
│   ├── gui/           # GUI-Komponenten
│   └── security/      # Verschlüsselung
├── tests/             # Unit Tests
├── inpricer_gui.py    # Haupt-GUI
├── start_gui.py       # Schnellstart
├── test_examples.py   # Test-Beispiele
└── build_standalone.py # Build-Skript
```

### Features:
- ✅ Drag & Drop GUI
- ✅ Intelligente Medikamentenerkennung (20+ Medikamente)
- ✅ Review-Modus mit 3 Tabs
- ✅ Lernfunktion für neue Mappings
- ✅ Privatsphäre-Filter (entfernt Namen, Adressen, PLZ)
- ✅ Passwortgeschützer Export
- ✅ 8 Test-Beispiele
- ✅ Bereits mit .git initialisiert

---

## 🚀 GitHub-Bereitschaft

Alle Projekte sind **GitHub-Ready** mit:
- ✅ Vollständige README-Dateien (EN/DE)
- ✅ .gitignore Konfiguration
- ✅ Anonymisierte Test-Daten
- ✅ Build-Skripte für Standalone-Versionen
- ✅ Sicherheitsdokumentation
- ✅ Keine persönlichen Daten

## 📋 Nächste Schritte

1. **InPricer:** Bereits Git-initialisiert, bereit für GitHub
2. **Tax Calculator Storage:** `git init` → GitHub Repository
3. **CSV Tresor App:** `git init` → GitHub Repository

## 🔧 Verwendung

### InPricer starten:
```bash
cd inpricer/
python3 start_gui.py
```

### Tax Calculator starten:
```bash
cd tax-calculator-storage/
python3 tax_calculator.py          # Standard
python3 tax_calculator_secure.py   # Enhanced Security
```

### CSV Tresor starten:
```bash
cd csv-tresor-app/
python3 csv_tresor.py
```

---

**Alle Projekte sind jetzt ordentlich organisiert und bereit für GitHub!** 🎉 