#!/bin/bash

# Portfolio Management Suite - Quick Start Script
# 
# Source code is organized in the src/ folder
# All test files are organized in the tests/ folder
# Use: python run_tests.py [options] to run tests from root directory
# Or:  cd tests && python master_test_runner.py [options] to run from tests folder
#
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

modules=("src/tactical_tracker.py" "src/options_tracker.py" "src/options_tracker_ui.py" "src/main_app.py")
missing_modules=()

for module in "${modules[@]}"; do
    if [ ! -f "$module" ]; then
        missing_modules+=("$module")
    fi
done

if [ ${#missing_modules[@]} -ne 0 ]; then
    echo "❌ Missing required modules:"
    printf '   %s\n' "${missing_modules[@]}"
    echo "Please ensure all required files are in the src/ directory."
    exit 1
fi

echo "✅ All modules found"

# Check for and kill all existing Streamlit processes
echo "🔍 Checking for existing Streamlit processes..."

# Kill any Python processes running Streamlit
echo "   Terminating all Streamlit processes..."
pkill -f "streamlit run" 2>/dev/null || true
pkill -f "main_app.py" 2>/dev/null || true

# Kill any processes using common Streamlit ports
for port in 8501 8502 8503 8504 8505; do
    port_pids=$(lsof -ti :$port 2>/dev/null || true)
    if [ ! -z "$port_pids" ]; then
        echo "   Killing processes on port $port: $port_pids"
        for pid in $port_pids; do
            kill -9 $pid 2>/dev/null || true
        done
    fi
done

# Wait for processes to terminate
sleep 3

# Double-check port 8501 specifically
if lsof -ti :8501 >/dev/null 2>&1; then
    echo "   Port 8501 still in use, force killing..."
    lsof -ti :8501 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

echo "✅ Streamlit cleanup completed"

# Start the application
echo ""
echo "🚀 Starting Portfolio Management Suite..."
echo ""
echo "Available Features:"
echo "   ⚡ Tactical Momentum Tracker"
echo "   🛡️ Long-Term Quality Stocks" 
echo "   🎯 Options Trading Tracker"
echo ""
echo "Press Ctrl+C to stop the application"
echo "======================================="

# Run streamlit app and let it choose the port
echo "⏳ Launching application..."
streamlit run src/main_app.py --server.address localhost &
streamlit_pid=$!

# Wait for startup and then detect the actual port
sleep 4

# Find which port our Streamlit process is actually using
actual_port="unknown"
for port in 8501 8502 8503 8504 8505; do
    if lsof -ti :$port >/dev/null 2>&1; then
        actual_port=$port
        break
    fi
done

if [ "$actual_port" != "unknown" ]; then
    echo ""
    echo "✅ Portfolio Management Suite is now running!"
    echo "🌐 Access the application at: http://localhost:$actual_port"
    echo ""
else
    echo ""
    echo "🌐 Application started - check the Streamlit output above for the URL"
    echo ""
fi

# Wait for the background process
wait
