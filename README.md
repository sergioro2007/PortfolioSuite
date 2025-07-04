# Tactical Momentum Portfolio Tracker

A Streamlit-based application for automated tactical stock/ETF portfolio management using momentum and relative strength analysis.

## 🚀 Quick Start

### Option 1: Using the Launch Script (Recommended)
```bash
./run_app.sh
```

### Option 2: Manual Launch
```bash
# Activate virtual environment
source .venv/bin/activate

# Install core dependencies (if needed)
pip install streamlit yfinance pandas numpy

# Run the application
streamlit run streamlit_app.py
```

## 📱 Using the Application

1. **Configure Parameters**:
   - Set minimum RS score (20-100)
   - Set minimum weekly return target (0.25%-5.0%)
   - Adjust other screening criteria

2. **Run Screening**:
   - Click "Run Screening" to discover qualified tickers
   - Review results with detailed metrics and reasoning

3. **Monitor Portfolio**:
   - Track market health indicators
   - Get buy/sell/hold recommendations
   - Monitor real-time performance

## 🔧 Features

- ✅ **Automated ticker discovery** from major indices
- ✅ **User-configurable screening parameters**
- ✅ **Real-time market health monitoring**
- ✅ **Advanced technical analysis**
- ✅ **Interactive web interface**
- ✅ **Risk management tools**

## 📊 Market Health Monitoring

The app automatically monitors market conditions and adjusts screening criteria when defensive mode is warranted (defensive score ≥ 70).

## ✨ NEW: Defensive Cash Allocation

The app now includes an intelligent defensive cash allocation system that automatically adjusts portfolio allocation based on market conditions:

### Market Regimes & Cash Allocation

- **🟢 AGGRESSIVE**: 0% cash - Full allocation to momentum stocks
- **🟠 CAUTIOUS**: 5% cash - Small defensive buffer
- **🟡 DEFENSIVE**: 15% cash - Moderate risk reduction  
- **🔴 HIGHLY_DEFENSIVE**: 30% cash - Significant capital preservation

### How It Works

1. **Market Health Analysis**: The app continuously monitors VIX, market breadth, and other indicators
2. **Automatic Regime Detection**: Classifies current market conditions into defensive levels
3. **Dynamic Allocation**: Reduces stock exposure and increases cash in challenging markets
4. **User Control**: Toggle defensive cash allocation on/off via checkbox in portfolio section

### Benefits

- **Capital Preservation**: Automatically reduces risk in volatile markets
- **Tactical Flexibility**: Maintains cash for opportunities during market weakness  
- **Professional Approach**: Mimics institutional portfolio management practices
- **Transparent Logic**: Clear indicators show why cash is being held

### UI Features

- Real-time preview shows stock vs. cash allocation percentages
- Market regime indicator with color-coded status
- Detailed explanation of defensive positioning when active
- Summary metrics separated for stock allocation and defensive cash

## 🎯 Portfolio Allocation

The portfolio allocation section displays the current allocation across different assets, including stocks and cash. It is updated in real-time based on the latest market data and the app's defensive cash allocation rules.

## 🛠️ Requirements

- Python 3.7+
- Internet connection for real-time data
- Web browser for the Streamlit interface

## 📝 Project Status

✅ **COMPLETE** - All core functionality implemented and tested.

For detailed requirements and technical specifications, see `tactical_portfolio_app_requirements.md`.

---

*Last updated: July 1, 2025*
