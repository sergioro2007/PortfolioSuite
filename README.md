# Portfolio Management Suite v2.0.0

A comprehensive, multi-feature investment analysis platform with professional-grade portfolio management tools for tactical, long-term, and options trading strategies.

---

## 🎯 Features Overview

- **Tactical Momentum Portfolio Tracker**: Automated momentum screening, real-time market health, dynamic cash allocation, and historical comparison.
- **Long-Term Quality Stocks Tracker**: Fundamental quality screening, defensive sector focus, low volatility, and minimal rotation.
- **Options Trading Tracker**: Weekly income targeting, multiple options strategies, technical analysis, and trade memory.
- **Unified Web & CLI Interface**: Access all modules via browser or command line.
- **Cross-Platform GUI**: Native desktop launcher for macOS and Windows.

---

## � Project Structure

```
Portfolio-Management-Suite/
├── portfolio_suite/              # Main application package
│   ├── options_trading/          # Options module
│   ├── tactical_tracker/         # Momentum module
│   ├── trade_analysis/           # Analysis module
│   ├── ui/                       # Web interface
│   └── gui/                      # Desktop GUI
├── .streamlit/                   # Streamlit configuration
├── data/                         # Sample data
├── tests/                        # Essential tests
├── distribution_package/         # Ready-to-ship install package
├── requirements.txt              # Python dependencies
├── setup.py, pyproject.toml      # Packaging config
├── quick_install.sh              # Auto installer
├── INSTALLATION_PACKAGE_README.md# End-user install guide
├── CLEANUP_SUMMARY.md            # Cleanup report
└── README.md                     # This documentation
```

---

## 🚀 Installation

### **Recommended: Use the Distribution Package**

1. **Unzip** `portfolio_management_suite_v2.0.0_installation_package.zip`
2. **Run the installer:**
   ```bash
   cd distribution_package
   ./quick_install.sh
   ```
   This sets up a virtual environment, installs all dependencies, and creates launch scripts.

3. **For detailed instructions:**  
   See `INSTALLATION_PACKAGE_README.md` in the package.

### **Manual Install (Advanced)**

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install the package:
   ```bash
   pip install distribution_package/portfolio_management_suite-2.0.0-py3-none-any.whl
   pip install -r requirements.txt
   ```

---

## 🎮 Usage

