#!/usr/bin/env python3
"""
🧪 Comprehensive Test Runner for Portfolio Management Suite
==========================================================

Runs all tests for the Portfolio Management Suite including:
- Options Tracker functionality
- Strike generation
- Real price fetching
- Trade suggestion logic
- UI components
- Integration tests

Usage: python run_all_tests.py [--verbose] [--module MODULE_NAME]
"""

import os
import sys

# Add parent directory to path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import subprocess
import argparse
import time
from datetime import datetime

def run_command(command, description, verbose=False):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    if verbose:
        print(f"Command: {command}")
    
    try:
        start_time = time.time()
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        end_time = time.time()
        
        if result.returncode == 0:
            print(f"✅ PASSED ({end_time - start_time:.2f}s)")
            if verbose and result.stdout:
                print("STDOUT:")
                print(result.stdout)
            return True
        else:
            print(f"❌ FAILED ({end_time - start_time:.2f}s)")
            print("STDERR:")
            print(result.stderr)
            if result.stdout:
                print("STDOUT:")
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run all tests for Portfolio Management Suite")
    parser.add_argument('--verbose', '-v', action='store_true', help="Verbose output")
    parser.add_argument('--module', '-m', help="Run specific test module only")
    parser.add_argument('--quick', '-q', action='store_true', help="Run quick tests only (skip integration)")
    
    args = parser.parse_args()
    
    print("🚀 Portfolio Management Suite - Comprehensive Test Runner")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Define test modules
    test_modules = {
        'options_tracker': {
            'file': 'test_options_tracker.py',
            'description': 'Testing Options Tracker Core Functionality',
            'quick': True
        },
        'strikes': {
            'file': 'test_strikes.py', 
            'description': 'Testing Strike Generation Logic',
            'quick': True
        },
        'real_prices': {
            'file': 'test_real_prices.py',
            'description': 'Testing Real Option Price Fetching',
            'quick': True
        },
        'option_pricing': {
            'file': 'test_option_pricing.py',
            'description': 'Testing Option Pricing Models',
            'quick': True
        },
        'ui_improvements': {
            'file': 'test_ui_improvements.py',
            'description': 'Testing UI Improvements (Sorting & URLs)',
            'quick': True
        },
        'portfolio_tests': {
            'file': 'tests/run_tests.py',
            'description': 'Testing Portfolio Management Core',
            'quick': False
        }
    }
    
    # Filter tests based on arguments
    if args.module:
        if args.module not in test_modules:
            print(f"❌ Unknown module: {args.module}")
            print(f"Available modules: {', '.join(test_modules.keys())}")
            return 1
        test_modules = {args.module: test_modules[args.module]}
    
    if args.quick:
        test_modules = {k: v for k, v in test_modules.items() if v['quick']}
    
    # Run tests
    passed = 0
    failed = 0
    total_start_time = time.time()
    
    for module_name, module_info in test_modules.items():
        test_file = module_info['file']
        description = module_info['description']
        
        # Check if test file exists
        if not os.path.exists(test_file):
            print(f"\n⚠️  SKIPPING: {test_file} (file not found)")
            continue
        
        # Run the test
        success = run_command(
            f"python {test_file}",
            description,
            args.verbose
        )
        
        if success:
            passed += 1
        else:
            failed += 1
    
    # Summary
    total_time = time.time() - total_start_time
    total_tests = passed + failed
    
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
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
