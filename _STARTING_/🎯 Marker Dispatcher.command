#!/bin/bash

# 🎯 Marker Dispatcher System - One Click Starter
# ==============================================

echo ""
echo "🎯 MARKER DISPATCHER SYSTEM"
echo "==========================="
echo ""

# Farben für bessere Lesbarkeit
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Pfad zum Marker Validator Projekt
PROJECT_PATH="/Users/benjaminpoersch/claude_curser/Marker_validator_convert"

# Prüfe ob das Projekt existiert
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}❌ Projekt nicht gefunden: $PROJECT_PATH${NC}"
    echo "Bitte überprüfe den Pfad und versuche es erneut."
    exit 1
fi

echo -e "${CYAN}📁 Projekt-Pfad: $PROJECT_PATH${NC}"
echo ""

# Prüfe Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js ist nicht installiert!${NC}"
    echo "Bitte installiere Node.js von https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✅ Node.js gefunden: $(node --version)${NC}"
echo ""

# Stoppe alle laufenden Services
echo -e "${YELLOW}🛑 Stoppe alle laufenden Services...${NC}"
pkill -f "node index.js" 2>/dev/null
sleep 2

# Wechsle zum Projekt-Verzeichnis
cd "$PROJECT_PATH"

echo -e "${BLUE}🚀 Starte Marker Dispatcher System...${NC}"
echo ""

# Starte alle Services
echo -e "${PURPLE}1️⃣  Starte Validator Agent (Port 4001)...${NC}"
cd packages/subagents/validator
npm install > /dev/null 2>&1
node index.js > /dev/null 2>&1 &
VALIDATOR_PID=$!
sleep 2

echo -e "${PURPLE}2️⃣  Starte Repair Agent (Port 4002)...${NC}"
cd ../repair
npm install > /dev/null 2>&1
node index.js > /dev/null 2>&1 &
REPAIR_PID=$!
sleep 2

echo -e "${PURPLE}3️⃣  Starte Convert Agent (Port 4003)...${NC}"
cd ../convert
npm install > /dev/null 2>&1
node index.js > /dev/null 2>&1 &
CONVERT_PID=$!
sleep 2

echo -e "${PURPLE}4️⃣  Starte Dispatcher (Port 4004)...${NC}"
cd ../../dispatcher
npm install > /dev/null 2>&1
node index.js > /dev/null 2>&1 &
DISPATCHER_PID=$!
sleep 2

echo -e "${PURPLE}5️⃣  Starte Dashboard (Port 4000)...${NC}"
cd ../subagents/dashboard
npm install > /dev/null 2>&1
node index.js > /dev/null 2>&1 &
DASHBOARD_PID=$!
sleep 3

# Prüfe ob alle Services laufen
echo ""
echo -e "${CYAN}🔍 Prüfe Service-Status...${NC}"
sleep 2

# Health Checks
SERVICES=(
    "http://localhost:4001/health"
    "http://localhost:4002/health"
    "http://localhost:4003/health"
    "http://localhost:4004/health"
    "http://localhost:4000"
)

SERVICE_NAMES=(
    "Validator Agent"
    "Repair Agent"
    "Convert Agent"
    "Dispatcher"
    "Dashboard"
)

ALL_RUNNING=true

for i in "${!SERVICES[@]}"; do
    if curl -s "${SERVICES[$i]}" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ ${SERVICE_NAMES[$i]} läuft${NC}"
    else
        echo -e "${RED}❌ ${SERVICE_NAMES[$i]} nicht erreichbar${NC}"
        ALL_RUNNING=false
    fi
done

echo ""
if [ "$ALL_RUNNING" = true ]; then
    echo -e "${GREEN}🎉 ALLE SERVICES LAUFEN ERFOLGREICH!${NC}"
    echo ""
    echo -e "${CYAN}🌐 DASHBOARD:${NC} http://localhost:4000"
    echo -e "${CYAN}🔧 DISPATCHER:${NC} http://localhost:4004"
    echo -e "${CYAN}🤖 VALIDATOR:${NC} http://localhost:4001"
    echo -e "${CYAN}🔧 REPAIR:${NC} http://localhost:4002"
    echo -e "${CYAN}🔧 CONVERT:${NC} http://localhost:4003"
    echo ""
    echo -e "${YELLOW}💡 Tipp: Öffne http://localhost:4000 im Browser für das Dashboard${NC}"
    echo ""
    echo -e "${BLUE}📋 Verfügbare Endpunkte:${NC}"
    echo "  • POST /process?steps=validate,repair,convert"
    echo "  • GET /agents/meta"
    echo "  • GET /agents/status"
    echo ""
else
    echo -e "${RED}⚠️  Einige Services konnten nicht gestartet werden${NC}"
    echo "Überprüfe die Logs und versuche es erneut."
fi

echo ""
echo -e "${YELLOW}⏹️  Drücke Ctrl+C um alle Services zu stoppen${NC}"
echo ""

# Warte auf Benutzer-Interruption
trap 'cleanup' INT

cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stoppe alle Services...${NC}"
    
    # Stoppe alle Services
    kill $VALIDATOR_PID 2>/dev/null
    kill $REPAIR_PID 2>/dev/null
    kill $CONVERT_PID 2>/dev/null
    kill $DISPATCHER_PID 2>/dev/null
    kill $DASHBOARD_PID 2>/dev/null
    
    # Zusätzlicher Cleanup
    pkill -f "node index.js" 2>/dev/null
    
    echo -e "${GREEN}✅ Alle Services gestoppt${NC}"
    echo ""
    exit 0
}

# Warte auf Benutzer-Interruption
wait
