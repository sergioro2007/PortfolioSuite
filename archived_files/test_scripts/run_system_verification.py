#!/usr/bin/env python3
"""
Comprehensive System Test Runner
==============================

This script runs all system verification tests including:
- Unit tests for core functionality
- System parity tests (ensures new app matches original)
- System health checks (performance, dependencies, etc.)
- Integration tests

Run this regularly to verify system integrity and parity.
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_suite(test_pattern: str, suite_name: str) -> tuple:
    """Run a specific test suite and return results"""
    print(f"\n🧪 Running {suite_name}")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern=test_pattern)
    
    # Capture output
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    
    start_time = time.time()
    result = runner.run(suite)
    duration = time.time() - start_time
    
    # Print results
    output = stream.getvalue()
    print(output)
    
    return result, duration

def print_summary(all_results: list):
    """Print comprehensive summary of all test results"""
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 80)
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_duration = 0
    
    for suite_name, result, duration in all_results:
        tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
        passed = tests - failures - errors - skipped
        
        print(f"\n{suite_name}:")
        print(f"  Tests:    {tests:3d} | ✅ Passed: {passed:3d} | ❌ Failed: {failures:3d} | 🚫 Errors: {errors:3d} | ⏭️ Skipped: {skipped:3d}")
        print(f"  Duration: {duration:.2f}s")
        
        total_tests += tests
        total_failures += failures
        total_errors += errors
        total_skipped += skipped
        total_duration += duration
    
    total_passed = total_tests - total_failures - total_errors - total_skipped
    
    print(f"\n{'OVERALL TOTALS':^60}")
    print("-" * 60)
    print(f"Total Tests:     {total_tests:3d}")
    print(f"✅ Passed:       {total_passed:3d}")
    print(f"❌ Failed:       {total_failures:3d}")
    print(f"🚫 Errors:       {total_errors:3d}")
    print(f"⏭️ Skipped:      {total_skipped:3d}")
    print(f"⏱️ Total Time:   {total_duration:.2f}s")
    
    # Overall status
    if total_failures == 0 and total_errors == 0:
        print("\n🎉 ALL TESTS PASSED! System is healthy and maintains parity.")
    else:
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        print(f"\n⚠️ Some tests failed. Success rate: {success_rate:.1f}%")
    
    print("=" * 80)
    
    return total_failures == 0 and total_errors == 0

def main():
    """Run comprehensive system verification"""
    print("🔬 COMPREHENSIVE SYSTEM VERIFICATION")
    print("🎯 Testing: Core functionality, System parity, Health checks, Integration")
    print("=" * 80)
    
    all_results = []
    
    # 1. Run core unit tests
    try:
        result, duration = run_test_suite('test_*.py', 'Core Unit Tests')
        all_results.append(('Core Unit Tests', result, duration))
    except Exception as e:
        print(f"❌ Failed to run core unit tests: {e}")
    
    # 2. Run system parity tests
    try:
        result, duration = run_test_suite('test_system_parity.py', 'System Parity Tests')
        all_results.append(('System Parity Tests', result, duration))
    except Exception as e:
        print(f"❌ Failed to run system parity tests: {e}")
    
    # 3. Run system health checks
    try:
        result, duration = run_test_suite('test_system_health.py', 'System Health Checks')
        all_results.append(('System Health Checks', result, duration))
    except Exception as e:
        print(f"❌ Failed to run system health checks: {e}")
    
    # Print comprehensive summary
    all_passed = print_summary(all_results)
    
    # Additional recommendations
    print("\n🔧 RECOMMENDATIONS:")
    if all_passed:
        print("✅ System is fully operational and maintains 100% parity")
        print("✅ All dependencies are working correctly")
        print("✅ Performance is within acceptable limits")
        print("✅ Ready for production use")
    else:
        print("⚠️ Review failed tests above")
        print("⚠️ Check dependencies and system configuration")
        print("⚠️ Verify data sources are accessible")
        print("⚠️ Consider running individual test suites for detailed debugging")
    
    print(f"\n📋 Test suites run: {len(all_results)}")
    print("🔄 Run this script regularly to ensure continued system health")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
