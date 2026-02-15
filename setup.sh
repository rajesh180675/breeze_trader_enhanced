#!/bin/bash
# Breeze Trader Enhanced - Setup Script
# Version: 8.5

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     Breeze Options Trader - Enhanced v8.5 Setup          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Python 3.8+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python $python_version detected"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "   Remove and recreate? (y/n): " recreate
    if [ "$recreate" = "y" ]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p .streamlit
mkdir -p logs
echo "✅ Directories created"
echo ""

# Create secrets template
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "🔐 Creating secrets template..."
    cat > .streamlit/secrets.toml << EOF
# Breeze API Credentials
# Get these from ICICI Breeze portal: https://api.icicidirect.com/apiuser/home

BREEZE_API_KEY = "your_api_key_here"
BREEZE_API_SECRET = "your_api_secret_here"

# Note: Session token must be entered daily in the app
# It expires every 24 hours
EOF
    echo "✅ Secrets template created at .streamlit/secrets.toml"
    echo "   ⚠️  IMPORTANT: Edit this file with your API credentials"
else
    echo "ℹ️  Secrets file already exists"
fi
echo ""

# Create streamlit config
if [ ! -f ".streamlit/config.toml" ]; then
    echo "⚙️  Creating Streamlit configuration..."
    cat > .streamlit/config.toml << EOF
[server]
port = 8501
headless = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#2c3e50"
font = "sans serif"
EOF
    echo "✅ Streamlit configuration created"
else
    echo "ℹ️  Streamlit config already exists"
fi
echo ""

# Run setup verification
echo "🧪 Running setup verification..."
python3 -c "
import sys
print('✅ Python imports verified')

try:
    import streamlit
    print('✅ Streamlit installed')
except ImportError:
    print('❌ Streamlit not found')
    sys.exit(1)

try:
    import pandas
    print('✅ Pandas installed')
except ImportError:
    print('❌ Pandas not found')
    sys.exit(1)

try:
    import numpy
    print('✅ NumPy installed')
except ImportError:
    print('❌ NumPy not found')
    sys.exit(1)

try:
    from breeze_connect import BreezeConnect
    print('✅ Breeze Connect installed')
except ImportError:
    print('❌ Breeze Connect not found')
    sys.exit(1)

print('✅ All core packages verified')
"
echo ""

# Success message
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete! ✨                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Edit credentials:"
echo "   nano .streamlit/secrets.toml"
echo ""
echo "2. Run the application:"
echo "   streamlit run app.py"
echo ""
echo "3. Access in browser:"
echo "   http://localhost:8501"
echo ""
echo "📖 Documentation:"
echo "   - README.md - User guide"
echo "   - REVIEW_REPORT.md - Technical details"
echo ""
echo "⚠️  IMPORTANT NOTES:"
echo "   - Keep secrets.toml secure (never commit to git)"
echo "   - Get fresh session token daily from ICICI portal"
echo "   - Test with small orders first"
echo "   - Always use stop-losses"
echo ""
echo "🎉 Happy Trading!"
echo ""
