#!/usr/bin/env python3
"""
🧪 Portfolio Management Suite Test Launcher
===========================================

Simple launcher that calls the master test runner in the tests folder.
This allows running tests from the root directory while keeping all test files organized.

Usage: python run_tests.py [options]
"""

import os
import sys
import subprocess

def main():
    # Get the path to the master test runner
    script_dir = os.path.dirname(os.path.abspath(__file__))
    master_runner = os.path.join(script_dir, 'tests', 'master_test_runner.py')
    
    if not os.path.exists(master_runner):
        print("❌ Master test runner not found in tests folder")
        return 1
    
    # Pass all arguments to the master test runner
    cmd = [sys.executable, master_runner] + sys.argv[1:]
    
    try:
        result = subprocess.run(cmd, cwd=script_dir)
        return result.returncode
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
