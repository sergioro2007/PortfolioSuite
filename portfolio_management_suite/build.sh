#!/bin/bash
cd "$(dirname "$0")"
# Universal build/install script for Portfolio Management Suite
# Ensures public PyPI is used for all dependencies and build tools

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check for pip config that sets a private index
PIP_CONF_GLOBAL=$(python3 -c 'import sys; print(sys.prefix + "/etc/pip.conf")')
PIP_CONF_USER="$HOME/.pip/pip.conf"
PIP_CONF_ENV="$PIP_CONFIG_FILE"

warn_private_index() {
    echo -e "${YELLOW}⚠️  Detected a pip config or environment variable that may set a private index.\n   This build will use the public PyPI index for all operations.${NC}"
}

if [ -f "$PIP_CONF_GLOBAL" ] || [ -f "$PIP_CONF_USER" ] || [ ! -z "$PIP_CONF_ENV" ]; then
    warn_private_index
fi

# Upgrade pip, setuptools, wheel from public PyPI
python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple --upgrade pip setuptools wheel


# Build the package (source and wheel) with public PyPI index for isolated build env
echo -e "${BLUE}🔨 Building package...${NC}"
python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple build
PIP_INDEX_URL=https://pypi.org/simple python3 -m build


echo -e "${GREEN}✅ Build complete. Distributions are in the dist/ directory.${NC}"

# Copy the .tar.gz and quick_install.sh to distribution_package (if not already there)

# Copy all necessary files to distribution_package
cp dist/portfolio_management_suite-*.whl dist/portfolio_management_suite-*.tar.gz quick_install.sh requirements.txt INSTALLATION_PACKAGE_README.md config.toml distribution_package/

# Create a fresh install bundle zip in distribution_package
cd distribution_package
rm -f portfolio_management_suite_install_bundle.zip
zip -r portfolio_management_suite_install_bundle.zip portfolio_management_suite-*.whl portfolio_management_suite-*.tar.gz quick_install.sh requirements.txt INSTALLATION_PACKAGE_README.md config.toml
cd ..

echo -e "${GREEN}✅ Install bundle created: distribution_package/portfolio_management_suite_install_bundle.zip${NC}"

# To install the package (uncomment if you want auto-install after build):
# echo -e "${BLUE}📦 Installing built package...${NC}"
# python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple dist/*.whl
# echo -e "${GREEN}✅ Installation complete.${NC}"
