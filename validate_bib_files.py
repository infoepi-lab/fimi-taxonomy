#!/usr/bin/env python3
"""
Validate BibTeX files for common syntax errors
"""
import re
from pathlib import Path

def check_bib_file(file_path):
    """Check a single bib file for syntax errors"""
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        # Check for field assignment without trailing comma before next field
        # Pattern: field = "value"  (no comma) followed by field = 
        if re.match(r'\s+\w+\s+=', line):
            # This line is a field assignment
            # Check if previous line was also a field assignment without comma
            if i > 1:
                prev_line = lines[i-2].rstrip()
                # Check if previous line ends with } or " but not ,
                if re.search(r'["}]\s*$', prev_line) and not re.search(r',\s*$', prev_line):
                    # Check it's not a closing brace for an entry
                    if not re.match(r'^\}', prev_line):
                        errors.append({
                            'line': i-1,
                            'text': prev_line,
                            'error': 'Missing comma at end of field'
                        })
    
    return errors

def main():
    function_dir = Path('function')
    bib_files = list(function_dir.glob('*.bib'))
    
    print(f"Checking {len(bib_files)} .bib files...\n")
    
    total_errors = 0
    for bib_file in sorted(bib_files):
        errors = check_bib_file(bib_file)
        if errors:
            print(f"\n{bib_file.name}:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  Line {error['line']}: {error['error']}")
                print(f"    {error['text'][:80]}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more errors")
            total_errors += len(errors)
    
    print(f"\n\nTotal errors found: {total_errors}")

if __name__ == "__main__":
    main()