### **Web Interface**
```bash
# From the project directory (after activating the environment)
portfolio-suite --component web
# Or use the launch_web.sh script created by the installer
./launch_web.sh
```
Open your browser to [http://localhost:8501](http://localhost:8501)

### **Full GUI Application**
```bash
portfolio-suite
# Or use the launch_gui.sh script
./launch_gui.sh
```

### **Command Line Analysis**
```bash
portfolio-suite --component options    # Options Trading
portfolio-suite --component tactical   # Tactical Tracker
portfolio-suite --component analysis   # Trade Analysis

# Or direct module access:
python -m portfolio_suite.trade_analysis.cli analyze AAPL
python -m portfolio_suite.trade_analysis.cli suggest SPY QQQ
python -m portfolio_suite.trade_analysis.cli summary
```

---

## 🧪 Testing

Run the essential test suite:
```bash
cd tests
python run_tests.py
```
Or run individual test files as needed.

---

## 🛠️ Requirements

- Python 3.8+
- Internet connection (for real-time market data)
- Web browser (for Streamlit interface)

All dependencies are listed in `requirements.txt`.

---

## 📄 Documentation

- **INSTALLATION_PACKAGE_README.md**: End-user installation and troubleshooting
- **CLEANUP_SUMMARY.md**: Details of project cleanup and structure
- **PORT_CONFIGURATION.md**: (Optional) Port customization info

---

## 🏆 Status

- **Version**: 2.0.0
- **Production Ready**: Yes
- **Distribution Package**: `portfolio_management_suite_v2.0.0_installation_package.zip`

---

*For more details, see the full installation guide in your distribution package.*

---
- **🟡 DEFENSIVE** (3 signals): **15% cash** - Moderate risk reduction
- **🔴 HIGHLY_DEFENSIVE** (4+ signals): **30% cash** - Significant capital preservation

#### 📊 Two-Tier Position Sizing System
- **Strong Buy positions** (8-20% allocation): Momentum score >15 AND weekly return >2.0%
- **Moderate Buy positions** (3-12% allocation): Momentum score >10 (excluding strong buys)
- **Integer-only percentages** for practical implementation
- **Automatic scaling to 100%** with priority-based adjustments

#### ⚡ Strict Tactical Momentum Rules
- **Pre-qualification requirement**: 3 of 4 weeks >2% gain AND average weekly >1.5%
- **Market cap threshold**: >$5B for institutional-quality liquidity
- **Daily reevaluation logic**: 
  - Drop >3% → Review/Exit
  - Drop >1.5% → Watch closely
  - Gain >2% → Strong Momentum

#### 📈 Historical Comparison Tracking
- **"Changes Since Last Analysis"** feature with `data/portfolio_results.pkl` storage
- **Comprehensive comparison metrics**: new entries, dropped stocks, performance changes
- **Actionable recommendations** based on historical performance patterns
- **Portfolio evolution tracking** over time

## � Project Structure

The Portfolio Management Suite is organized with a clean separation of concerns:

```
Portfolio-Management-Suite/
├── src/                          # 📦 Source Code
│   ├── __init__.py              # Package initialization
│   ├── main_app.py              # 🎯 Main Streamlit application
│   ├── tactical_tracker.py     # ⚡ Tactical momentum tracking
│   ├── quality_tracker.py      # 🛡️ Long-term quality stocks
│   ├── options_tracker.py      # 🎯 Options trading strategies
│   ├── options_tracker_ui.py   # 🖥️ Options UI components
│   ├── streamlit_app.py        # 📊 Legacy Streamlit app
│   └── options_analyzer.py     # 🔍 Options analysis utilities
├── tests/                       # 🧪 Test Suite
│   ├── master_test_runner.py   # Main test orchestrator
│   ├── test_*.py               # Test files by category
│   ├── debug_*.py              # Debug and verification scripts
│   └── run_*.py                # Various test runners
├── data/                        # 📊 Data Storage
│   ├── portfolio_results.pkl   # Historical analysis results
│   └── options_trades.pkl      # Options trade history
├── run_portfolio_suite.sh      # 🚀 Main application launcher
├── run_tests.py               # 🧪 Test launcher (from root)
├── requirements.txt           # 📋 Python dependencies
└── README.md                  # 📖 This documentation
```

### Key Benefits of This Structure

- **Clean Separation**: Source code in `src/`, tests in `tests/`, data in `data/`, configuration in root
- **Easy Navigation**: All related files grouped together
- **Import Clarity**: Clear import paths and module organization
- **Data Organization**: Historical data and trade records stored separately in `data/`
- **Testing**: Comprehensive test suite with organized categories
- **Deployment**: Simple launch scripts for different use cases

## 🚀 Quick Start

### Installation
```bash
# Clone or download the project
cd Portfolio-Management-Suite

# Install required dependencies
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Complete Portfolio Suite (Recommended)
```bash
./run_portfolio_suite.sh
```

#### Option 2: Direct Streamlit Launch
```bash
# Run the complete multi-feature application
streamlit run src/main_app.py
```

#### Option 3: Legacy Tactical Tracker Only
```bash
# For the original tactical momentum tracker only
./run_app.sh
# or
streamlit run src/streamlit_app.py
```

## 📱 Using the Application

### 🎯 Feature Selection
1. **Home Page**: Overview of both investment approaches and guidance
2. **⚡ Tactical Momentum Tracker**: Active trading and momentum strategies  
3. **🛡️ Long-Term Quality Stocks**: Conservative, dividend-focused investing

### ⚡ Tactical Momentum Tracker Usage
1. **Configure Parameters**:
   - Set minimum RS score (20-100)
   - Set minimum weekly return target (0.5%-5.0%)
   - Adjust allocation weights and portfolio size
   - **Enable/disable deterministic mode** (Advanced Settings)
   - **Toggle defensive cash allocation** (Allow Defensive Cash checkbox)

2. **Run Screening**:
   - Click "Run Screening" to discover qualified tickers
   - **Automatic pre-qualification**: Only tickers meeting 3 of 4 weeks >2% gain AND avg >1.5% are scored
   - Review market health indicators and **6-signal defensive score**
   - **View real-time market regime classification** (Aggressive/Cautious/Defensive/Highly Defensive)
   - Examine results with detailed metrics and reasoning

3. **Monitor Portfolio**:
   - Track **dynamic cash allocation** (0-30%) based on market conditions
   - **Two-tier position sizing**: Strong Buys (8-20%) vs Moderate Buys (3-12%)
   - Get buy/sell/hold recommendations with **automatic integer percentage allocation**
   - Monitor real-time performance and allocation percentages
   - **Review "Changes Since Last Analysis"** for historical comparison tracking
   - **Daily reevaluation alerts** for positions dropping >1.5% or >3%

### 🛡️ Long-Term Quality Stocks Usage
1. **Configure Quality Filters**:
   - Set minimum ROE and maximum beta thresholds
   - Choose preferred defensive sectors
   - Set dividend yield and market cap requirements

2. **Run Quality Analysis**:
   - Analyze fundamental quality metrics
   - Review defensive characteristics and sector allocation
   - Get long-term performance validation

3. **Weekly Tracking**:
   - Monitor minimal rotation requirements
   - Track consistency in quality metrics
   - Review performance vs benchmarks

### 🎯 Options Trading Tracker Usage
1. **Configure Options Strategies**:
   - Select desired strategy type(s): Bull Put Spread, Bear Call Spread, Iron Condor, Broken Wing Butterfly
   - Set target weekly income (recommended: $500+)
   - Adjust position size and risk parameters

2. **Run Options Screening**:
   - Click "Run Options Screening" to find suitable trades
   - Review 1-week price predictions and technical indicator analysis
   - Examine trade candidates with detailed profit/loss projections

3. **Manage Options Trades**:
   - Track open positions and monitor P&L
   - Receive automated recommendations to Hold/Close/Adjust trades
   - Analyze strategy performance and make adjustments as needed

## 🔧 Features

### ⚡ Tactical Momentum Features
- ✅ **Automated ticker discovery** from major indices (500+ tickers screened)
- ✅ **Strict pre-qualification rules**: 3 of 4 weeks >2% AND avg weekly >1.5%
- ✅ **6-signal market health monitoring** with real-time defensive scoring
- ✅ **Dynamic cash allocation** (0-30%) based on market regime detection
- ✅ **Two-tier position sizing** with user-configurable allocation weights (8-20% / 3-12%)
- ✅ **Integer-only percentages** for practical implementation
- ✅ **Deterministic mode** for consistent, reproducible analysis
- ✅ **Historical comparison tracking** with "Changes Since Last Analysis"
- ✅ **Daily reevaluation logic** with automatic position monitoring
- ✅ **Advanced technical analysis** (RSI, MACD, moving averages)
- ✅ **Risk management tools** with stop-loss suggestions

### 🛡️ Quality Stocks Features  
- ✅ **Fundamental quality screening**
- ✅ **Defensive sector analysis**
- ✅ **Long-term performance validation**
- ✅ **Low volatility focus**
- ✅ **Dividend aristocrat emphasis**
- ✅ **Weekly tracking system**

### 🎯 Options Trading Features
- ✅ **Multiple options strategies**: Bull Put Spreads, Bear Call Spreads, Iron Condors, Broken Wing Butterflies
- ✅ **Weekly income targeting** with automated trade evaluation
- ✅ **1-week price predictions** using technical indicators
- ✅ **Complete trade memory and P&L tracking**
- ✅ **Integration with OptionStrat** for trade visualization

## 📊 Market Health Monitoring

The tactical tracker automatically monitors market conditions and adjusts screening criteria when defensive mode is warranted (defensive score ≥ 70), while the quality tracker focuses on consistent fundamental strength regardless of market conditions.

## ✨ Multi-Strategy Investment Approach

The Portfolio Management Suite combines two complementary investment strategies:

### 🎯 Strategic Allocation Framework

#### Core-Satellite Approach
- **🛡️ Core Holdings (60-80%)**: Use Long-Term Quality Stocks for portfolio foundation
- **⚡ Satellite Positions (20-40%)**: Use Tactical Momentum for opportunistic allocation
- **📊 Dynamic Rebalancing**: Adjust emphasis based on market conditions

#### Market Regime Adaptation
- **🟢 Bull Markets**: Emphasize Tactical Momentum (higher satellite allocation)
- **🔴 Bear Markets**: Emphasize Quality Stocks (defensive core positioning)  
- **🟡 Uncertain Markets**: Balanced approach utilizing both strategies
- **🔄 Transition Periods**: Gradual shifts between offensive and defensive postures

### Market Regimes & Cash Allocation (Tactical Tracker)

- **🟢 AGGRESSIVE**: 0% cash - Full allocation to momentum stocks
- **🟠 CAUTIOUS**: 5% cash - Small defensive buffer
- **🟡 DEFENSIVE**: 15% cash - Moderate risk reduction  
- **🔴 HIGHLY_DEFENSIVE**: 30% cash - Significant capital preservation

### Quality Stock Characteristics (Quality Tracker)

- **🟢 Fundamental Quality**: Positive earnings, consistent dividends, ROE >10%
- **🛡️ Defensive Sectors**: Consumer Staples, Healthcare, Utilities, Quality Energy
- **📈 Long-term Performance**: 5-year outperformance with low volatility
- **💰 Income Generation**: Reliable dividend history and sustainable yields
- **🔒 Stability Focus**: Beta ≤ 1.2 for reduced portfolio volatility

## 🎯 Portfolio Allocation

The suite provides sophisticated allocation management across both strategies:

### ⚡ Tactical Allocation System
- **Two-tier position sizing**: Strong Buy (8-20%) vs Moderate Buy (3-12%)
- **Integer-only percentages** for practical implementation
- **Automatic scaling to 100%** with priority-based adjustments
- **Real-time market regime adaptation** with defensive cash allocation

### 🛡️ Quality Portfolio Construction  
- **Fundamental screening** with quality score ranking
- **Sector diversification** across defensive industries
- **Low-turnover approach** with quarterly rebalancing
- **Dividend yield optimization** for income generation

## 🛠️ Requirements

- **Python 3.8+** (tested with Python 3.8-3.11)
- **Internet connection** for real-time market data
- **Web browser** for the Streamlit interface

### Dependencies
All required packages are listed in `requirements.txt` for easy installation and consistent environments:

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `streamlit` - Web application framework
- `yfinance` - Market data retrieval
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `requests` - HTTP requests for web scraping
- `beautifulsoup4` - HTML parsing for market data

**Why requirements.txt?**
- **Consistent Environment**: Ensures all users have the same package versions
- **Easy Deployment**: Single command installs all dependencies
- **Version Control**: Tracks specific package versions for stability
- **Professional Standard**: Industry best practice for Python projects

## 🧪 Testing

The Portfolio Management Suite includes a comprehensive testing framework to ensure all features work correctly.

### Test Organization

All test files and testing utilities are organized in the `tests/` folder:

```
tests/
├── master_test_runner.py      # Main test orchestrator
├── test_option_pricing*.py    # Option pricing accuracy tests
├── test_optionstrat_url*.py   # URL generation tests  
├── test_ui*.py               # User interface tests
├── test_integration*.py      # End-to-end integration tests
├── test_core.py              # Core functionality tests
├── test_portfolio.py         # Portfolio management tests
├── debug_*.py                # Debug and verification scripts
└── run_*.py                  # Various test runners
```

### Running Tests

#### From Root Directory (Recommended)
```bash
# Quick test (core functionality only)
python run_tests.py --quick

# Full test suite (all tests including integration)
python run_tests.py --full

# Specific category
python run_tests.py --category pricing
python run_tests.py --category urls
python run_tests.py --category ui

# Verbose output
python run_tests.py --verbose
```

#### From Tests Directory
```bash
cd tests/

# Using master test runner directly
python master_test_runner.py
python master_test_runner.py --full
python master_test_runner.py --quick

# Shell script wrapper
./test.sh
./test.sh full
./test.sh verbose
```

### Test Categories

**Pricing Tests**: Verify option pricing accuracy against real market data
- Real-time price fetching from yfinance
- Strike selection algorithms
- Spread credit calculations

**URL Generation Tests**: Ensure OptionStrat integration works correctly
- Proper SELL/BUY indicators
- Decimal strike handling
- Strategy-specific URL formats

**UI Tests**: Validate user interface components
- Options tracker display
- Trade suggestion formatting
- Interactive features

**Integration Tests**: End-to-end workflow testing
- Complete trade suggestion pipeline
- Multi-ticker processing
- Error handling and recovery

## 📝 Project Status

✅ **VERSION 2.0 COMPLETE** - Multi-feature portfolio management suite fully implemented with 100% tactical tracker parity achieved.

### New in v2.0:
- 🎯 **Multi-feature architecture** with tactical and quality investment approaches
- 🛡️ **Long-term quality stocks tracker** with fundamental analysis
- 📊 **Unified interface** with feature selection and educational content
- 🔄 **Complementary strategies** designed to work together
- 📱 **Enhanced user experience** with comprehensive guidance
- 📈 **Historical comparison tracking** with "Changes Since Last Analysis" feature
- ✅ **100% Tactical Tracker Parity** - New modular tactical tracker produces identical results to original

### ✅ Verification Complete:
- **Auto-Discovery Mode**: Perfect parity (50 → 25 → top 10 identical rankings)
- **Manual Input Mode**: Full compatibility with original parameters
- **Market Health Analysis**: Identical 6-signal defensive scoring system
- **ETF Handling**: Correct market cap filtering at $5B threshold
- **Momentum Scoring**: Exact algorithm replication with identical results
- **Portfolio Allocation**: Same two-tier sizing and defensive cash allocation

### 🔧 Technical Achievement:
The new tactical tracker module maintains 100% backward compatibility with the original `streamlit_app.py` while providing the modular, extensible architecture of the Portfolio Management Suite v2.0. All edge cases, filtering logic, and scoring algorithms have been verified to produce identical results.

## 📁 Project Structure

### Essential Files (Main Directory)
- `main_app.py` - Multi-feature portfolio management suite launcher
- `tactical_tracker.py` - Modular tactical momentum tracker (with historical comparison)
- `streamlit_app.py` - Legacy tactical tracker (reference implementation)
- `requirements.txt` - Python package dependencies
- `run_suite.sh` / `run_suite_edge.sh` - Application launch scripts
- `README.md` - Main documentation

### Data Storage
- `data/portfolio_results.pkl` - Historical analysis data for comparison feature
- `data/options_trades.pkl` - Options trade history (auto-created)

### Supporting Directories
- `tests/` - Core test suite for validation and quality assurance
- `archived_files/` - Documentation, debug files, and project backups
- `.streamlit/` - Streamlit configuration (includes Edge browser compatibility)

For detailed project structure and organization, see `PROJECT_STATUS.md`.

---

*Last updated: July 5, 2025 - Source Code Reorganization and Comprehensive Documentation Update*
