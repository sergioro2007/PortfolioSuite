#!/usr/bin/env python3
"""
Automated test runner for dual-model implementation
Runs all tests and provides comprehensive report
"""

import pytest
import sys
import os
import subprocess


def run_all_dual_model_tests():
    """Run comprehensive dual-model test suite"""
    test_files = [
        "tests/test_dual_model_core.py",
        "tests/test_dual_model_ui.py",
        "tests/test_dual_model_strategy.py",
        "tests/test_dual_model_end_to_end.py",
        "tests/test_dual_model_performance.py",
        "tests/test_enhanced_analysis.py",
    ]
    print("🧪 Running Comprehensive Dual-Model Test Suite")
    print("=" * 60)
    all_passed = True
    for test_file in test_files:
        print(f"\n📋 Running {test_file}...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✅ {test_file} - PASSED")
        else:
            print(f"❌ {test_file} - FAILED")
            print(result.stdout)
            print(result.stderr)
            all_passed = False
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL DUAL-MODEL TESTS PASSED!")
        print("✅ Implementation ready for production")
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️  Fix issues before deployment")
    return all_passed


if __name__ == "__main__":
    success = run_all_dual_model_tests()
    sys.exit(0 if success else 1)
