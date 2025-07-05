#!/usr/bin/env python3
"""
🧪 Master Test Runner for Portfolio Management Suite
===================================================

Unified test runner that executes all test categories from the tests folder.
This replaces the scattered test scripts with a centralized testing system.

Usage: 
  python master_test_runner.py                    # Run core tests
  python master_test_runner.py --full             # Run all tests
  python master_test_runner.py --quick            # Run quick tests only
  python master_test_runner.py --category pricing # Run specific category
  python master_test_runner.py --verbose          # Verbose output
"""

import os
import sys
import subprocess
import argparse
import time
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_script(script_name, description, verbose=False):
    """Run a single test script and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        print(f"⚠️  SKIPPING: {script_name} (file not found)")
        return None
    
    try:
        start_time = time.time()
        result = subprocess.run(
            f"python {script_path}", 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=os.path.dirname(__file__)
        )
        end_time = time.time()
        
        if result.returncode == 0:
            print(f"✅ PASSED ({end_time - start_time:.2f}s)")
            if verbose and result.stdout:
                print("Output:")
                print(result.stdout[:1000] + "..." if len(result.stdout) > 1000 else result.stdout)
            return True
        else:
            print(f"❌ FAILED ({end_time - start_time:.2f}s)")
            if result.stderr:
                print("Error output:")
                print(result.stderr[:1000] + "..." if len(result.stderr) > 1000 else result.stderr)
            if result.stdout:
                print("Standard output:")
                print(result.stdout[:1000] + "..." if len(result.stdout) > 1000 else result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Master test runner for Portfolio Management Suite')
    parser.add_argument('--full', action='store_true', help='Run all tests including slow ones')
    parser.add_argument('--quick', action='store_true', help='Run only quick tests')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    parser.add_argument('--category', choices=['pricing', 'urls', 'ui', 'integration'], help='Run specific test category')
    
    args = parser.parse_args()
    
    print("🚀 Portfolio Management Suite - Master Test Runner")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Define test categories
    test_categories = {
        'pricing': [
            ('test_option_pricing_accuracy.py', 'Option Pricing & Strike Generation'),
            ('test_real_prices.py', 'Real Market Price Fetching'),
            ('test_pricing_fix.py', 'Pricing Fix Verification'),
        ],
        'urls': [
            ('test_optionstrat_urls.py', 'OptionStrat URL Generation'),
            ('test_bear_call_url.py', 'Bear Call Spread URL Fix'),
            ('test_url_fix.py', 'URL Generation Fix'),
        ],
        'ui': [
            ('test_ui_display.py', 'UI Display Testing'),
            ('test_ui_improvements.py', 'UI Improvements'),
        ],
        'integration': [
            ('test_integration.py', 'Integration Testing'),
            ('test_integration_final.py', 'Final Integration Tests'),
            ('test_complete_suite.py', 'Complete Suite Testing'),
        ],
        'core': [
            ('test_core.py', 'Core Functionality'),
            ('test_config.py', 'Configuration Testing'),
            ('test_portfolio.py', 'Portfolio Management'),
        ],
        'suggestions': [
            ('test_suggestions_quick.py', 'Trade Suggestion Generation'),
            ('test_strikes.py', 'Strike Selection Logic'),
        ]
    }
    
    # Determine which tests to run
    if args.category:
        tests_to_run = test_categories.get(args.category, [])
        if not tests_to_run:
            print(f"❌ Unknown category: {args.category}")
            return 1
    elif args.quick:
        # Quick tests - essential functionality only
        tests_to_run = (test_categories['pricing'][:1] + 
                       test_categories['urls'][:1] + 
                       test_categories['suggestions'][:1])
    elif args.full:
        # All tests
        tests_to_run = []
        for category_tests in test_categories.values():
            tests_to_run.extend(category_tests)
    else:
        # Default: core tests
        tests_to_run = (test_categories['pricing'][:1] + 
                       test_categories['urls'][:1] + 
                       test_categories['ui'][:1])
    
    # Run the tests
    passed = 0
    failed = 0
    skipped = 0
    start_time = time.time()
    
    for script_name, description in tests_to_run:
        result = run_test_script(script_name, description, args.verbose)
        if result is True:
            passed += 1
        elif result is False:
            failed += 1
        else:
            skipped += 1
    
    total_time = time.time() - start_time
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {passed + failed + skipped}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Skipped: {skipped}")
    print(f"⏱️  Total Time: {total_time:.2f}s")
    print(f"🏁 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n💥 {failed} TEST(S) FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
