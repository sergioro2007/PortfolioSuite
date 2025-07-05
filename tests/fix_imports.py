#!/usr/bin/env python3
"""
Batch fix import paths in all test files
"""

import os
import re

# Directory containing test files
test_dir = '/Users/soliv112/PersonalProjects/Test/tests'

# Correct import pattern
correct_import = """# Add parent directory to path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))"""

def fix_imports_in_file(filepath):
    """Fix import paths in a single file"""
    if not filepath.endswith('.py'):
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Skip if already has the correct import
    if "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))" in content:
        return False
    
    # Patterns to replace
    patterns_to_replace = [
        r"sys\.path\.append\(os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\)",
        r"sys\.path\.append\('/Users/soliv112/PersonalProjects/Test'\)",
        r"sys\.path\.insert\(0, os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\)",
    ]
    
    # Check if file has import statements and sys module
    has_sys_import = 'import sys' in content
    has_os_import = 'import os' in content
    
    modified = False
    
    # Replace existing incorrect patterns
    for pattern in patterns_to_replace:
        if re.search(pattern, content):
            content = re.sub(pattern, "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))", content)
            modified = True
    
    # If no sys.path modification found but has imports, add the correct one
    if not modified and has_sys_import and has_os_import:
        # Find a good place to insert the path modification
        lines = content.split('\n')
        insert_line = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('import os') or line.strip().startswith('import sys'):
                insert_line = i + 1
        
        if insert_line > 0:
            lines.insert(insert_line, "")
            lines.insert(insert_line + 1, "# Add parent directory to path so we can import the main modules")
            lines.insert(insert_line + 2, "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))")
            content = '\n'.join(lines)
            modified = True
    
    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Fix imports in all test files"""
    print("🔧 Fixing import paths in test files...")
    
    fixed_files = []
    for filename in os.listdir(test_dir):
        if filename.endswith('.py') and filename != 'fix_imports.py':
            filepath = os.path.join(test_dir, filename)
            if fix_imports_in_file(filepath):
                fixed_files.append(filename)
                print(f"✅ Fixed imports in {filename}")
    
    if fixed_files:
        print(f"\n🎯 Fixed import paths in {len(fixed_files)} files:")
        for filename in sorted(fixed_files):
            print(f"  - {filename}")
    else:
        print("✅ All test files already have correct import paths")

if __name__ == "__main__":
    main()
