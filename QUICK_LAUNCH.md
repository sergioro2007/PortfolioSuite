# Quick Launch Guide

## Options Trading Tracker

### Method 1: Using the main application (RECOMMENDED)

```bash
cd /Users/soliv112/PersonalProjects/PortfolioSuite
source venv/bin/activate
python -m streamlit run src/portfolio_suite/__main__.py --server.port=8506
```

Then visit: http://localhost:8506

### Method 2: Direct Options Tracker Launch

```bash
cd /Users/soliv112/PersonalProjects/PortfolioSuite
source venv/bin/activate
streamlit run run_options_simple.py --server.port=8507
```

### Method 3: Alternative Direct Launch

```bash
cd /Users/soliv112/PersonalProjects/PortfolioSuite
source venv/bin/activate
python -c "
import sys, os
sys.path.insert(0, 'src')
from portfolio_suite.options_trading.ui import render_options_tracker
render_options_tracker()
"
```

## Current Status

✅ All field mapping issues resolved (target_mid → target_price, etc.)  
✅ Application running successfully on port 8506  
✅ Market Analysis section working without crashes  
✅ Trade suggestions functionality operational

## Fixed Issues

- ✅ KeyError: 'target_mid' resolved
- ✅ Field mapping consistency between core and UI
- ✅ Python module import paths fixed
- ✅ Streamlit application launching properly
