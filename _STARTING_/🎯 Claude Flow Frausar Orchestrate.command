#!/bin/bash

# 🎯 Claude Flow Frausar Orchestrate Starter
# ===========================================
# One-Click Starter für Claude Flow Frausar GUI Upgrade

echo "🎯 CLAUDE FLOW FRAUSAR ORCHESTRATE"
echo "=================================="
echo ""

# Projekt-Pfad setzen
PROJECT_PATH="/Users/benjaminpoersch/claude_curser/claude-flow/claude-flow"
cd "$PROJECT_PATH"

echo "📁 Projekt-Pfad: $PROJECT_PATH"

# Claude Flow Status prüfen
echo "🔍 Prüfe Claude Flow Status..."
if ! command -v claude-flow &> /dev/null; then
    echo "❌ Claude Flow nicht gefunden!"
    echo "   Bitte installiere Claude Flow zuerst."
    exit 1
fi

echo "✅ Claude Flow gefunden"

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

# Workflow-Historie anzeigen
echo ""
echo "📋 AKTUELLE WORKFLOW-HISTORIE:"
sqlite3 .swarm/memory.db "SELECT timestamp, workflow_name, phase, status FROM workflow_history ORDER BY timestamp DESC LIMIT 3;" 2>/dev/null || echo "  Keine Workflow-Historie gefunden"

echo ""
echo "🚀 STARTE FRAUSAR ORCHESTRATION..."
echo "=================================="

# Claude Flow Frausar Orchestrate starten
echo "🎯 Führe aus: claude-flow frausar-orchestrate start"
echo ""

# Führe das Kommando aus
claude-flow frausar-orchestrate start

echo ""
echo "✅ Orchestrierung gestartet!"
echo ""
echo "📊 MONITORING-OPTIONEN:"
echo "  ./monitor-agents.sh status    - Status anzeigen"
echo "  ./monitor-agents.sh live      - Live-Monitoring"
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
echo ""
echo "📁 OUTPUT-VERZEICHNISSE:"
echo "  Frausar_API_GUI/ - Implementierte Features"
echo "  .claude/commands/marker-system/ - Kommando-Definitionen"
echo "  .swarm/memory.db - Workflow-Historie"
echo ""
echo "🎉 Frausar GUI Upgrade läuft jetzt mit Claude Flow!" 