#!/usr/bin/env python3
"""
Test-Skript für OrDo Modelle und Router
"""

import requests
import json
import time
from router import Router, load_router_config

def test_ollama_connection():
    """Testet Ollama-Verbindung"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama verfügbar")
            print(f"📋 Verfügbare Modelle: {[m['name'] for m in models.get('models', [])]}")
            return True
        else:
            print(f"❌ Ollama-Fehler: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama nicht erreichbar: {e}")
        return False

def test_model_response(model_name, prompt="Hallo, wie geht es dir?"):
    """Testet Modell-Antwort"""
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 50
            }
        }
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '').strip()
        else:
            return f"Fehler: {response.status_code}"
            
    except Exception as e:
        return f"Fehler: {e}"

def test_router():
    """Testet Router-Funktionalität"""
    try:
        config = load_router_config('resonanz_trichord_router.yaml')
        router = Router(config)
        print("✅ Router erfolgreich geladen")
        
        # Test-Events
        test_events = [
            {
                'text': 'Ich fühle mich wie ein Kind und bin überrascht.',
                'metadata': {'source': 'test'}
            },
            {
                'text': 'Es gibt einen Strudel von Wut in mir.',
                'metadata': {'source': 'test'}
            },
            {
                'text': 'Ich sehe Kristalle des Vertrauens.',
                'metadata': {'source': 'test'}
            }
        ]
        
        for i, event in enumerate(test_events, 1):
            chosen_model = router.route(event)
            print(f"Event {i}: '{event['text'][:30]}...' → {chosen_model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Router-Test fehlgeschlagen: {e}")
        return False

def main():
    """Hauptfunktion"""
    print("🧠 OrDo Modelle und Router Test")
    print("=" * 50)
    
    # Test Ollama
    print("\n1. Teste Ollama-Verbindung...")
    ollama_ok = test_ollama_connection()
    
    if ollama_ok:
        # Test verfügbare Modelle
        print("\n2. Teste verfügbare Modelle...")
        models_to_test = ['qwen2.5:3b', 'phi3:mini']
        
        for model in models_to_test:
            print(f"\nTeste {model}...")
            response = test_model_response(model, "Sag 'Hallo' auf Deutsch.")
            print(f"Antwort: {response}")
    
    # Test Router
    print("\n3. Teste Router...")
    router_ok = test_router()
    
    print("\n" + "=" * 50)
    if ollama_ok and router_ok:
        print("✅ Alle Tests erfolgreich!")
        print("🚀 System bereit zum Starten")
    else:
        print("⚠️  Einige Tests fehlgeschlagen")
        print("🔧 Bitte prüfe die Konfiguration")

if __name__ == "__main__":
    main() 