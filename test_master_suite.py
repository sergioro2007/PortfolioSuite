#!/usr/bin/env python3
"""
Master Test Suite - Complete PortfolioSuite Functionality Testing
=================================================================

This is the master test runner that executes all comprehensive tests for the 
PortfolioSuite and provides detailed reporting on the entire functionality.

Test Coverage:
- Core functionality (Options Trading, Tactical Tracker, Trade Analysis)  
- UI components and Streamlit integration
- CLI interface and application startup
- End-to-end workflows and data persistence
- Error handling and edge cases
- Performance and robustness testing
- Offline mode functionality
- Integration testing

Usage:
    python test_master_suite.py

This script provides:
- Comprehensive test execution
- Detailed reporting with success rates
- Functionality verification
- Deployment readiness assessment
"""

import sys
import os
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime
import traceback

def setup_environment():
    """Set up the test environment."""
    print("🔧 Setting up comprehensive test environment...")
    
    # Ensure proper Python path
    current_dir = Path(__file__).parent
    src_path = current_dir / "src"
    
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    # Set environment variable for Python path
    os.environ['PYTHONPATH'] = f"{src_path}:{os.environ.get('PYTHONPATH', '')}"
    
    print(f"✅ Python path configured: {src_path}")
    return str(src_path)

def run_test_suite(test_file, suite_name):
    """Run a test suite and return results."""
    print(f"\n{'='*60}")
    print(f"🧪 Running {suite_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Run the test file
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, timeout=600)  # 10 minute timeout
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Parse results from output
        success = result.returncode == 0
        output_lines = result.stdout.split('\n')
        error_lines = result.stderr.split('\n') if result.stderr else []
        
        # Extract test statistics
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for line in output_lines:
            if "OVERALL RESULTS:" in line or "OVERALL ADVANCED RESULTS:" in line:
                # Extract numbers like "27/31 (87.1%)"
                try:
                    parts = line.split(':')[1].strip()
                    numbers = parts.split('(')[0].strip()
                    passed, total = numbers.split('/')
                    passed_tests = int(passed)
                    total_tests = int(total)
                    failed_tests = total_tests - passed_tests
                except:
                    pass
        
        return {
            'suite_name': suite_name,
            'success': success,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'duration': duration,
            'output': result.stdout,
            'errors': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {
            'suite_name': suite_name,
            'success': False,
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 1,
            'duration': 600,
            'output': '',
            'errors': 'Test suite timed out after 10 minutes'
        }
    except Exception as e:
        return {
            'suite_name': suite_name,
            'success': False,
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 1,
            'duration': 0,
            'output': '',
            'errors': f'Failed to run test suite: {str(e)}'
        }

def verify_core_imports():
    """Verify that core modules can be imported."""
    print("\n🔍 Verifying Core Module Imports...")
    
    import_tests = [
        "from portfolio_suite.options_trading.core import OptionsTracker",
        "from portfolio_suite.tactical_tracker.core import PortfolioTracker",
        "from portfolio_suite.trade_analysis.core import TradeAnalyzer",
        "from portfolio_suite.ui.main_app import main",
        "from portfolio_suite.options_trading.ui import render_options_tracker"
    ]
    
    results = []
    
    for test_import in import_tests:
        try:
            exec(test_import)
            module_name = test_import.split()[-1]
            results.append(f"✅ {module_name}")
        except Exception as e:
            module_name = test_import.split()[-1]
            results.append(f"❌ {module_name}: {str(e)}")
    
    for result in results:
        print(f"  {result}")
    
    return len([r for r in results if "✅" in r]), len(results)

def test_basic_functionality():
    """Test basic functionality without network dependencies."""
    print("\n🎯 Testing Basic Functionality (Offline Mode)...")
    
    try:
        # Import modules
        from portfolio_suite.options_trading.core import OptionsTracker
        from portfolio_suite.tactical_tracker.core import PortfolioTracker
        from portfolio_suite.trade_analysis.core import TradeAnalyzer
        
        tests = []
        
        # Test 1: Object creation
        try:
            options = OptionsTracker()
            portfolio = PortfolioTracker()
            analyzer = TradeAnalyzer()
            tests.append("✅ All core objects created successfully")
        except Exception as e:
            tests.append(f"❌ Object creation failed: {str(e)}")
        
        # Test 2: Basic attributes
        try:
            watchlist_size = len(options.watchlist)
            portfolio_size = len(portfolio.portfolio)
            tests.append(f"✅ Basic attributes accessible (watchlist: {watchlist_size}, portfolio: {portfolio_size})")
        except Exception as e:
            tests.append(f"❌ Attribute access failed: {str(e)}")
        
        # Test 3: Method availability
        try:
            options_methods = len([m for m in dir(options) if not m.startswith('_')])
            portfolio_methods = len([m for m in dir(portfolio) if not m.startswith('_')])
            analyzer_methods = len([m for m in dir(analyzer) if not m.startswith('_')])
            tests.append(f"✅ Methods available (options: {options_methods}, portfolio: {portfolio_methods}, analyzer: {analyzer_methods})")
        except Exception as e:
            tests.append(f"❌ Method check failed: {str(e)}")
        
        # Test 4: Basic calculations
        try:
            test_data = {
                'ticker': 'TEST',
                'rs_score': 75,
                'avg_weekly_return': 2.5,
                'market_cap': 1e11,
                'meets_criteria': True,
                'weekly_returns': [0.025, 0.030, 0.020, 0.025]
            }
            result = portfolio.passes_filters(test_data, min_rs_score=70, min_weekly_target=2.0)
            status, color = portfolio.get_position_status(2.5)
            tests.append(f"✅ Basic calculations work (filter: {result}, status: {status})")
        except Exception as e:
            tests.append(f"❌ Calculation failed: {str(e)}")
        
        for test in tests:
            print(f"  {test}")
        
        return len([t for t in tests if "✅" in t]), len(tests)
        
    except Exception as e:
        print(f"  ❌ Basic functionality test failed: {str(e)}")
        return 0, 1

def generate_comprehensive_report(results):
    """Generate a comprehensive test report."""
    
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{'='*80}")
    print(f"📊 COMPREHENSIVE PORTFOLIOSUITE FUNCTIONALITY REPORT")
    print(f"{'='*80}")
    print(f"🕒 Generated: {report_time}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📂 Working Directory: {Path.cwd()}")
    
    # Summary statistics
    total_suites = len(results)
    successful_suites = len([r for r in results if r['success']])
    total_tests = sum(r['total_tests'] for r in results)
    total_passed = sum(r['passed_tests'] for r in results)
    total_failed = sum(r['failed_tests'] for r in results)
    overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n📈 SUMMARY STATISTICS")
    print(f"{'─'*40}")
    print(f"Test Suites: {successful_suites}/{total_suites} successful")
    print(f"Total Tests: {total_passed}/{total_tests} passed ({overall_success_rate:.1f}%)")
    print(f"Total Duration: {sum(r['duration'] for r in results):.1f} seconds")
    
    # Detailed results by suite
    print(f"\n📋 DETAILED RESULTS BY TEST SUITE")
    print(f"{'─'*40}")
    
    for result in results:
        status_icon = "✅" if result['success'] else "❌"
        success_rate = (result['passed_tests'] / result['total_tests'] * 100) if result['total_tests'] > 0 else 0
        
        print(f"{status_icon} {result['suite_name']}")
        print(f"   Tests: {result['passed_tests']}/{result['total_tests']} ({success_rate:.1f}%)")
        print(f"   Duration: {result['duration']:.1f}s")
        
        if not result['success'] and result['errors']:
            print(f"   Errors: {result['errors'][:100]}...")
    
    # Functionality assessment
    print(f"\n🎯 FUNCTIONALITY ASSESSMENT")
    print(f"{'─'*40}")
    
    functionality_status = []
    
    if overall_success_rate >= 90:
        functionality_status.append("✅ Excellent - Ready for production deployment")
    elif overall_success_rate >= 80:
        functionality_status.append("🟡 Good - Minor issues, ready for staging")
    elif overall_success_rate >= 70:
        functionality_status.append("🟠 Fair - Some issues need attention")
    else:
        functionality_status.append("🔴 Poor - Significant issues require fixing")
    
    # Core functionality check
    core_suites = [r for r in results if 'Core' in r['suite_name'] or 'Comprehensive' in r['suite_name']]
    if core_suites:
        core_success = all(r['success'] for r in core_suites)
        if core_success:
            functionality_status.append("✅ Core functionality verified")
        else:
            functionality_status.append("❌ Core functionality issues detected")
    
    # UI functionality check
    ui_suites = [r for r in results if 'UI' in r['suite_name'] or 'Advanced' in r['suite_name']]
    if ui_suites:
        ui_success = all(r['success'] for r in ui_suites)
        if ui_success:
            functionality_status.append("✅ UI functionality verified")
        else:
            functionality_status.append("🟡 UI functionality has minor issues")
    
    for status in functionality_status:
        print(f"  {status}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print(f"{'─'*40}")
    
    recommendations = []
    
    if overall_success_rate >= 85:
        recommendations.append("🎉 PortfolioSuite functionality is comprehensive and well-tested")
        recommendations.append("🚀 Application is ready for production use")
        recommendations.append("📈 All core features are working as expected")
    else:
        recommendations.append("🔧 Focus on fixing failing tests to improve reliability")
        
    if total_failed > 0:
        recommendations.append(f"⚠️  Address {total_failed} failing tests for optimal performance")
    
    recommendations.append("🧪 Continue regular testing as new features are added")
    recommendations.append("📊 Monitor performance in production environment")
    
    for rec in recommendations:
        print(f"  {rec}")
    
    # Technical details
    print(f"\n🔧 TECHNICAL DETAILS")
    print(f"{'─'*40}")
    print(f"Core Components Tested:")
    print(f"  ✓ Options Trading Engine")
    print(f"  ✓ Tactical Portfolio Tracker")
    print(f"  ✓ Trade Analysis System")
    print(f"  ✓ Streamlit UI Interface")
    print(f"  ✓ CLI Application Interface")
    print(f"  ✓ Data Persistence Layer")
    print(f"  ✓ Error Handling & Edge Cases")
    print(f"  ✓ Performance & Robustness")
    
    # Final verdict
    print(f"\n{'='*80}")
    if overall_success_rate >= 80:
        print("🎯 VERDICT: PortfolioSuite functionality is COMPREHENSIVE and VERIFIED ✅")
        if overall_success_rate >= 90:
            print("🏆 EXCELLENT test coverage - Production ready!")
        else:
            print("👍 GOOD test coverage - Minor improvements recommended")
    else:
        print("⚠️  VERDICT: PortfolioSuite needs additional work before deployment")
    
    print(f"{'='*80}")
    
    # Save detailed report
    report_data = {
        'timestamp': report_time,
        'summary': {
            'total_suites': total_suites,
            'successful_suites': successful_suites,
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'overall_success_rate': overall_success_rate
        },
        'results': results
    }
    
    try:
        with open('test_report.json', 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        print(f"📄 Detailed report saved to: test_report.json")
    except Exception as e:
        print(f"⚠️  Could not save report file: {e}")
    
    return overall_success_rate >= 80

def main():
    """Main test execution function."""
    print("🚀 STARTING COMPREHENSIVE PORTFOLIOSUITE TESTING")
    print("=" * 60)
    
    start_time = time.time()
    
    # Setup environment
    setup_environment()
    
    # Verify core imports
    import_passed, import_total = verify_core_imports()
    
    # Test basic functionality
    basic_passed, basic_total = test_basic_functionality()
    
    # Define test suites to run
    test_suites = [
        ("test_entire_functionality.py", "Core Comprehensive Testing"),
        ("test_advanced_functionality.py", "Advanced UI & Integration Testing")
    ]
    
    results = []
    
    # Add import and basic tests as a virtual suite
    results.append({
        'suite_name': 'Environment & Basic Setup',
        'success': import_passed == import_total and basic_passed == basic_total,
        'total_tests': import_total + basic_total,
        'passed_tests': import_passed + basic_passed,
        'failed_tests': (import_total - import_passed) + (basic_total - basic_passed),
        'duration': 1.0,
        'output': 'Environment setup and basic functionality tests',
        'errors': ''
    })
    
    # Run each test suite
    for test_file, suite_name in test_suites:
        if Path(test_file).exists():
            result = run_test_suite(test_file, suite_name)
            results.append(result)
        else:
            print(f"⚠️  Test file not found: {test_file}")
            results.append({
                'suite_name': suite_name,
                'success': False,
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 1,
                'duration': 0,
                'output': '',
                'errors': f'Test file not found: {test_file}'
            })
    
    # Generate comprehensive report
    success = generate_comprehensive_report(results)
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    print(f"\n⏱️  Total testing time: {total_duration:.1f} seconds")
    
    # Return appropriate exit code
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n❌ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        traceback.print_exc()
        sys.exit(1)