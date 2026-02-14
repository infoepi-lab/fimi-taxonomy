#!/usr/bin/env python3
"""
Fix BibTeX files by removing leading commas before entry types
"""
import os
import re
from pathlib import Path

def fix_bib_file(file_path):
    """Fix a single bib file by removing ,@ patterns"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace },\n,@ with },\n\n@
    # This handles the case where there's a closing brace, then a comma before the next entry
    fixed_content = re.sub(r'\}\s*\n\s*,@', r'}\n\n@', content)
    
    # Also handle case where line starts with ,@
    fixed_content = re.sub(r'^\s*,@', r'@', fixed_content, flags=re.MULTILINE)
    
    if content != fixed_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    return False

def main():
    function_dir = Path('function')
    bib_files = list(function_dir.glob('*.bib'))
    
    print(f"Found {len(bib_files)} .bib files in function/")
    print()
    
    fixed_count = 0
    for bib_file in sorted(bib_files):
        if fix_bib_file(bib_file):
            print(f"[FIXED] {bib_file.name}")
            fixed_count += 1
        else:
            print(f"[OK] {bib_file.name}")
    
    print()
    print(f"Fixed {fixed_count} files")

if __name__ == "__main__":
    main()
