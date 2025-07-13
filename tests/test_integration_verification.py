"""
Integration test that runs end-to-end verification.

This test runs our comprehensive verification script to ensure
all installation and setup issues are caught by the test suite.
"""

import subprocess
import sys
from pathlib import Path


def test_end_to_end_verification():
    """Run the comprehensive end-to-end verification script."""
    project_root = Path(__file__).parent.parent
    verify_script = project_root / "scripts" / "verify_installation.py"
    
    assert verify_script.exists(), "Verification script should exist"
    
    # Run the verification script
    result = subprocess.run([
        sys.executable, str(verify_script)
    ], capture_output=True, text=True, timeout=120)
    
    # Print output for debugging
    if result.stdout:
        print("\n--- Verification Output ---")
        print(result.stdout)
    
    if result.stderr:
        print("\n--- Verification Errors ---")
        print(result.stderr)
    
    # Script should exit with code 0 if all checks pass
    assert result.returncode == 0, f"End-to-end verification failed with exit code {result.returncode}"


if __name__ == "__main__":
    test_end_to_end_verification()
    print("✅ End-to-end verification test passed!")
