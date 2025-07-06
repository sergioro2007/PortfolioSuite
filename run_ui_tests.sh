#!/bin/bash

# Run all tests related to options trading UI and trade suggestion workflow
echo "================================================"
echo "🧪 Running Options Trading UI and Suggestion Tests"
echo "================================================"

# Set up Python path
export PYTHONPATH=$(pwd)

# Run the core tests
echo "🧪 Running trade suggestion workflow tests..."
python -m unittest tests/test_trade_suggestion_workflow.py

echo "🧪 Running UI trade display tests..."
python -m unittest tests/test_ui_trade_display.py

echo "🧪 Running trade suggestion filter tests..."
python -m unittest tests/test_profit_target_filter.py

echo "🧪 Running dynamic watchlist tests..."
python -m unittest tests/test_dynamic_watchlist.py

echo "🧪 Running OptionStrat URL generation tests..."
python -m unittest tests/test_optionstrat_urls.py

echo "✅ All tests complete!"
