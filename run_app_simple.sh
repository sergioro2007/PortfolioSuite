#!/bin/bash

# Tactical Momentum Portfolio Tracker - Simple Launch Script
# This script runs the Streamlit application with minimal setup

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🚀 Tactical Momentum Portfolio Tracker${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Check only core dependencies (skip visualization packages for now)
echo -e "${BLUE}📦 Checking core dependencies...${NC}"
missing_core=()

if ! python -c "import streamlit" 2>/dev/null; then
    missing_core+=("streamlit")
fi

if ! python -c "import yfinance" 2>/dev/null; then
    missing_core+=("yfinance")
fi

if ! python -c "import pandas" 2>/dev/null; then
    missing_core+=("pandas")
fi

if ! python -c "import numpy" 2>/dev/null; then
    missing_core+=("numpy")
fi

# Install only missing core packages
if [ ${#missing_core[@]} -gt 0 ]; then
    echo -e "${YELLOW}📥 Installing core packages: ${missing_core[*]}${NC}"
    pip install "${missing_core[@]}"
    echo -e "${GREEN}✅ Core dependencies installed${NC}"
else
    echo -e "${GREEN}✅ All core dependencies are ready${NC}"
fi

# Check if the main app file exists
if [ ! -f "streamlit_app.py" ]; then
    echo -e "${RED}❌ Error: streamlit_app.py not found in current directory${NC}"
    echo -e "${RED}   Make sure you're running this script from the project directory${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎯 Starting Tactical Momentum Portfolio Tracker...${NC}"
echo -e "${BLUE}📊 The app will open in your default browser${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop the application${NC}"
echo ""

# Run the Streamlit app
streamlit run streamlit_app.py --server.port 8501 --server.address localhost

echo ""
echo -e "${BLUE}👋 Application stopped. Thank you for using Tactical Momentum Portfolio Tracker!${NC}"
