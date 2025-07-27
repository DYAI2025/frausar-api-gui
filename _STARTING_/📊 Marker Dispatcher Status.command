#!/bin/bash

# 📊 Marker Dispatcher Status Check
# =================================

echo ""
echo "📊 MARKER DISPATCHER STATUS"
echo "==========================="
echo ""

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Services und ihre Ports
declare -A SERVICES=(
    ["Validator Agent"]="4001"
    ["Repair Agent"]="4002"
    ["Convert Agent"]="4003"
    ["Dispatcher"]="4004"
    ["Dashboard"]="4000"
)

echo -e "${CYAN}🔍 Prüfe Service-Status...${NC}"
echo ""

ALL_RUNNING=true

# Prüfe jeden Service
for SERVICE in "${!SERVICES[@]}"; do
    PORT="${SERVICES[$SERVICE]}"
    
    if curl -s "http://localhost:$PORT/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $SERVICE (Port $PORT) - ONLINE${NC}"
        
        # Zeige zusätzliche Info für Dispatcher
        if [ "$SERVICE" = "Dispatcher" ]; then
            echo -e "${BLUE}   📋 Agent Status:${NC}"
            AGENT_STATUS=$(curl -s "http://localhost:$PORT/agents/meta" 2>/dev/null | head -c 200)
            if [ -n "$AGENT_STATUS" ]; then
                echo "   $AGENT_STATUS..."
            else
                echo "   Status nicht verfügbar"
            fi
        fi
    else
        echo -e "${RED}❌ $SERVICE (Port $PORT) - OFFLINE${NC}"
        ALL_RUNNING=false
    fi
done

echo ""
echo -e "${CYAN}🌐 Verfügbare URLs:${NC}"
echo ""

if [ "$ALL_RUNNING" = true ]; then
    echo -e "${GREEN}🎉 ALLE SERVICES LAUFEN!${NC}"
    echo ""
    echo -e "${BLUE}📊 Dashboard:${NC} http://localhost:4000"
    echo -e "${BLUE}🔧 Dispatcher:${NC} http://localhost:4004"
    echo -e "${BLUE}🤖 Validator:${NC} http://localhost:4001"
    echo -e "${BLUE}🔧 Repair:${NC} http://localhost:4002"
    echo -e "${BLUE}🔧 Convert:${NC} http://localhost:4003"
    echo ""
    echo -e "${YELLOW}💡 Öffne das Dashboard: open http://localhost:4000${NC}"
    echo ""
    
    # Zeige Beispiel-API-Calls
    echo -e "${CYAN}📋 Beispiel API-Calls:${NC}"
    echo "  • curl http://localhost:4004/agents/meta"
    echo "  • curl -X POST 'http://localhost:4004/process?steps=validate' -H 'Content-Type: application/json' -d '{\"id\": \"A_TEST\", \"level\": 1}'"
    echo ""
else
    echo -e "${RED}⚠️  Einige Services sind offline${NC}"
    echo ""
    echo -e "${YELLOW}💡 Starte das System mit: ./🎯 Marker Dispatcher.command${NC}"
fi

echo ""
echo -e "${CYAN}📈 System-Info:${NC}"
echo "  • Node.js Version: $(node --version 2>/dev/null || echo 'Nicht installiert')"
echo "  • Aktuelle Zeit: $(date)"
echo "  • Uptime: $(uptime | awk '{print $3}' | sed 's/,//')"
echo ""

# Prüfe laufende Node.js Prozesse
echo -e "${CYAN}🔍 Laufende Node.js Prozesse:${NC}"
RUNNING_PROCESSES=$(ps aux | grep -E "node.*index\.js" | grep -v grep | wc -l)
if [ "$RUNNING_PROCESSES" -gt 0 ]; then
    echo -e "${GREEN}✅ $RUNNING_PROCESSES Node.js Prozesse laufen${NC}"
    ps aux | grep -E "node.*index\.js" | grep -v grep | awk '{print "  • " $11 " (PID: " $2 ")"}'
else
    echo -e "${RED}❌ Keine Node.js Prozesse gefunden${NC}"
fi

echo ""
