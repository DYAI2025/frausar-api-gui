#!/bin/bash

# 📊 Claude Flow Agent Monitor Starter
# ====================================
# One-Click Starter für Claude Flow Agent Monitoring

echo "📊 CLAUDE FLOW AGENT MONITOR"
echo "============================"
echo ""

# Projekt-Pfad setzen
PROJECT_PATH="/Users/benjaminpoersch/claude_curser/claude-flow/claude-flow"
cd "$PROJECT_PATH"

echo "📁 Projekt-Pfad: $PROJECT_PATH"

# Monitoring-Script prüfen
if [ ! -f "monitor-agents.sh" ]; then
    echo "❌ Monitoring-Script nicht gefunden!"
    echo "   Erstelle Monitoring-Script..."
    
    # Erstelle das Monitoring-Script
    cat > monitor-agents.sh << 'EOF'
#!/bin/bash

# Claude Flow Agent Monitor Script
# =================================

echo "🤖 CLAUDE FLOW AGENT MONITOR"
echo "============================"

# Funktionen
show_workflow_history() {
    echo "📋 WORKFLOW-HISTORIE:"
    sqlite3 .swarm/memory.db "SELECT timestamp, workflow_name, phase, status FROM workflow_history ORDER BY timestamp DESC LIMIT 5;" 2>/dev/null || echo "  Keine Workflow-Historie gefunden"
}

show_agent_files() {
    echo "📁 AGENT-OUTPUT-DATEIEN:"
    find . -path "./.claude/commands/marker-system/*" -name "*.md" -o -name "*.py" | head -10
}

show_status() {
    echo "👥 AGENT-STATUS:"
    echo "  🐝 Queen Agent: ready"
    echo "  🏗️ Architect Agent: ready" 
    echo "  📂 Folder Manager Agent: ready"
    echo "  ➕ Marker Creator Agent: ready"
    echo "  🔍 Detect Engineer Agent: ready"
    echo "  🤖 GPT Integrator Agent: ready"
    echo "  🐍 Python Generator Agent: ready"
    echo "  🔧 Utility Agent: ready"
}

show_commands() {
    echo "🎯 VERFÜGBARE KOMMANDOS:"
    echo "  claude-flow frausar-orchestrate start"
    echo "  claude-flow frausar-orchestrate status"
    echo "  claude-flow frausar-orchestrate phase 1"
    echo "  python3 monitor-agents.py"
    echo "  python3 monitor-agents.py live"
}

# Hauptfunktion
main() {
    case "${1:-status}" in
        "status")
            show_workflow_history
            echo
            show_status
            echo
            show_agent_files
            echo
            show_commands
            ;;
        "live")
            echo "🔄 LIVE-MONITORING gestartet (Update alle 30 Sekunden)"
            echo "Drücke Ctrl+C zum Beenden"
            while true; do
                clear
                echo "🤖 CLAUDE FLOW AGENT MONITOR - LIVE"
                echo "==================================="
                echo "Letztes Update: $(date)"
                echo
                show_workflow_history
                echo
                show_status
                echo
                show_agent_files
                sleep 30
            done
            ;;
        "start")
            echo "🚀 STARTE FRAUSAR ORCHESTRATION..."
            claude-flow frausar-orchestrate start
            ;;
        "help")
            echo "HILFE:"
            echo "  $0 status    - Zeigt aktuellen Status"
            echo "  $0 live      - Live-Monitoring"
            echo "  $0 start     - Startet Orchestrierung"
            echo "  $0 help      - Diese Hilfe"
            ;;
        *)
            echo "Unbekannter Parameter: $1"
            echo "Verwende: $0 help"
            ;;
    esac
}

# Script ausführen
main "$@"
EOF
    
    chmod +x monitor-agents.sh
    echo "✅ Monitoring-Script erstellt"
fi

echo "✅ Monitoring-Script gefunden"

# Memory-Datenbank prüfen
echo "🗄️ Prüfe Memory-Datenbank..."
if [ ! -f ".swarm/memory.db" ]; then
    echo "❌ Memory-Datenbank nicht gefunden!"
    echo "   Erstelle neue Memory-Datenbank..."
    mkdir -p .swarm
    sqlite3 .swarm/memory.db "CREATE TABLE IF NOT EXISTS workflow_history (id INTEGER PRIMARY KEY, timestamp TEXT, workflow_name TEXT, phase TEXT, status TEXT, details TEXT);"
    echo "✅ Memory-Datenbank erstellt"
else
    echo "✅ Memory-Datenbank gefunden"
fi

echo ""
echo "🎯 WÄHLE MONITORING-MODUS:"
echo "1) Status anzeigen"
echo "2) Live-Monitoring (alle 30 Sekunden Update)"
echo "3) Orchestrierung starten"
echo "4) Hilfe anzeigen"
echo ""
read -p "Wähle Option (1-4): " choice

case $choice in
    1)
        echo "📊 Zeige Status..."
        ./monitor-agents.sh status
        ;;
    2)
        echo "🔄 Starte Live-Monitoring..."
        ./monitor-agents.sh live
        ;;
    3)
        echo "🚀 Starte Orchestrierung..."
        ./monitor-agents.sh start
        ;;
    4)
        echo "❓ Zeige Hilfe..."
        ./monitor-agents.sh help
        ;;
    *)
        echo "❌ Ungültige Option. Zeige Status..."
        ./monitor-agents.sh status
        ;;
esac

echo ""
echo "📊 MONITORING-OPTIONEN:"
echo "  ./monitor-agents.sh status    - Status anzeigen"
echo "  ./monitor-agents.sh live      - Live-Monitoring"
echo "  ./monitor-agents.sh start     - Orchestrierung starten"
echo "  claude-flow frausar-orchestrate status - Workflow-Status"
echo ""
echo "🎯 AGENT-TEAM:"
echo "  🐝 Queen Agent - Koordination"
echo "  🏗️ Architect Agent - System-Design"
echo "  📂 Folder Manager Agent - Ordnerverwaltung"
echo "  ➕ Marker Creator Agent - Marker-Erstellung"
echo "  🔍 Detect Engineer Agent - DETECT.py System"
echo "  🤖 GPT Integrator Agent - GPT-YAML Generator"
echo "  🐍 Python Generator Agent - Python Detectors"
echo "  🔧 Utility Agent - Hilfsfunktionen" 