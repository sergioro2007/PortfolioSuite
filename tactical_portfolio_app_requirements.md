# Tactical Momentum Portfolio Tracker

This Streamlit application automatically identifies and manages a tactical stock/ETF portfolio based on short-term momentum, relative strength, and weekly performance rules. The app features sophisticated risk management with **automatic defensive cash allocation** that adapts to changing market conditions.

---

## 🎯 Goals

- Achieve **0.5-3% weekly returns** per position (user-configurable).
- Maintain a **portfolio of up to 25 U.S.-listed stocks/ETFs** with a market cap above $5B.
- **Automatically adjust cash allocation** based on market regime (0-30% defensive cash).
- Rotate out of underperforming stocks weekly or daily if needed.
- React defensively when market conditions deteriorate with intelligent cash preservation.

---

## ✅ Selection Criteria

1. **Liquidity & Market Cap**
   - Stocks/ETFs must have market cap > $5B
   - High average daily volume

2. **Momentum & Technicals**
   - User-configurable RS score threshold (default: 30+ for standard screening)
   - Favorable technical setups: breakouts, cup-with-handle, strong trend
   - Comprehensive technical analysis including RSI, MACD, moving averages

3. **Performance Requirements**
   - User-configurable minimum weekly return target (default: 1.5%)
   - Must meet tactical criteria: **at least 3 of last 4 weeks > 2%** gain
   - **Average weekly return > 1.5%** (strictly enforced before scoring)
   - Automatic exit if position underperforms or violates risk management rules

4. **Parameter Enforcement**
   - ✅ User-defined parameters are strictly enforced
   - ✅ Tactical momentum rules applied before any scoring
   - ✅ Transparent filtering with detailed qualification reasons

---

## 🤖 Automated Ticker Discovery & Screening

- The application **automatically discovers qualifying tickers** from S&P 500, NASDAQ 100, and other major indices
- **Multi-stage screening process**:
  1. Basic filters: Market cap > $5B, sufficient volume
  2. User-defined criteria: RS score and weekly return thresholds
  3. Technical analysis: RSI, MACD, moving average trends
  4. Risk management: Volatility and drawdown checks
- **Real-time data integration** using yfinance API
- **Intelligent result limiting**: Up to 25 tickers in aggressive mode, 15 in defensive mode
- **Transparent qualification**: Each ticker comes with detailed reasoning for inclusion/exclusion

## 🛡️ NEW: Intelligent Defensive Cash Allocation

### Automatic Market Regime Detection
The app continuously monitors **6 real-time market signals** and automatically adjusts portfolio allocation:

**Market Health Signals Monitored:**
1. **VIX > 30** (fear index threshold)
2. **VIX Rising Trend** (increasing market fear)
3. **SPY below 20-day MA** (market weakness)
4. **Market Breadth < 50%** (few stocks advancing)
5. **High Volatility > 2.5%** (excessive daily price swings)
6. **Negative Momentum** (10-day < 30-day moving averages)

### Dynamic Cash Allocation by Market Regime

- **🟢 AGGRESSIVE** (0-1 signals): **0% cash** - Full stock allocation
- **🟠 CAUTIOUS** (2 signals): **5% cash** - Small defensive buffer  
- **🟡 DEFENSIVE** (3 signals): **15% cash** - Moderate risk reduction
- **🔴 HIGHLY_DEFENSIVE** (4+ signals): **30% cash** - Significant capital preservation

### User Control & Transparency
- **"Allow Defensive Cash" checkbox** - Users can disable automatic cash allocation
- **Real-time preview** - Shows exact stock vs. cash allocation percentages
- **Market regime indicator** - Color-coded status with explanations
- **Educational UI** - Clear explanations of why defensive positioning is active

---

## 🎯 Enhanced Portfolio Allocation System

### Two-Tier Position Sizing
- **Strong Buy positions**: 8-20% allocation (user adjustable)
- **Moderate Buy positions**: 3-12% allocation (user adjustable)
- **Automatic scaling**: Ensures total allocation = 100% using integer percentages

### Qualification Criteria
- **Strong Buys**: Momentum score > 15 AND weekly return > 2.0%
- **Moderate Buys**: Momentum score > 10 (excluding strong buys)
- **Watch List**: Promising stocks that don't quite qualify

