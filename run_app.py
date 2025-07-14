#!/usr/bin/env python3
"""
Portfolio Suite Application Launcher
=====================================
A simplified launcher that properly sets up the Python path and runs the application.
"""
import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Now import and run the application
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    import sys
    
    print("🚀 Starting Portfolio Management Suite...")
    print("📁 Project Root:", project_root)
    print("🐍 Python Path:", sys.path[0])
    
    # Set up streamlit to run the main app
    sys.argv = [
        "streamlit", 
        "run", 
        str(project_root / "src" / "portfolio_suite" / "ui" / "main_app.py"),
        "--server.address", "localhost",
        "--server.port", "8501"
    ]
    
    stcli.main()
