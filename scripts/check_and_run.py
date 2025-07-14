#!/usr/bin/env python3
"""
Quick verification script to ensure Portfolio Suite is working.

Run this after any setup or installation to verify everything is operational.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Run quick verification and optionally start the application."""
    project_root = Path(__file__).parent
    
    print("🔍 Quick Portfolio Suite Verification")
    print("=" * 40)
    
    # Run verification script
    verify_script = project_root / "scripts" / "verify_installation.py"
    if verify_script.exists():
        print("📋 Running comprehensive verification...")
        result = subprocess.run([sys.executable, str(verify_script)])
        
        if result.returncode == 0:
            print("\n🎯 Quick Test Suite...")
            # Run core tests only (fast verification)
            test_result = subprocess.run([
                sys.executable, "-m", "pytest", 
                str(project_root / "tests"),
                "-m", "not slow and not integration",
                "-q", "--tb=no"
            ])
            
            if test_result.returncode == 0:
                print("✅ Core tests passed")
                
                # Ask if user wants to start the application
                response = input("\n🚀 Start the Portfolio Suite web app? (y/N): ").strip().lower()
                if response in ['y', 'yes']:
                    print("\n🌐 Starting Portfolio Suite...")
                    print("   Open http://localhost:8501 in your browser")
                    print("   Press Ctrl+C to stop")
                    
                    subprocess.run([
                        sys.executable, "-m", "portfolio_suite", "--component", "web"
                    ])
                else:
                    print("\n✅ Verification complete! To start later:")
                    print("   python3.13 -m portfolio_suite --component web")
            else:
                print("❌ Some core tests failed")
                return 1
        else:
            print("❌ Verification failed")
            return 1
    else:
        print("❌ Verification script not found")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
