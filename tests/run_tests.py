#!/usr/bin/env python3
"""
Comprehensive test runner for Portfolio Management Suite.
Includes environment verification and end-to-end testing.
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run all tests with proper configuration."""
    project_root = Path(__file__).parent.parent
    
    # Run pytest with appropriate options
    cmd = [
        sys.executable, "-m", "pytest",
        str(project_root / "tests"),
        "-v",  # verbose
        "--tb=short",  # shorter traceback format
        "--disable-warnings",  # disable warnings for cleaner output
        "--color=yes",  # colored output
        "-m", "not slow",  # exclude slow tests by default
    ]
    
    print("🧪 Running Portfolio Management Suite Tests")
    print("=" * 50)
    print("📋 Test Categories:")
    print("   • Core functionality tests")
    print("   • Environment setup verification") 
    print("   • Integration tests")
    print("   • End-to-end verification")
    print("=" * 50)
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✅ ALL TESTS PASSED")
        print("\n🚀 To run the application:")
        print("   python3.13 -m portfolio_suite --component web")
        print("   Then open: http://localhost:8501")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("   Check the output above for details")
        
    return result.returncode

def run_with_slow_tests():
    """Run all tests including slow integration tests."""
    project_root = Path(__file__).parent.parent
    
    cmd = [
        sys.executable, "-m", "pytest",
        str(project_root / "tests"),
        "-v",
        "--tb=short", 
        "--disable-warnings",
        "--color=yes",
        # Include slow tests
    ]
    
    print("🧪 Running ALL Portfolio Management Suite Tests (including slow tests)")
    print("=" * 70)
    
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--include-slow":
        sys.exit(run_with_slow_tests())
    else:
        sys.exit(main())
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--include-slow":
        sys.exit(run_with_slow_tests())
    else:
        sys.exit(main())
