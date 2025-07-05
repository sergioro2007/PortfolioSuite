#!/usr/bin/env python3
"""
🧪 Core Test Runner for Portfolio Management Suite
=================================================

Runs essential tests for the Portfolio Management Suite:
- Option pricing accuracy
- OptionStrat URL generation
- UI display testing

Usage: python run_core_tests.py [--verbose]
"""

import os
import sys

# Add parent directory to path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import subprocess
import argparse
import time
from datetime import datetime

def run_test(test_file, description, verbose=False):
    """Run a single test file and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    if not os.path.exists(test_file):
        print(f"⚠️  SKIPPING: {test_file} (file not found)")
        return None
    
    try:
        start_time = time.time()
        result = subprocess.run(
            f"python {test_file}", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        end_time = time.time()
        
        if result.returncode == 0:
            print(f"✅ PASSED ({end_time - start_time:.2f}s)")
            if verbose and result.stdout:
                print("Output:")
                print(result.stdout)
            return True
        else:
            print(f"❌ FAILED ({end_time - start_time:.2f}s)")
            if result.stderr:
                print("Error output:")
                print(result.stderr)
            if result.stdout:
                print("Standard output:")
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run core test suite')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()
    
    print("🚀 Portfolio Management Suite - Core Test Runner")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Core test files (only existing ones)
    core_tests = [
        ("tests/test_option_pricing_accuracy.py", "Option Pricing & Strike Generation"),
        ("tests/test_optionstrat_urls.py", "OptionStrat URL Generation"),
        ("tests/test_ui_display.py", "UI Display Testing"),
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    total_time = 0
    
    start_time = time.time()
    
    for test_file, description in core_tests:
        result = run_test(test_file, description, args.verbose)
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
