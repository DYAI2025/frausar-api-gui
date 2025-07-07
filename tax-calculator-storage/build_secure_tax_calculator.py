#!/usr/bin/env python3
"""
Build script für Enhanced Security Tax Calculator
Erstellt Windows .exe und Mac .app mit Doppelklick-Funktionalität
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_secure_tax_calculator():
    """Build standalone executable mit Enhanced Security"""
    
    print("🔨 Baue Enhanced Security Tax Calculator...")
    
    # Stelle sicher, dass wir im richtigen Verzeichnis sind
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if secure version exists
    if not Path("tax_calculator_secure.py").exists():
        print("❌ tax_calculator_secure.py nicht gefunden!")
        return False
    
    # PyInstaller command für maximale Kompatibilität
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",  # Wichtig für Windows Doppelklick
        "--name", "TaxCalculatorSecure",
        "--distpath", "dist_secure",
        "--workpath", "build_secure",
        "--specpath", ".",
        "--hidden-import", "cryptography",
        "--hidden-import", "cryptography.hazmat.primitives.kdf.scrypt",
        "--hidden-import", "cryptography.hazmat.primitives.kdf.pbkdf2",
        "--hidden-import", "cryptography.fernet",
        "--hidden-import", "secrets",
        "--hidden-import", "hashlib",
        "--clean",
        "tax_calculator_secure.py"
    ]
    
    try:
        # Führe PyInstaller aus
        print("🔧 Führe PyInstaller aus...")
        subprocess.run(pyinstaller_cmd, check=True)
        
        print("✅ Build erfolgreich!")
        
        # Kopiere die ausführbare Datei
        if sys.platform == "win32":
            exe_path = Path("dist_secure/TaxCalculatorSecure.exe")
            final_path = Path("TaxCalculatorSecure.exe")
            print("🪟 Windows .exe wird erstellt...")
        elif sys.platform == "darwin":
            exe_path = Path("dist_secure/TaxCalculatorSecure.app")
            final_path = Path("TaxCalculatorSecure.app")
            print("🍎 macOS .app wird erstellt...")
        else:
            exe_path = Path("dist_secure/TaxCalculatorSecure")
            final_path = Path("TaxCalculatorSecure")
            print("🐧 Linux Binary wird erstellt...")
            
        if exe_path.exists():
            # Entferne alte Version falls vorhanden
            if final_path.exists():
                if final_path.is_dir():
                    shutil.rmtree(final_path)
                else:
                    final_path.unlink()
                    
            shutil.move(str(exe_path), str(final_path))
            
            # Setze Ausführungsrechte für Unix-Systeme
            if sys.platform != "win32":
                os.chmod(final_path, 0o755)
            
            file_size = final_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📦 Standalone-Anwendung erstellt: {final_path}")
            print(f"📏 Dateigröße: {file_size:.1f} MB")
            
            # Aufräumen
            shutil.rmtree("build_secure", ignore_errors=True)
            shutil.rmtree("dist_secure", ignore_errors=True)
            if os.path.exists("TaxCalculatorSecure.spec"):
                os.remove("TaxCalculatorSecure.spec")
                
            print("🧹 Temporäre Build-Dateien entfernt")
            
            # Windows-spezifische Anweisungen
            if sys.platform == "win32":
                print("\n🪟 Windows-Hinweise:")
                print("   • Doppelklick auf TaxCalculatorSecure.exe zum Starten")
                print("   • Funktioniert ohne Python-Installation")
                print("   • Windows Defender könnte warnen (normal bei unsigned .exe)")
                
            return True
        else:
            print("❌ Ausführbare Datei nicht gefunden!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build fehlgeschlagen: {e}")
        return False
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        return False

def test_security_features():
    """Teste die Sicherheitsfeatures"""
    print("\n🔒 Teste Sicherheitsfeatures...")
    
    try:
        # Test Scrypt availability
        from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
        print("✅ Scrypt KDF verfügbar")
        
        # Test secrets module
        import secrets
        test_salt = secrets.token_bytes(32)
        print(f"✅ Kryptographisch sicherer Zufallsgenerator: {len(test_salt)} bytes")
        
        # Test enhanced algorithms
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        print("✅ PBKDF2 mit SHA256 verfügbar")
        
        print("✅ Alle Sicherheitsfeatures verfügbar!")
        return True
        
    except ImportError as e:
        print(f"❌ Sicherheitsfeature fehlt: {e}")
        return False

if __name__ == "__main__":
    print("Enhanced Security Tax Calculator Build System")
    print("=" * 50)
    
    # Check dependencies
    print("📦 Überprüfe Abhängigkeiten...")
    
    try:
        import PyInstaller
        print("✅ PyInstaller verfügbar")
    except ImportError:
        print("⏳ Installiere PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    try:
        import cryptography
        print(f"✅ Cryptography {cryptography.__version__} verfügbar")
    except ImportError:
        print("⏳ Installiere Cryptography...")
        subprocess.run([sys.executable, "-m", "pip", "install", "cryptography"], check=True)
    
    # Test security features
    if not test_security_features():
        print("❌ Sicherheitsfeatures nicht verfügbar!")
        sys.exit(1)
    
    # Build the application
    success = build_secure_tax_calculator()
    
    if success:
        print("\n🎉 Enhanced Security Tax Calculator ist bereit!")
        print("\n🔒 Sicherheitsfeatures:")
        print("   • AES-256 Verschlüsselung")
        print("   • Scrypt + PBKDF2 Key Derivation")
        print("   • 1.000.000+ Iterationen")
        print("   • 32-Byte Salt")
        print("   • Integritätsprüfung")
        print("   • Rate Limiting")
        print("   • Timing Attack Schutz")
        
        if sys.platform == "win32":
            print("\n🪟 Windows: Doppelklick auf TaxCalculatorSecure.exe")
        elif sys.platform == "darwin":
            print("\n🍎 macOS: Doppelklick auf TaxCalculatorSecure.app")
        else:
            print("\n🐧 Linux: ./TaxCalculatorSecure")
            
    else:
        print("\n❌ Build fehlgeschlagen. Bitte überprüfen Sie die Fehlermeldungen.")
        sys.exit(1) 