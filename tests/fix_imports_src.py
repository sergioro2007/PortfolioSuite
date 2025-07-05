#!/usr/bin/env python3
"""
Fix import paths in test files to use the new src/ folder structure
"""

import os
import glob

def fix_imports_for_src():
    """Update import paths in all test files to use src folder"""
    test_files = glob.glob("/Users/soliv112/PersonalProjects/Test/tests/*.py")
    
    print("🔧 Fixing import paths for src/ folder structure...")
    
    # Import statements to update
    import_updates = {
        'from options_tracker import': 'from src.options_tracker import',
        'from options_tracker_ui import': 'from src.options_tracker_ui import',
        'from tactical_tracker import': 'from src.tactical_tracker import',
        'from quality_tracker import': 'from src.quality_tracker import',
        'from main_app import': 'from src.main_app import',
        'from streamlit_app import': 'from src.streamlit_app import',
        'from options_analyzer import': 'from src.options_analyzer import',
        'import options_tracker': 'import src.options_tracker as options_tracker',
        'import options_tracker_ui': 'import src.options_tracker_ui as options_tracker_ui',
        'import tactical_tracker': 'import src.tactical_tracker as tactical_tracker',
        'import quality_tracker': 'import src.quality_tracker as quality_tracker',
        'import main_app': 'import src.main_app as main_app',
        'import streamlit_app': 'import src.streamlit_app as streamlit_app',
        'import options_analyzer': 'import src.options_analyzer as options_analyzer'
    }
    
    fixed_files = []
    
    for file_path in test_files:
        filename = os.path.basename(file_path)
        
        # Skip certain files
        if filename in ['__init__.py', 'fix_imports_src.py']:
            continue
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Apply import updates
            for old_import, new_import in import_updates.items():
                if old_import in content:
                    content = content.replace(old_import, new_import)
            
            # If content changed, write it back
            if content != original_content:
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"✅ Fixed imports in {filename}")
                fixed_files.append(filename)
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    print(f"\n🎯 Fixed import paths in {len(fixed_files)} files:")
    for filename in sorted(fixed_files):
        print(f"  - {filename}")

if __name__ == "__main__":
    fix_imports_for_src()