### Real-Time Allocation Management
- **Integer-only percentages** for practical implementation
- **Automatic adjustment** to exactly 100% total allocation
- **Priority weighting** (strong buys get allocation adjustments first)
- **Live feedback** showing allocation previews and adjustments

---

## 🔁 Daily Reevaluation Logic

Each day, check:

- Ticker's % change from 10AM price
- Flag if:
  - Drop > 3% → Review/Exit
  - Drop > 1.5% → Watch closely
  - Gain > 2% → Strong Momentum

---

## 🛠️ App Features & Functionality

### 🆕 LATEST FEATURES ✅ IMPLEMENTED

#### Defensive Cash Allocation System
- **Automatic market regime detection** with 6-signal monitoring system
- **Dynamic cash allocation** (0-30%) based on market conditions
- **User control toggle** to enable/disable defensive positioning
- **Real-time allocation preview** with market regime indicators
- **Educational UI** explaining defensive logic and market conditions

#### Professional Portfolio Management
- **Two-tier allocation system** (Strong Buy 8-20%, Moderate Buy 3-12%)
- **Integer-only percentages** for practical implementation
- **Automatic scaling to 100%** with priority-based adjustments
- **Live allocation feedback** with adjustment notifications
- **Comprehensive position metrics** (momentum scores, weekly returns)

#### Enhanced UI/UX
- **Real-time percentage calculations** with proper formatting
- **Market regime indicators** with color-coded status
- **Allocation summary metrics** (separated stock/cash allocations)
- **Educational tooltips** explaining defensive positioning
- **Clean, professional interface** suitable for institutional use

### Core Features ✅ IMPLEMENTED

#### 1. Advanced Screening Engine
- **Strict tactical momentum enforcement**: 3 of 4 weeks > 2% gain required
- **Pre-scoring qualification**: Average weekly return > 1.5% mandatory
- **User-configurable parameters**: RS score (30-100), weekly targets (0.5-5.0%)
- **Deterministic results**: Consistent ticker discovery across runs
- **Robust error handling**: Graceful handling of data issues

#### 2. Technical Analysis Suite
- **Multi-timeframe momentum analysis** with weekly return calculations
- **RSI, MACD, Bollinger Bands** integration for technical validation
- **Moving average trend confirmation** (10, 20, 50-day MAs)
- **Volume and liquidity validation** for institutional-quality picks
- **Relative strength scoring** against market benchmarks

#### 3. Risk Management Tools
- **Position tracking** with real-time P&L calculation
- **Stop-loss suggestions** based on volatility and technical levels
- **Diversification analysis** across sectors and market caps
- **Volatility monitoring** with automatic risk adjustment
- **Cash preservation** during adverse market conditions

#### 4. Market Intelligence Dashboard
- **Live market health scoring** with 6-signal monitoring
- **Sector rotation insights** using ETF performance analysis
- **Volatility regime detection** with automatic defensive triggers
- **Economic indicator integration** (VIX, breadth, momentum)
- **Historical comparison** with previous portfolio analyses

#### 5. Production-Ready Interface
- **Streamlit web application** with professional styling
- **Interactive parameter controls** with real-time validation
- **Comprehensive data tables** with proper percentage formatting
- **Export capabilities** for portfolio results and analysis
- **Mobile-responsive design** for multi-device access

### Recent Major Updates ✅ COMPLETED

#### V2.0 - Defensive Cash Allocation (2025-07-03)
- **🛡️ Intelligent defensive cash allocation** (0-30% based on market regime)
- **🎯 Two-tier position sizing** with user-adjustable allocation weights
- **📊 Real-time allocation preview** with market regime indicators
- **🔧 Integer-only percentages** for clean, practical allocations
- **📱 Enhanced UI/UX** with educational defensive positioning explanations

#### V1.5 - Portfolio Management Overhaul (2025-07-02)
- **🎯 Fixed allocation logic** to ensure exactly 100% allocation
- **📈 Corrected percentage displays** in all UI tables and metrics
- **🔄 Deterministic ticker discovery** (eliminated random ticker swaps)
- **✅ Fixed yfinance parameter issues** (removed unsupported arguments)
- **🔇 Suppressed verbose logging** for cleaner user experience

