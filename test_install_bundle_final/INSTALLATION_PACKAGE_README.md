# 📦 Portfolio Management Suite - Installation Package

## 🎯 What You Have

This package contains everything needed to install and run the Portfolio Management Suite on any computer.

## 📋 Package Contents

```
dist/
├── portfolio_management_suite-2.0.0-py3-none-any.whl    # Main installation file (10KB)
└── portfolio_management_suite-2.0.0.tar.gz              # Source distribution (190KB)

Additional Files:
├── requirements.txt                                       # Dependencies list
├── INSTALLATION_PACKAGE_README.md                       # This file
└── .streamlit/config.toml                               # Configuration file
```

## 🚀 How to Install on Another Computer

### Prerequisites
- Python 3.8 or higher
- Internet connection (for downloading dependencies)

### Installation Steps

#### Method 1: Install from Wheel (Recommended - Fastest)
```bash
# 1. Create a new directory for the project
mkdir portfolio_suite
cd portfolio_suite

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# 4. Install the package (always use public PyPI index to avoid private index errors)
python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple --upgrade pip setuptools wheel
python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple ./portfolio_management_suite-2.0.0-py3-none-any.whl

# 5. Install additional dependencies (using public PyPI)
python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple streamlit>=1.25.0 yfinance>=0.2.0 pandas>=2.0.0 numpy>=1.24.0 requests>=2.31.0 beautifulsoup4>=4.12.0
```

#### Method 2: Install from Source
```bash
# 1. Extract the source distribution
tar -xzf portfolio_management_suite-2.0.0.tar.gz
cd portfolio_management_suite-2.0.0

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Install the package (using public PyPI)
python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple --upgrade pip setuptools wheel
python3 -m pip install --no-cache-dir --index-url https://pypi.org/simple -e .
## ⚠️ Troubleshooting: Private Index Errors

If you see errors about a private index (e.g. `http://pypi.tat.ford.com/root/internal/+simple/`), you must force pip to use the public index as above. You may also need to temporarily move or comment out any `pip.conf` or `PIP_INDEX_URL` environment variable that sets a private index.

## 🔨 Build from Source (with public PyPI)

Use the provided `build.sh` script to build the package, always using the public PyPI index:

```sh
bash build.sh
```

This will:
- Upgrade build tools from public PyPI
- Build both wheel and source distributions in `dist/`

---

For more details, see the comments in each script or contact the maintainer.
```

### Setup Configuration (Optional)
```bash
# Create .streamlit directory and copy config
mkdir -p .streamlit
# Copy the config.toml file to .streamlit/config.toml
```

## 🎮 How to Run

After installation, you can run the application in multiple ways:

### Command Line Interface
```bash
# Activate environment first
source .venv/bin/activate

# Launch full GUI application
portfolio-suite

# Launch web interface
portfolio-suite --component web

# Launch specific modules
portfolio-suite --component options    # Options Trading
portfolio-suite --component tactical   # Tactical Tracker
portfolio-suite --component analysis   # Trade Analysis
```

### Direct Module Access
```bash
# Trade Analysis CLI
python -m portfolio_suite.trade_analysis.cli analyze AAPL
python -m portfolio_suite.trade_analysis.cli suggest SPY QQQ
python -m portfolio_suite.trade_analysis.cli summary

# Web Interface (if you have the full source)
streamlit run portfolio_suite/ui/main_app.py
```

## 🎯 What You Get

### Core Features
- **Options Trading Tracker**: Track options positions with real-time implied volatility
- **Tactical Momentum Tracker**: Market timing and momentum analysis
- **Trade Analysis**: Real-time stock analysis with technical indicators
- **Web Interface**: Browser-based access at http://localhost:8501
- **CLI Tools**: Command-line analysis tools

### Example Usage
```bash
# Get analysis for Apple stock
portfolio-analysis analyze AAPL

# Get trade suggestions for multiple stocks  
portfolio-analysis suggest SPY QQQ AAPL

# Launch web interface
portfolio-suite --component web
```

## 📊 Test Installation

To verify everything works:

```bash
# Test package import
python -c "import portfolio_suite; print('✅ Installation successful!')"

# Test trade analysis
portfolio-analysis analyze SPY

# Launch web interface
portfolio-suite --component web
```

## 🔧 Troubleshooting

### Common Issues

1. **Python Version**: Ensure Python 3.8+
   ```bash
   python --version
   ```

2. **Virtual Environment**: Always activate before running
   ```bash
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Dependencies**: If imports fail, reinstall dependencies
   ```bash
   pip install --upgrade streamlit yfinance pandas numpy requests beautifulsoup4
   ```

4. **Port Issues**: Default port is 8501. If busy, Streamlit will auto-select another.

### Network Requirements
- Internet access for real-time market data (yfinance)
- Port 8501 for web interface (or auto-selected alternative)

## 📦 Package Information

- **Name**: portfolio-management-suite
- **Version**: 2.0.0
- **Size**: ~10KB (wheel), ~190KB (source)
- **Python**: 3.8+
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **License**: MIT

## 🎉 Ready to Use!

Your Portfolio Management Suite package is ready for distribution and installation on any computer with Python 3.8+.

---

**Package Created**: July 7, 2025  
**Version**: 2.0.0  
**Status**: Production Ready ✅
