#!/usr/bin/env python3
"""
Build-Skript für CSV-Tresor Standalone-Anwendung
Erstellt ausführbare Dateien für Windows und Mac
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_standalone():
    """Erstelle eine standalone ausführbare Datei"""
    
    print("🔨 Baue CSV-Tresor Standalone-Anwendung...")
    
    # Stelle sicher, dass wir im richtigen Verzeichnis sind
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # PyInstaller-Kommando
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "CSV-Tresor",
        "--hidden-import", "cryptography",
        "--hidden-import", "tkinter",
        "--clean",
        "--distpath", "dist",
        "csv_tresor.py"
    ]
    
    # Windows-spezifische Optionen
    if sys.platform == "win32":
        pyinstaller_cmd.extend([
            "--icon", "NONE",  # Kein Icon für jetzt
            "--version-file", "NONE"
        ])
    
    try:
        # Führe PyInstaller aus
        print("⏳ Führe PyInstaller aus...")
        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ PyInstaller Fehler: {result.stderr}")
            return False
        
        print("✅ Build erfolgreich!")
        
        # Finde die ausführbare Datei
        if sys.platform == "win32":
            exe_name = "CSV-Tresor.exe"
        elif sys.platform == "darwin":
            exe_name = "CSV-Tresor"
        else:
            exe_name = "CSV-Tresor"
            
        exe_path = Path("dist") / exe_name
        
        if exe_path.exists():
            # Kopiere in Hauptverzeichnis
            final_path = Path(exe_name)
            if final_path.exists():
                final_path.unlink()
            shutil.copy2(str(exe_path), str(final_path))
            
            print(f"📦 Standalone-Anwendung erstellt: {final_path}")
            
            # Zeige Dateigröße
            size_mb = final_path.stat().st_size / (1024 * 1024)
            print(f"📏 Dateigröße: {size_mb:.1f} MB")
            
            # Aufräumen
            cleanup_build_files()
            
            return True
        else:
            print("❌ Ausführbare Datei nicht gefunden!")
            return False
            
    except Exception as e:
        print(f"❌ Build fehlgeschlagen: {e}")
        return False

def cleanup_build_files():
    """Räume temporäre Build-Dateien auf"""
    try:
        if Path("build").exists():
            shutil.rmtree("build")
        if Path("dist").exists():
            shutil.rmtree("dist")
        if Path("CSV-Tresor.spec").exists():
            Path("CSV-Tresor.spec").unlink()
        print("🧹 Temporäre Build-Dateien entfernt")
    except Exception as e:
        print(f"⚠️ Warnung beim Aufräumen: {e}")

def install_dependencies():
    """Installiere benötigte Abhängigkeiten"""
    print("📦 Überprüfe Abhängigkeiten...")
    
    required_packages = ["cryptography", "pyinstaller"]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} bereits installiert")
        except ImportError:
            print(f"⏳ Installiere {package}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
                print(f"✅ {package} erfolgreich installiert")
            except subprocess.CalledProcessError as e:
                print(f"❌ Fehler beim Installieren von {package}: {e}")
                return False
    
    return True

def main():
    """Hauptfunktion"""
    print("🔒 CSV-Tresor Build-System")
    print("=" * 40)
    
    # Prüfe ob csv_tresor.py existiert
    if not Path("csv_tresor.py").exists():
        print("❌ csv_tresor.py nicht gefunden!")
        print("Stelle sicher, dass du dich im richtigen Verzeichnis befindest.")
        return 1
    
    # Installiere Abhängigkeiten
    if not install_dependencies():
        print("❌ Abhängigkeiten konnten nicht installiert werden")
        return 1
    
    # Baue die Anwendung
    success = build_standalone()
    
    if success:
        print("\n🎉 CSV-Tresor ist bereit!")
        print("Starte die Anwendung mit einem Doppelklick auf die erstellte Datei.")
        
        # Plattform-spezifische Hinweise
        if sys.platform == "win32":
            print("\n💡 Windows-Hinweis:")
            print("Die .exe Datei kann direkt ausgeführt werden.")
            print("Windows Defender könnte eine Warnung zeigen - das ist normal für neue .exe Dateien.")
        elif sys.platform == "darwin":
            print("\n💡 Mac-Hinweis:")
            print("Beim ersten Start: Rechtsklick → 'Öffnen' (wegen Gatekeeper)")
        
        return 0
    else:
        print("\n❌ Build fehlgeschlagen.")
        print("Überprüfe die Fehlermeldungen oben.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 