#!/bin/bash

# Portfolio Management Suite Installer for macOS
# =============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 Portfolio Management Suite Installer${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${YELLOW}⚠️  This installer is designed for macOS. For other platforms, use pip install.${NC}"
    echo ""
    echo "To install on other platforms:"
    echo "  pip install -e ."
    echo ""
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    echo ""
    echo "Please install Python 3 from:"
    echo "  https://www.python.org/downloads/"
    echo "  or use Homebrew: brew install python"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}✅ Found Python ${PYTHON_VERSION}${NC}"

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is required but not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found pip3${NC}"

# Create virtual environment (optional but recommended)
echo ""
echo -e "${BLUE}🔧 Setting up Python environment...${NC}"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --index-url https://pypi.org/simple/

# Install the package in development mode
echo ""
echo -e "${BLUE}📦 Installing Portfolio Management Suite...${NC}"

# Install basic requirements
pip install -e . --index-url https://pypi.org/simple/

# Install GUI dependencies for macOS
echo "Installing macOS GUI dependencies..."
pip install 'rumps>=0.3.0' --index-url https://pypi.org/simple/

# Install optional development dependencies
read -p "Install development dependencies? (y/N): " install_dev
if [[ $install_dev =~ ^[Yy]$ ]]; then
    echo "Installing development dependencies..."
    pip install -e ".[dev]" --index-url https://pypi.org/simple/
fi

# Create application shortcut
echo ""
echo -e "${BLUE}🚀 Creating application shortcuts...${NC}"

# Create launcher script
LAUNCHER_SCRIPT="$HOME/Applications/Portfolio Suite.command"
mkdir -p "$HOME/Applications"

cat > "$LAUNCHER_SCRIPT" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

# Find the project directory (where this script's parent contains setup.py)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
while [[ "$PROJECT_DIR" != "/" && ! -f "$PROJECT_DIR/setup.py" ]]; do
    PROJECT_DIR="$(dirname "$PROJECT_DIR")"
done

if [[ ! -f "$PROJECT_DIR/setup.py" ]]; then
    # Fallback to current directory of the script
    PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

cd "$PROJECT_DIR"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Launch the application
python -m portfolio_suite --component gui

EOF

chmod +x "$LAUNCHER_SCRIPT"

# Create desktop shortcut
DESKTOP_SHORTCUT="$HOME/Desktop/Portfolio Suite.command"
cp "$LAUNCHER_SCRIPT" "$DESKTOP_SHORTCUT"

# Create dock shortcut (Applications folder)
APPLICATIONS_SHORTCUT="/Applications/Portfolio Suite.command"
sudo cp "$LAUNCHER_SCRIPT" "$APPLICATIONS_SHORTCUT" 2>/dev/null || true

echo -e "${GREEN}✅ Created application shortcuts:${NC}"
echo "  • Desktop: $HOME/Desktop/Portfolio Suite.command"
echo "  • Applications: $HOME/Applications/Portfolio Suite.command"
if [ -f "/Applications/Portfolio Suite.command" ]; then
    echo "  • System Applications: /Applications/Portfolio Suite.command"
fi

# Test installation
echo ""
echo -e "${BLUE}🧪 Testing installation...${NC}"

if python -c "import portfolio_suite; print('✅ Package import successful')" 2>/dev/null; then
    echo -e "${GREEN}✅ Installation test passed${NC}"
else
    echo -e "${RED}❌ Installation test failed${NC}"
    echo "You can still try running the application manually with:"
    echo "  python -m portfolio_suite"
fi

# Create uninstaller
echo ""
echo -e "${BLUE}🗑️  Creating uninstaller...${NC}"

UNINSTALLER_SCRIPT="./uninstall_portfolio_suite.sh"
cat > "$UNINSTALLER_SCRIPT" << 'EOF'
#!/bin/bash

echo "🗑️  Portfolio Management Suite Uninstaller"
echo "=========================================="
echo ""

read -p "Are you sure you want to uninstall Portfolio Management Suite? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo "Removing application shortcuts..."
rm -f "$HOME/Desktop/Portfolio Suite.command"
rm -f "$HOME/Applications/Portfolio Suite.command"
sudo rm -f "/Applications/Portfolio Suite.command" 2>/dev/null || true

echo "Uninstalling Python package..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

pip uninstall portfolio-management-suite -y 2>/dev/null || true

echo "Removing virtual environment..."
rm -rf .venv

echo ""
echo "✅ Portfolio Management Suite has been uninstalled."
echo "Note: Project files and data remain in the current directory."

EOF

chmod +x "$UNINSTALLER_SCRIPT"

echo -e "${GREEN}✅ Created uninstaller: $UNINSTALLER_SCRIPT${NC}"

# Final instructions
echo ""
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo ""
echo "You can now launch Portfolio Management Suite in several ways:"
echo ""
echo -e "${BLUE}Desktop App:${NC}"
echo "  • Double-click 'Portfolio Suite.command' on your Desktop"
echo "  • Or from Applications folder"
echo ""
echo -e "${BLUE}Command Line:${NC}"
echo "  • Desktop GUI: ${YELLOW}portfolio-suite --component gui${NC}"
echo "  • Web Interface: ${YELLOW}portfolio-suite --component web${NC}"
echo "  • Options Only: ${YELLOW}portfolio-suite --component options${NC}"
echo ""
echo -e "${BLUE}Development:${NC}"
echo "  • Activate environment: ${YELLOW}source .venv/bin/activate${NC}"
echo "  • Run tests: ${YELLOW}python -m pytest tests/${NC}"
echo "  • Run directly: ${YELLOW}python -m portfolio_suite${NC}"
echo ""
echo -e "${YELLOW}Note: The first launch may take a moment to initialize.${NC}"
echo ""
