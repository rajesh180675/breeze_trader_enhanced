#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Breeze Options Trader PRO - Linux/Mac Run Script
# ═══════════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        Starting Breeze Options Trader PRO...             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo ""
    echo "Please run ./setup.sh first to install dependencies."
    echo ""
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start Streamlit app
echo -e "${GREEN}Starting application...${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Application will open in your default browser"
echo "  Press Ctrl+C to stop the application"
echo "═══════════════════════════════════════════════════════════"
echo ""

streamlit run app_enhanced.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Application exited with an error${NC}"
    echo ""
    exit 1
fi
