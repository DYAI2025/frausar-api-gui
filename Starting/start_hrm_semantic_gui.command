#!/bin/bash

# HRM Semantic Generator GUI Starter
# Startet die GUI für die semantische Beispielerzeugung

echo "🧠 HRM Semantic Generator GUI"
echo "=============================="
echo ""

# Change to HRM directory
cd "$(dirname "$0")/../_NEWZ_TOOLZ_/HRM_Super_reasoning/HRM"

# Check if we have a trained model
if [ -f "outputs/semantic-gen/checkpoints/best_model.pt" ] || [ -f "checkpoints/semantic_gen_best.pt" ]; then
    echo "✅ Trainiertes Modell gefunden - Starte vollständige GUI..."
    python3 semantic_generator_gui.py
else
    echo "⚡ Kein trainiertes Modell gefunden - Starte Demo GUI..."
    echo ""
    echo "Die Demo-GUI zeigt die Funktionalität ohne trainiertes Modell."
    echo "Für volle Funktionalität trainieren Sie zuerst ein Modell mit:"
    echo "  python train_semantic_generator.py"
    echo ""
    python3 marker_generator_studio.py
fi

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Ein Fehler ist aufgetreten."
    echo "Drücken Sie eine Taste zum Beenden..."
    read -n 1
fi