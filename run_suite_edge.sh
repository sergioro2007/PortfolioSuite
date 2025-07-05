#!/bin/bash

# Edge-Compatible Portfolio Suite Launch Script
echo "🎯 Portfolio Management Suite v2.0 (Edge Compatible)"
echo "=================================================="
echo "Starting Edge-compatible portfolio management application..."
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

# Launch with Edge-friendly settings
echo ""
echo "🚀 Launching Portfolio Management Suite (Edge Compatible)..."
echo "Opening at: http://localhost:8503"
echo ""
echo "Available features:"
echo "  ⚡ Tactical Momentum Tracker"
echo "  🛡️ Long-Term Quality Stocks"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run with specific settings for Edge compatibility
streamlit run src/main_app.py \
  --server.port 8503 \
  --server.headless false \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --browser.gatherUsageStats false
