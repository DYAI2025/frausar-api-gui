#!/usr/bin/env python3
"""
Windows Build-Skript für Tax Calculator Storage
Erstellt beide Versionen: Standard und Enhanced Security
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def install_dependencies():
    """Installiere notwendige Abhängigkeiten"""
    print("📦 Installiere Abhängigkeiten...")
    
    dependencies = [
        "pyinstaller>=6.0.0",
        "cryptography>=45.0.0"
    ]
    
    # Scrypt optional installieren
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "scrypt>=0.8.0"], 
                     check=True, capture_output=True)
        print("✅ scrypt>=0.8.0 installiert")
    except subprocess.CalledProcessError:
        print("⚠️  scrypt nicht verfügbar - verwende nur PBKDF2")
    
    for dep in dependencies:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep} installiert")
        except subprocess.CalledProcessError as e:
            print(f"❌ Fehler bei {dep}: {e}")
            return False
    
    return True

def build_standard_version():
    """Baue die Standard-Version"""
    print("\n🔨 Baue Standard Tax Calculator Storage...")
    
    # Windows-spezifische PyInstaller-Kommandos
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "TaxCalculatorStorage",
        "--clean",
        "--distpath", "dist_windows",
        "--workpath", "build_windows",
        "--specpath", ".",
        "tax_calculator.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Standard-Version erfolgreich erstellt!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build fehlgeschlagen: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def build_secure_version():
    """Baue die Enhanced Security Version"""
    print("\n🔒 Baue Enhanced Security Tax Calculator...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "TaxCalculatorSecure",
        "--clean",
        "--distpath", "dist_windows_secure",
        "--workpath", "build_windows_secure",
        "--specpath", ".",
        "tax_calculator_secure.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Enhanced Security Version erfolgreich erstellt!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build fehlgeschlagen: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def organize_files():
    """Organisiere die erstellten Dateien"""
    print("\n📁 Organisiere Windows-Dateien...")
    
    # Erstelle Windows-Verzeichnis
    windows_dir = Path("windows_executables")
    windows_dir.mkdir(exist_ok=True)
    
    # Kopiere .exe Dateien
    files_to_copy = [
        ("dist_windows/TaxCalculatorStorage.exe", "TaxCalculatorStorage.exe"),
        ("dist_windows_secure/TaxCalculatorSecure.exe", "TaxCalculatorSecure.exe")
    ]
    
    for source, dest in files_to_copy:
        source_path = Path(source)
        dest_path = windows_dir / dest
        
        if source_path.exists():
            shutil.copy2(source_path, dest_path)
            print(f"✅ {dest} kopiert")
        else:
            print(f"❌ {source} nicht gefunden")
    
    # Erstelle README für Windows
    readme_content = """# Tax Calculator Storage - Windows Executables

## Sofort einsatzbereit - Keine Installation erforderlich!

### Dateien:
- **TaxCalculatorStorage.exe** - Standard-Version
- **TaxCalculatorSecure.exe** - Enhanced Security Version

### Verwendung:
1. Doppelklick auf die .exe Datei
2. Keine Python-Installation erforderlich
3. Keine zusätzlichen Abhängigkeiten nötig

### Sicherheit:
- Standard: PBKDF2 + Fernet (256-bit)
- Enhanced: Scrypt + PBKDF2 + AES-256 + Rate Limiting

### Unterstützte Formate:
- CSV, SIP, TXT, XML, JSON, DAT

### Hinweise:
- Die Dateien sind ca. 20-30 MB groß
- Beim ersten Start kann Windows SmartScreen warnen
- Klicken Sie "Weitere Informationen" → "Trotzdem ausführen"
"""
    
    with open(windows_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ Windows-Dateien in {windows_dir} organisiert")

def cleanup():
    """Räume temporäre Dateien auf"""
    print("\n🧹 Räume temporäre Dateien auf...")
    
    dirs_to_remove = [
        "build_windows",
        "build_windows_secure",
        "dist_windows",
        "dist_windows_secure"
    ]
    
    for dir_name in dirs_to_remove:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"✅ {dir_name} entfernt")
    
    # Entferne .spec Dateien
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"✅ {spec_file} entfernt")

def main():
    """Hauptfunktion"""
    print("🪟 Tax Calculator Storage - Windows Build")
    print("=" * 50)
    
    # Überprüfe Plattform
    if platform.system() == "Windows":
        print("✅ Windows-System erkannt")
    else:
        print("⚠️  Nicht auf Windows - .exe Dateien werden trotzdem erstellt")
    
    # Installiere Abhängigkeiten
    if not install_dependencies():
        print("❌ Abhängigkeiten konnten nicht installiert werden")
        return False
    
    # Baue beide Versionen
    success_standard = build_standard_version()
    success_secure = build_secure_version()
    
    if success_standard and success_secure:
        organize_files()
        cleanup()
        
        print("\n🎉 Windows-Build erfolgreich abgeschlossen!")
        print("📁 Dateien befinden sich in: windows_executables/")
        print("🪟 Bereit für Windows-Deployment!")
        return True
    else:
        print("\n❌ Build fehlgeschlagen")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 