# Portfolio Management Suite v2.0

A comprehensive multi-feature investment analysis platform with professional-grade portfolio management tools for both tactical and long-term investment strategies.

## 🎯 Features Overview

### ⚡ Tactical Momentum Portfolio Tracker
**Purpose**: Short-term tactical opportunities and momentum investing

- Automated momentum screening with strict tactical rules
- Real-time market health monitoring with 6-signal detection
- Intelligent defensive cash allocation (0-30% based on market regime)
- Two-tier position sizing (Strong Buy/Moderate Buy)
- Weekly return targets (0.5-3% configurable)
- Portfolio of up to 25 positions with high turnover

### 🛡️ Long-Term Quality Stocks Tracker  
**Purpose**: Conservative anchor portfolio for long-term investors

- Fundamental quality screening (ROE, profitability, dividends)
- Defensive sector focus (Consumer Staples, Healthcare, Utilities)
- Low volatility requirements (beta ≤ 1.2)
- 5-year performance validation
- Minimal weekly rotation
- Portfolio of 10-15 quality stocks for stability

## 🚀 Quick Start

### Installation
```bash
# Clone or download the project
cd Portfolio-Management-Suite

# Install required dependencies
pip install -r requirements.txt
```

### Option 1: Using the New Multi-Feature Launcher (Recommended)
```bash
./run_suite.sh
```

### Option 2: Manual Launch
```bash
# Run the multi-feature application
streamlit run main_app.py
```

### Option 3: Legacy Tactical Tracker Only
```bash
# For the original tactical momentum tracker only
./run_app.sh
# or
streamlit run streamlit_app.py
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

2. **Run Screening**:
   - Click "Run Screening" to discover qualified tickers
   - Review market health indicators and defensive signals
   - Examine results with detailed metrics and reasoning

3. **Monitor Portfolio**:
   - Track market health indicators and regime classification
   - Get buy/sell/hold recommendations with automatic cash allocation
   - Monitor real-time performance and allocation percentages
   - View historical comparison with "Changes Since Last Analysis"

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

## 🔧 Features

### ⚡ Tactical Momentum Features
- ✅ **Automated ticker discovery** from major indices
- ✅ **User-configurable screening parameters**
- ✅ **Real-time market health monitoring**
- ✅ **Advanced technical analysis**
- ✅ **Intelligent defensive cash allocation**
- ✅ **Historical comparison tracking** ("Changes Since Last Analysis")
- ✅ **Risk management tools**

### 🛡️ Quality Stocks Features  
- ✅ **Fundamental quality screening**
- ✅ **Defensive sector analysis**
- ✅ **Long-term performance validation**
- ✅ **Low volatility focus**
- ✅ **Dividend aristocrat emphasis**
- ✅ **Weekly tracking system**

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
All required packages are listed in `requirements.txt`:
- `streamlit` - Web application framework
- `yfinance` - Market data retrieval
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `requests` - HTTP requests for web scraping
- `beautifulsoup4` - HTML parsing for market data

## 🧪 Testing & Verification

The project includes comprehensive testing to ensure system reliability and parity:

### Test Suite Structure
- **Location**: `tests/` directory
- **Runner**: `python tests/run_tests.py` (basic unit tests)
- **System Verification**: `python tests/run_system_verification.py` (comprehensive)
- **Coverage**: 80%+ test coverage across all modules

### Test Categories
- **Unit Tests**: Core functionality testing (`test_*.py`)
- **Integration Tests**: End-to-end workflow testing
- **System Parity Tests**: Ensures new tracker matches original exactly
- **System Health Tests**: Performance, dependencies, error handling
- **Performance Tests**: Validates acceptable response times

### Running Tests

#### Basic Unit Tests
```bash
python tests/run_tests.py
```

#### Comprehensive System Verification
```bash
python tests/run_system_verification.py
```
This runs all test suites including:
- Core unit tests
- System parity verification
- System health checks
- Integration tests

#### UI Verification
```bash
python final_ui_test.py
```
Launches both applications for side-by-side comparison.

### System Verification Features
The system verification tests capture essential logic for ongoing validation:
- **Parity Testing**: Ensures identical results between original and new tactical trackers
- **Health Monitoring**: Verifies all dependencies, imports, and performance benchmarks
- **Error Handling**: Tests resilience to data issues and edge cases
- **End-to-End Flow**: Validates complete workflows from discovery to recommendations

These tests should be run regularly to ensure continued system health and parity.

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

For detailed requirements and technical specifications, see `tactical_portfolio_app_requirements.md`.

## 📁 Project Structure

### Essential Files (Main Directory)
- `main_app.py` - Multi-feature portfolio management suite launcher
- `tactical_tracker.py` - Modular tactical momentum tracker (with historical comparison)
- `streamlit_app.py` - Legacy tactical tracker (reference implementation)
- `portfolio_results.pkl` - Historical analysis data for comparison feature
- `requirements.txt` - Python package dependencies
- `run_suite.sh` / `run_suite_edge.sh` - Application launch scripts
- `README.md` - Main documentation
- `tactical_portfolio_app_requirements.md` - Technical specifications

### Supporting Directories
- `tests/` - Core test suite for validation and quality assurance
- `archived_files/` - Documentation, debug files, and project backups
- `.streamlit/` - Streamlit configuration (includes Edge browser compatibility)

For detailed project structure and organization, see `PROJECT_STATUS.md`.

---

*Last updated: December 27, 2024 - Historical Comparison Feature and Documentation Updates*
