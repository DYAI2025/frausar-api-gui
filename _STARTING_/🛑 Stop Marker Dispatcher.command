#!/bin/bash

# 🛑 Stop Marker Dispatcher System
# ================================

echo ""
echo "🛑 STOP MARKER DISPATCHER SYSTEM"
echo "================================"
echo ""

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🛑 Stoppe alle Marker Dispatcher Services...${NC}"
echo ""

# Stoppe alle Node.js Prozesse die zu Marker Dispatcher gehören
echo "Suche nach laufenden Services..."

# Finde und stoppe alle relevanten Prozesse
PIDS=$(ps aux | grep -E "node.*index\.js" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo -e "${GREEN}✅ Keine laufenden Services gefunden${NC}"
else
    echo "Gefundene Prozesse:"
    ps aux | grep -E "node.*index\.js" | grep -v grep
    
    echo ""
    echo -e "${YELLOW}Stoppe Prozesse...${NC}"
    
    for PID in $PIDS; do
        echo "Stoppe Prozess $PID"
        kill $PID 2>/dev/null
    done
    
    # Warte kurz und prüfe ob noch Prozesse laufen
    sleep 2
    
    REMAINING=$(ps aux | grep -E "node.*index\.js" | grep -v grep | awk '{print $2}')
    if [ -n "$REMAINING" ]; then
        echo -e "${RED}Erzwinge Stopp der verbleibenden Prozesse...${NC}"
        for PID in $REMAINING; do
            kill -9 $PID 2>/dev/null
        done
    fi
    
    echo -e "${GREEN}✅ Alle Services gestoppt${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Marker Dispatcher System erfolgreich gestoppt!${NC}"
echo ""
echo "Services die gestoppt wurden:"
echo "  • Validator Agent (Port 4001)"
echo "  • Repair Agent (Port 4002)"
echo "  • Convert Agent (Port 4003)"
echo "  • Dispatcher (Port 4004)"
echo "  • Dashboard (Port 4000)"
echo ""

# Prüfe ob Ports noch belegt sind
echo -e "${YELLOW}🔍 Prüfe Port-Status...${NC}"
PORTS=(4000 4001 4002 4003 4004)

for PORT in "${PORTS[@]}"; do
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}⚠️  Port $PORT ist noch belegt${NC}"
    else
        echo -e "${GREEN}✅ Port $PORT ist frei${NC}"
    fi
done

echo ""
echo -e "${GREEN}✅ Cleanup abgeschlossen${NC}"
echo ""