#### V1.4 - Tactical Rules Enhancement (2025-07-01)
- **⚡ Strict momentum enforcement**: 3 of 4 weeks > 2% gain required
- **📏 Pre-scoring qualification**: Average weekly return > 1.5% mandatory
- **🎯 Enhanced filtering logic** to prioritize high-confidence trades
- **📊 Improved momentum scoring** algorithm for better stock selection
- **🧪 Comprehensive test suite** (60 tests, ~80% coverage)

---

## 📆 Current Application Workflow

### 🌅 Daily Operation

#### 1. Market Health Assessment
- **6-signal monitoring system**: VIX, breadth, volatility, momentum, SPY MAs
- **Automatic regime classification**: AGGRESSIVE → CAUTIOUS → DEFENSIVE → HIGHLY_DEFENSIVE
- **Real-time defensive score calculation** (0-100 scale)
- **Market regime indicators** displayed prominently in UI

#### 2. Intelligent Portfolio Allocation
- **Dynamic cash allocation**: 0-30% based on market regime
- **Two-tier position sizing**: Strong Buys (8-20%) vs Moderate Buys (3-12%)
- **User-controlled allocation weights** with real-time preview
- **Automatic scaling to 100%** using integer percentages
- **Priority-based allocation adjustments** (strong buys prioritized)

#### 3. Advanced Ticker Screening
- **Pre-qualification enforcement**: 3 of 4 weeks > 2% AND avg weekly > 1.5%
- **Automated discovery**: 500+ tickers from major indices and ETFs
- **Multi-stage filtering**: Market cap → Tactical rules → Technical analysis
- **Momentum scoring**: Only qualified tickers receive scores
- **Deterministic results**: Consistent screening across multiple runs

#### 4. Real-time Portfolio Management
- **Live position tracking** with momentum scores and weekly returns
- **Performance monitoring** against tactical rules
- **Risk management alerts** for underperforming positions
- **Sector diversification analysis** and allocation recommendations

#### 5. Professional Dashboard Interface
- **Market regime dashboard** with real-time health indicators
- **Interactive allocation controls** with immediate feedback
- **Comprehensive portfolio tables** with proper percentage formatting
- **Educational explanations** for defensive positioning decisions
- **Historical comparison** with previous analysis results

### 🎯 Key Workflow Benefits

- ✅ **Automatic risk management**: Cash allocation adapts to market conditions
- ✅ **Professional-grade allocation**: Integer percentages, exact 100% allocation
- ✅ **Institutional quality**: Mimics professional portfolio management practices
- ✅ **User control**: Full transparency with ability to override defensive features
- ✅ **Educational value**: Clear explanations of all decisions and market conditions

---

## 🧰 Technology Stack

### Core Libraries & APIs
- **Data & Analysis**: `yfinance` (market data), `pandas` (data manipulation), `numpy` (calculations)
- **Web Interface**: `streamlit` (fully implemented with professional styling)
- **Visualization**: Built-in Streamlit components with custom formatting
- **Technical Analysis**: Custom momentum calculations, RSI, MACD, moving averages

### Application Architecture
- **Production-ready single file**: `streamlit_app.py` (1,500+ lines, fully documented)
- **Object-oriented design**: `PortfolioTracker` class with modular methods
- **Real-time data integration**: Live market data via yfinance API
- **Responsive UI**: Streamlit-based interface optimized for desktop and mobile
- **Comprehensive testing**: 60+ unit tests with ~80% code coverage

### Performance & Reliability
- **Robust error handling**: Graceful degradation when market data unavailable
- **Efficient data processing**: Optimized for handling 500+ ticker screening
- **Deterministic results**: Consistent output across multiple runs
- **Production logging**: Suppressed verbose output, clean user experience
- **Scalable architecture**: Handles large datasets without performance issues

### Development & Testing
- **Test-driven development**: Comprehensive test suite with pytest
- **Continuous validation**: Automated testing of all major features
- **Documentation**: Inline comments and comprehensive README
- **Version control ready**: Clean, professional codebase structure
- **Easy deployment**: Single command launch (`streamlit run streamlit_app.py`)

---

## 🚀 Quick Start Guide

### Installation & Setup
```bash
# Install required packages
pip install streamlit yfinance pandas numpy requests beautifulsoup4

# Launch the application
streamlit run streamlit_app.py
```

### Using the Application

