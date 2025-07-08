#!/bin/bash
# Portfolio Management Suite - Quick Installer
# Run this script to automatically set up the Portfolio Management Suite

set -e  # Exit on any error

# Force pip to use the public PyPI index for all installs, overriding any system/user config
export PIP_INDEX_URL=https://pypi.org/simple

echo "🚀 Portfolio Management Suite - Quick Installer"
echo "=============================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Create project directory
PROJECT_DIR="portfolio_suite_app"
echo "📁 Creating directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate


# Always use public PyPI index for all installs
echo "📦 Installing Portfolio Management Suite (using public PyPI index)..."
if [ -f "../portfolio_management_suite-2.0.0-py3-none-any.whl" ]; then
    python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple ../portfolio_management_suite-2.0.0-py3-none-any.whl
else
    echo "❌ Wheel file not found. Please ensure portfolio_management_suite-2.0.0-py3-none-any.whl is in the same directory as this script."
    exit 1
fi

# Install dependencies from public PyPI
echo "📚 Installing dependencies (using public PyPI index)..."
python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple streamlit>=1.25.0 yfinance>=0.2.0 pandas>=2.0.0 numpy>=1.24.0 requests>=2.31.0 beautifulsoup4>=4.12.0

# Create .streamlit directory and config
echo "⚙️ Setting up configuration..."
mkdir -p .streamlit
if [ -f "../config.toml" ]; then
    cp ../config.toml .streamlit/
else
    # Create default config
    cat > .streamlit/config.toml << EOF
[server]
headless = false
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
EOF
fi

# Test installation
echo "🧪 Testing installation..."
if python -c "import portfolio_suite; print('✅ Portfolio Suite imported successfully')" 2>/dev/null; then
    echo "✅ Installation successful!"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Create launcher scripts
echo "🎯 Creating launcher scripts..."


# Web launcher (runs Streamlit app directly for maximum reliability)
cat > launch_web.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
main_app_path=$(python -c 'import sys; import portfolio_suite.ui.main_app; sys.stdout.write(portfolio_suite.ui.main_app.__file__)')
streamlit run "$main_app_path"
EOF
chmod +x launch_web.sh

# GUI launcher
cat > launch_gui.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
portfolio-suite
EOF
chmod +x launch_gui.sh

# Analysis CLI launcher
cat > analyze.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python -m portfolio_suite.trade_analysis.cli "$@"
EOF
chmod +x analyze.sh

echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "📍 Installation location: $(pwd)"
echo ""
echo "🚀 How to run:"
echo "   ./launch_web.sh      - Launch web interface"
echo "   ./launch_gui.sh      - Launch GUI application"
echo "   ./analyze.sh AAPL    - Analyze a stock"
echo ""
echo "📖 For more options, see INSTALLATION_PACKAGE_README.md"
echo ""
echo "🌐 Web interface will be available at: http://localhost:8501"
echo ""
