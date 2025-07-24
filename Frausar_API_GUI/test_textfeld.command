#!/bin/zsh
# Test-Skript für Textfeld-Funktionalität

echo "🧪 Teste Textfeld-Funktionalität..."
echo ""

# Prüft ob Python verfügbar ist
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 ist nicht installiert!"
    read -p "Drücken Sie Enter zum Beenden..."
    exit 1
fi

echo "✅ Python3 verfügbar"
echo ""

# Startet den Test
echo "🚀 Starte Textfeld-Test..."
echo ""
echo "Anleitung:"
echo "1. Klicken Sie in das Textfeld"
echo "2. Tippen Sie etwas ein"
echo "3. Klicken Sie 'Test Eingabe'"
echo ""

python3 test_marker_gui.py

echo ""
echo "👋 Test beendet"
read -p "Drücken Sie Enter zum Schließen..." 