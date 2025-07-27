#!/bin/zsh
# Fix Permissions für alle Start-Commands

echo "🔧 Setze Berechtigungen für alle Start-Commands..."

# Aktuelles Verzeichnis ermitteln
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

echo "Projekt-Root: $PROJECT_ROOT"
echo ""

# Alle .command Dateien im _STARTING_ Verzeichnis ausführbar machen
echo "📁 Setze Berechtigungen für _STARTING_ Commands..."
chmod +x "$SCRIPT_DIR"/*.command

# Ziel-Dateien der Symlinks ausführbar machen
echo "🔗 Setze Berechtigungen für Ziel-Dateien..."

# Kimi Commands
if [ -f "$PROJECT_ROOT/K2_cli/start_kimi_elegant.command" ]; then
    chmod +x "$PROJECT_ROOT/K2_cli/start_kimi_elegant.command"
    echo "✅ K2_cli/start_kimi_elegant.command"
fi

if [ -f "$PROJECT_ROOT/K2_cli/start_kimi.command" ]; then
    chmod +x "$PROJECT_ROOT/K2_cli/start_kimi.command"
    echo "✅ K2_cli/start_kimi.command"
fi

# Frausar Commands
if [ -f "$PROJECT_ROOT/Frausar_API_GUI/start_ai_integration.command" ]; then
    chmod +x "$PROJECT_ROOT/Frausar_API_GUI/start_ai_integration.command"
    echo "✅ Frausar_API_GUI/start_ai_integration.command"
fi

if [ -f "$PROJECT_ROOT/Frausar_API_GUI/start_ai_tests.command" ]; then
    chmod +x "$PROJECT_ROOT/Frausar_API_GUI/start_ai_tests.command"
    echo "✅ Frausar_API_GUI/start_ai_tests.command"
fi

if [ -f "$PROJECT_ROOT/Marker_assist_bot/frausar_gui.py" ]; then
    chmod +x "$PROJECT_ROOT/Marker_assist_bot/frausar_gui.py"
    echo "✅ Marker_assist_bot/frausar_gui.py"
fi

if [ -f "$PROJECT_ROOT/Frausar_API_GUI/main.py" ]; then
    chmod +x "$PROJECT_ROOT/Frausar_API_GUI/main.py"
    echo "✅ Frausar_API_GUI/main.py"
fi

echo ""
echo "🎉 Alle Berechtigungen gesetzt!"
echo ""
echo "Verfügbare Commands:"
ls -la "$SCRIPT_DIR"/*.command | awk '{print "  " $9}'
echo ""
echo "Jetzt können Sie alle Commands per Doppelklick starten!"
read -p "Drücken Sie Enter zum Schließen..." 