#!/bin/bash

# Portfolio Management Suite v2.0 Launch Script
# Multi-feature application launcher

echo "🎯 Portfolio Management Suite v2.0"
echo "=================================="
echo "Starting multi-feature portfolio management application..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q streamlit yfinance pandas numpy requests beautifulsoup4

# Clear any previous Streamlit cache
echo "Clearing Streamlit cache..."
streamlit cache clear

# Launch the application
echo ""
echo "🚀 Launching Portfolio Management Suite..."
echo "Opening in your default browser..."
echo ""
echo "Available features:"
echo "  ⚡ Tactical Momentum Tracker"
echo "  🛡️ Long-Term Quality Stocks"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the main application
streamlit run main_app.py --server.headless false --server.port 8502
