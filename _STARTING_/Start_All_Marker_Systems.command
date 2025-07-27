#!/bin/bash

# 🚀 Start All Marker Systems
# ===========================
# Startet alle Marker-bezogenen Systeme mit einem Klick

echo "🚀 START ALL MARKER SYSTEMS"
echo "==========================="
echo ""

# Farben für bessere Lesbarkeit
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktionen
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Projekt-Pfad
PROJECT_PATH="/Users/benjaminpoersch/claude_curser"
cd "$PROJECT_PATH"

print_status "Projekt-Pfad: $PROJECT_PATH"

# 1. Marker Validator Convert starten
print_status "1️⃣ Starte Marker Validator Convert..."
cd "$PROJECT_PATH/Marker_validator_convert"

if [ -f "start-dispatcher-system.command" ]; then
    ./start-dispatcher-system.command &
    print_success "Marker Validator Convert gestartet"
else
    print_warning "Marker Validator Convert Starter nicht gefunden"
fi

# 2. Frausar API GUI starten
print_status "2️⃣ Starte Frausar API GUI..."
cd "$PROJECT_PATH/Frausar_API_GUI"

if [ -f "main.py" ]; then
    python3 main.py &
    print_success "Frausar API GUI gestartet"
else
    print_warning "Frausar API GUI nicht gefunden"
fi

# 3. Claude Flow starten
print_status "3️⃣ Starte Claude Flow..."
cd "$PROJECT_PATH/claude-flow/claude-flow"

if [ -d ".claude" ]; then
    print_success "Claude Flow bereit"
    print_status "Claude Flow Commands verfügbar:"
    echo "  - marker-validate"
    echo "  - marker-repair"
    echo "  - marker-convert"
    echo "  - marker-test"
    echo "  - bug-fix-agent"
    echo "  - feature-migrator"
else
    print_warning "Claude Flow nicht gefunden"
fi

# 4. Status anzeigen
echo ""
print_status "📊 System-Status:"
echo "  • Marker Validator Convert: http://localhost:4000"
echo "  • Frausar API GUI: http://localhost:8000"
echo "  • Claude Flow: Bereit für Commands"

# 5. GitHub Repositories
echo ""
print_status "🔗 GitHub Repositories:"
echo "  • Marker Validator Convert: https://github.com/DYAI2025/Marker_Validator-Convertor"
echo "  • Frausar API GUI: https://github.com/DYAI2025/frausar-api-gui"
echo "  • Claude Flow Marker System: https://github.com/DYAI2025/claude-flow-marker-system"
echo "  • GPT-YAML Generator: https://github.com/DYAI2025/gpt-yaml-generator"

echo ""
print_success "✅ Alle Marker Systeme gestartet!"
print_status "Drücke Ctrl+C zum Beenden"

# Warten auf Benutzer-Interruption
trap 'echo ""; print_warning "Beende alle Marker Systeme..."; exit 0' INT
while true; do
    sleep 1
done
