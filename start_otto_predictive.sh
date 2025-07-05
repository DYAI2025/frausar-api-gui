#!/bin/bash

echo "🧠 Starte OTTO PREDICTIVE LEARNING..."
echo "======================================"

# Prüfe Python-Version
python3 --version

# Installiere Abhängigkeiten falls nötig
echo "📦 Prüfe Abhängigkeiten..."
pip3 install speechrecognition pyaudio pyyaml pyttsx3

# Erstelle Verzeichnisse
mkdir -p otto_jam_files
mkdir -p otto_mind_system
mkdir -p otto_crystals

echo "✅ Verzeichnisse erstellt"
echo "🚀 Starte Otto Predictive Learning..."

# Starte Otto
python3 otto_predictive_learning.py 