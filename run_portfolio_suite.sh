#!/bin/bash

# Portfolio Management Suite - Quick Start Script
echo "🎯 Portfolio Management Suite - Starting Application..."
echo "======================================================="

# Check Python environment
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed or not in PATH"
    exit 1
fi

# Check if streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing required packages..."
    pip3 install -r requirements.txt
fi

# Check if required modules exist
echo "🔍 Checking required modules..."

modules=("tactical_tracker.py" "options_tracker.py" "options_tracker_ui.py" "main_app.py")
missing_modules=()

for module in "${modules[@]}"; do
    if [ ! -f "$module" ]; then
        missing_modules+=("$module")
    fi
done

if [ ${#missing_modules[@]} -ne 0 ]; then
    echo "❌ Missing required modules:"
    printf '   %s\n' "${missing_modules[@]}"
    echo "Please ensure all required files are in the current directory."
    exit 1
fi

echo "✅ All modules found"

# Start the application
echo ""
echo "🚀 Starting Portfolio Management Suite..."
echo "   Navigate to: http://localhost:8501"
echo ""
echo "Available Features:"
echo "   ⚡ Tactical Momentum Tracker"
echo "   🛡️ Long-Term Quality Stocks" 
echo "   🎯 Options Trading Tracker"
echo ""
echo "Press Ctrl+C to stop the application"
echo "======================================="

# Run streamlit app
streamlit run main_app.py --server.port 8501 --server.address localhost
