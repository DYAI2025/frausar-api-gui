#!/usr/bin/env python3
"""
Test-Script für Otto Voice System
Überprüft alle Voice-Komponenten
"""

import os
import requests
import subprocess
import yaml
from pathlib import Path

def test_config_files():
    """Testet Konfigurationsdateien"""
    print("🔧 Teste Konfigurationsdateien...")
    
    # Test otto_config.yaml
    config_path = Path("shared/configs/otto_config.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        tts_provider = config.get('tts', {}).get('provider')
        voice_id = config.get('tts', {}).get('voice_id')
        
        print(f"   TTS Provider: {tts_provider}")
        print(f"   Voice ID: {voice_id}")
        
        if tts_provider == "elevenlabs" and voice_id == "6af9AKVSpHxy6rXrzqiz":
            print("   ✅ Konfiguration korrekt")
            return True
        else:
            print("   ❌ Konfiguration fehlerhaft")
            return False
    else:
        print("   ❌ Konfigurationsdatei nicht gefunden")
        return False

def test_voice_id_consistency():
    """Testet Voice ID Konsistenz"""
    print("🎭 Teste Voice ID Konsistenz...")
    
    voice_id = "6af9AKVSpHxy6rXrzqiz"
    files_to_check = [
        "otto_voice_macos.py",
        "otto_voice_interface.py", 
        "otto_predictive_learning.py",
        "ordo_mlx_agent.py"
    ]
    
    all_consistent = True
    for file_path in files_to_check:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                content = f.read()
                if voice_id in content:
                    print(f"   ✅ {file_path}: Voice ID gefunden")
                else:
                    print(f"   ❌ {file_path}: Voice ID nicht gefunden")
                    all_consistent = False
        else:
            print(f"   ⚠️ {file_path}: Datei nicht gefunden")
    
    return all_consistent

def test_elevenlabs_connection():
    """Testet ElevenLabs Verbindung"""
    print("🔊 Teste ElevenLabs Verbindung...")
    
    api_key = os.getenv('ELEVENLABS_API_KEY')
    voice_id = "6af9AKVSpHxy6rXrzqiz"
    
    if not api_key:
        print("   ❌ ELEVENLABS_API_KEY nicht gesetzt")
        return False
    
    try:
        url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
        headers = {"xi-api-key": api_key}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ ElevenLabs Verbindung erfolgreich")
            return True
        else:
            print(f"   ❌ ElevenLabs Fehler: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ ElevenLabs Verbindungsfehler: {e}")
        return False

def test_macos_voice():
    """Testet macOS Voice System"""
    print("🗣️ Teste macOS Voice System...")
    
    try:
        # Teste verfügbare deutsche Stimmen
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
        german_voices = [line for line in result.stdout.split('\n') if 'de_DE' in line]
        
        if german_voices:
            print(f"   ✅ {len(german_voices)} deutsche Stimmen verfügbar")
            
            # Teste Anna Stimme
            test_result = subprocess.run(['say', '-v', 'Anna', 'Test'], 
                                       capture_output=True, timeout=5)
            if test_result.returncode == 0:
                print("   ✅ Anna Stimme funktioniert")
                return True
            else:
                print("   ❌ Anna Stimme funktioniert nicht")
                return False
        else:
            print("   ❌ Keine deutschen Stimmen gefunden")
            return False
            
    except Exception as e:
        print(f"   ❌ macOS Voice Fehler: {e}")
        return False

def main():
    """Haupttest-Funktion"""
    print("🧪 OTTO VOICE SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("Konfigurationsdateien", test_config_files),
        ("Voice ID Konsistenz", test_voice_id_consistency),
        ("ElevenLabs Verbindung", test_elevenlabs_connection),
        ("macOS Voice System", test_macos_voice)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Test fehlgeschlagen: {e}")
            results.append((test_name, False))
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print("📊 TEST ERGEBNISSE:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nGesamt: {passed}/{total} Tests bestanden")
    
    if passed == total:
        print("🎉 Alle Tests bestanden! Otto Voice System ist bereit.")
    else:
        print("⚠️ Einige Tests fehlgeschlagen. Überprüfe die Konfiguration.")

if __name__ == "__main__":
    main() 