"""
Test runner script to execute all unit tests and generate coverage report
Run this script to test the entire application with coverage analysis
"""

import unittest
import sys
import os
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():
    """Run all test suites and generate a summary report"""
    
    print("🧪 Running Tactical Portfolio Tracker Unit Tests")
    print("=" * 60)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Capture test output
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    # Print results
    output = stream.getvalue()
    print(output)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    passed = total_tests - failures - errors - skipped
    
    print(f"Total Tests:     {total_tests}")
    print(f"✅ Passed:       {passed}")
    print(f"❌ Failed:       {failures}")
    print(f"🚫 Errors:       {errors}")
    print(f"⏭️ Skipped:      {skipped}")
    
    if failures == 0 and errors == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️ {failures + errors} test(s) need attention")
    
    print("\n💡 TIP: Run 'python run_system_verification.py' for comprehensive system checks")
    
    return failures == 0 and errors == 0

def run_specific_test_suite(suite_name):
    """Run a specific test suite"""
    
    suite_map = {
        'core': 'test_core.py',
        'analysis': 'test_analysis.py', 
        'portfolio': 'test_portfolio.py',
        'integration': 'test_integration.py'
    }
    
    if suite_name not in suite_map:
        print(f"❌ Unknown test suite: {suite_name}")
        print(f"Available suites: {', '.join(suite_map.keys())}")
        return 1
        
    print(f"🧪 Running {suite_name.title()} Test Suite")
    print("=" * 40)
    
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern=suite_map[suite_name])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test suite
        exit_code = run_specific_test_suite(sys.argv[1])
    else:
        # Run all tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
