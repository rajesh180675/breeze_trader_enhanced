#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Breeze Options Trader PRO - Linux/Mac Setup Script
# ═══════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Breeze Options Trader PRO - Installation Script        ║"
echo "║              Linux/Mac Version                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "  Mac: brew install python3"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Python found${NC}"
python3 --version
echo ""

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed${NC}"
    echo "Please install pip3"
    exit 1
fi

echo -e "${GREEN}✓ pip3 found${NC}"
echo ""

# Create virtual environment
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ Pip upgraded${NC}"
echo ""

# Install dependencies
echo "Installing dependencies..."
if pip install -r requirements.txt --quiet; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    echo ""
    echo "Trying with verbose output..."
    pip install -r requirements.txt
    exit 1
fi
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p data logs exports
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Set permissions
echo "Setting permissions..."
chmod +x run.sh
chmod +x setup.sh
echo -e "${GREEN}✓ Permissions set${NC}"
echo ""

# Initialize database
echo "Initializing database..."
if python3 -c "from persistence import TradeDB; db = TradeDB(); print('Database ready')" 2>/dev/null; then
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${YELLOW}⚠️ Database initialization warning (non-critical)${NC}"
fi
echo ""

# Configuration check
echo "Checking configuration..."
if [ -f "user_config.py" ]; then
    echo -e "${GREEN}✓ User configuration found${NC}"
else
    echo -e "${YELLOW}⚠️ user_config.py not found - using defaults${NC}"
fi
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "  Installation Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🚀 To start the application, run:"
echo ""
echo "    ./run.sh"
echo ""
echo "Or manually with:"
echo "    source venv/bin/activate"
echo "    streamlit run app_enhanced.py"
echo ""
echo "📚 For detailed documentation, see README.md"
echo "═══════════════════════════════════════════════════════════"
echo ""
