#!/bin/bash

# Portfolio Suite Launcher
# Activates environment and launches the web interface

echo "🚀 Starting Portfolio Management Suite..."
echo "============================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencies not installed. Installing now..."
    pip install --index-url https://pypi.org/simple/ -r requirements.txt
fi

echo "✅ Environment ready"
echo "📊 Launching Portfolio Suite Web Interface..."
echo ""
echo "🌐 Open your browser to: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Launch the web interface
python -m src.portfolio_suite --component web --host localhost --port 8501
