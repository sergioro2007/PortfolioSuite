#!/bin/bash

# Portfolio Suite Test Runner
# Runs the comprehensive test suite

echo "🧪 Portfolio Management Suite - Test Suite"
echo "=========================================="

# Activate virtual environment
source .venv/bin/activate

echo "✅ Environment activated"
echo "🔍 Running comprehensive tests..."
echo ""

# Run the main test suite
python tests/run_tests.py

echo ""
echo "📊 Test run complete!"
echo "💡 For specific tests, use:"
echo "   python tests/test_options_tracker.py"
echo "   python tests/test_core.py"
echo "   python -m pytest tests/ -v"
