#!/bin/bash
# 🧪 Quick Test Runner for Portfolio Management Suite
# 
# Usage:
#   ./test.sh           # Run quick tests only
#   ./test.sh full      # Run all tests including integration
#   ./test.sh verbose   # Run quick tests with verbose output
#   ./test.sh module options_tracker  # Run specific module

echo "🧪 Portfolio Management Suite Test Runner"
echo "=========================================="

case "$1" in
    "full")
        echo "Running all tests (including integration)..."
        python run_all_tests.py --verbose
        ;;
    "verbose" | "-v")
        echo "Running quick tests with verbose output..."
        python run_all_tests.py --quick --verbose
        ;;
    "module" | "-m")
        if [ -z "$2" ]; then
            echo "❌ Module name required. Available: options_tracker, strikes, real_prices, option_pricing, ui_improvements"
            exit 1
        fi
        echo "Running tests for module: $2"
        python run_all_tests.py --module "$2" --verbose
        ;;
    "help" | "-h" | "--help")
        echo "Usage:"
        echo "  ./test.sh           # Run quick tests only"
        echo "  ./test.sh full      # Run all tests including integration"
        echo "  ./test.sh verbose   # Run quick tests with verbose output"
        echo "  ./test.sh module MODULE_NAME  # Run specific module"
        echo ""
        echo "Available modules: options_tracker, strikes, real_prices, option_pricing, ui_improvements"
        exit 0
        ;;
    *)
        echo "Running quick tests..."
        python run_all_tests.py --quick
        ;;
esac

echo ""
echo "🏁 Test run complete!"
