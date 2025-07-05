# 📊 Portfolio Management Suite - Clean Project Structure

## 🎯 Current Status: **PRODUCTION READY**

Last cleaned: July 5, 2025

## 📁 Core Application Files

Last updated: July 5, 2025 *(Documentation updated December 27, 2024)*

### **Main Applications**
- `main_app.py` - Multi-feature Portfolio Management Suite (runs on port 8502)
- `streamlit_app.py` - Legacy standalone tactical tracker (runs on port 8501)
- `tactical_tracker.py` - Tactical momentum tracker module (✅ with historical comparison)

### **Additional Modules**
- `quality_tracker.py` - Long-term quality stocks tracker (placeholder)
- `options_analyzer.py` - Options analysis functionality

### **Launch Scripts**
- `run_suite.sh` - Launches multi-feature suite (recommended)
- `run_app.sh` - Launches legacy tactical tracker
- `run_suite_edge.sh` - Edge browser compatible launcher

### **Configuration**
- `.streamlit/config.toml` - Streamlit configuration with Edge compatibility
- `requirements.txt` - Python package dependencies
- `tactical_portfolio_app_requirements.md` - Project requirements documentation

### **Data**
- `portfolio_results.pkl` - Historical analysis results for comparison feature

## 🚀 How to Run

### **Recommended: Multi-Feature Suite**
```bash
./run_suite.sh
```
Opens at: http://localhost:8502

Features:
- ⚡ Tactical Momentum Tracker (with historical comparison)
- 🛡️ Long-Term Quality Stocks (in development)
- 📊 Feature selection interface

### **Alternative: Legacy Tracker**
```bash
./run_app.sh
```
Opens at: http://localhost:8501

## ✅ Implemented Features

### **Tactical Momentum Tracker**
- ✅ Auto-discovery mode
- ✅ Manual ticker input
- ✅ Market health monitoring
- ✅ Defensive cash allocation
- ✅ **Historical comparison ("Changes Since Last Analysis")**
- ✅ Portfolio recommendations
- ✅ Momentum scoring
- ✅ RS score filtering

### **Multi-Feature Suite**
- ✅ Feature selection interface
- ✅ Tactical tracker integration
- ✅ Edge browser compatibility
- ✅ Clean UI/UX

## 📁 Archived Files

Moved to `archived_files/` directory:
- `documentation/` - Project documentation and reports
- `backups/` - Backup files
- `test_scripts/` - Debug and test scripts

## 🧪 Testing

Essential test files kept in `tests/`:
- `run_tests.py` - Main test runner
- `test_*.py` - Core functionality tests
- `__init__.py` - Package initialization

## 🔧 Development Notes

- **Primary Development**: Focus on `main_app.py` and `tactical_tracker.py`
- **Browser Compatibility**: Chrome recommended, Edge supported via config
- **Data Persistence**: Results saved in `portfolio_results.pkl`
- **Historical Tracking**: Last 10 analyses automatically saved

## 📊 Next Steps

1. **Quality Tracker Implementation** - Complete long-term stocks module
2. **Feature Enhancement** - Add more analysis tools
3. **Performance Optimization** - Improve data fetching speed
4. **UI/UX Improvements** - Enhanced visualizations

---

**Status**: ✅ Clean, organized, and production-ready
**Last Update**: Portfolio Management Suite with historical comparison feature