#### 1. Configure Screening Parameters
- **Portfolio Size**: Set number of positions (1-25)
- **Min RS Score**: Relative strength threshold (30-100)
- **Min Weekly Target**: Required weekly return (0.5%-5.0%)

#### 2. Set Allocation Preferences
- **Strong Buy Weight**: Allocation % for top momentum stocks (8-20%)
- **Moderate Buy Weight**: Allocation % for secondary picks (3-12%)
- **Allow Defensive Cash**: Enable/disable automatic cash allocation

#### 3. Run Analysis
- Click **"🔄 Analyze Portfolio"** to start screening
- Review market health indicators and regime classification
- Examine qualified stock recommendations with detailed metrics

#### 4. Manage Portfolio
- Review suggested allocation percentages
- Monitor position recommendations (Strong Buy/Moderate Buy/Watch List)
- Track portfolio completion and cash allocation status

---

## 📊 Testing & Quality Assurance

### Comprehensive Test Suite
- **60 total tests** covering all major functionality
- **~80% code coverage** with critical path validation
- **9 defensive allocation tests** specifically for new cash management features
- **Integration tests** for end-to-end workflow validation
- **Edge case handling** for data failures and market anomalies

### Quality Standards
- **Production-ready code**: Professional documentation and error handling
- **User-friendly interface**: Intuitive controls with real-time feedback
- **Reliable data processing**: Robust handling of market data inconsistencies
- **Performance optimization**: Efficient screening of large ticker universes
- **Scalable architecture**: Handles varying market conditions and user preferences

---

## 📋 Project Status: PRODUCTION COMPLETE ✅

The Tactical Momentum Portfolio Tracker is a **fully functional, institutional-quality application** with advanced risk management capabilities:

### 🎯 Core Achievements
- ✅ **Advanced momentum screening** with strict tactical rules enforcement
- ✅ **Intelligent defensive cash allocation** (0-30% based on market regime)
- ✅ **Professional portfolio management** with two-tier position sizing
- ✅ **Real-time market health monitoring** with 6-signal detection system
- ✅ **Production-ready Streamlit interface** with educational UI components
- ✅ **Comprehensive testing suite** (60 tests, ~80% coverage)

### 🆕 Latest V2.0 Features
- **🛡️ Automatic defensive cash allocation** that adapts to market conditions
- **📊 Two-tier allocation system** (Strong Buy/Moderate Buy with user controls)
- **🎯 Integer-only percentages** for practical implementation
- **📱 Enhanced UI/UX** with real-time previews and market regime indicators
- **🧠 Educational tooltips** explaining defensive positioning logic

### 🔧 Technical Excellence
- **Deterministic results**: Consistent ticker discovery and screening
- **Robust error handling**: Graceful degradation with market data issues
- **Performance optimized**: Efficiently handles 500+ ticker screening
- **Professional codebase**: 1,500+ lines with comprehensive documentation
- **Test-driven development**: Extensive validation of all features

### 🏆 Production Quality Standards
- **Institutional-grade risk management**: Automatic cash allocation during market stress
- **Professional UI/UX**: Clean, educational interface suitable for investment professionals
- **Reliable data processing**: Handles real-world market data inconsistencies
- **User-friendly controls**: Intuitive parameter adjustment with real-time feedback
- **Scalable architecture**: Adapts to varying market conditions and user preferences

### 📈 Business Value Delivered
- **Risk-adjusted returns**: Automatic cash preservation during market downturns
- **Professional allocation**: Integer percentages for practical portfolio implementation
- **Educational value**: Clear explanations of market conditions and defensive positioning
- **Time efficiency**: Automated screening and allocation recommendations
- **Institutional quality**: Suitable for professional investment management use

---

## 🎉 Ready for Production Use

The application successfully delivers:

1. **🎯 Sophisticated momentum screening** with tactical rules enforcement
2. **🛡️ Intelligent risk management** through dynamic cash allocation
3. **📊 Professional portfolio allocation** with user-customizable parameters
4. **📱 Production-ready interface** with comprehensive user guidance
5. **🧪 Thoroughly tested codebase** with extensive quality assurance

**Perfect for**: Investment professionals, sophisticated individual investors, portfolio managers, and anyone seeking institutional-quality momentum investing tools with intelligent risk management.

---

_Last updated: 2025-07-03 - V2.0 Production Release with Defensive Cash Allocation_
