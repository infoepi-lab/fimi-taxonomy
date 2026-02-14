#!/usr/bin/env python3
"""
Fix the remaining 21 citation issues
"""
import re
from pathlib import Path

def fix_file(file_path, replacements):
    """Apply citation replacements to a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements.items():
        content = re.sub(r'@' + old + r'\b', '@' + new, content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixes = {
        'function/legitimation-chapter.qmd': {
            # Fuzzy matches
            'cia1955': 'CIA1955',
            'huang2019': 'HUANG2019',
            'kamyshanskaya2021': 'KAMYSHANSKAYA2021',
            'redden2013': 'REDDEN2013',
            'shikerova2022': 'SHIKEROVA2022',
            # Known mappings
            'mkinen2016': 'MAKINEN2016',
            'alexiev1985': 'Alexiev19852',
            'soviet1954': 'F1954',
            # Probable mappings
            'center2020': 'GLOBAL_ENGAGEMENT_CENTER2020',
            'department2024': 'US_DEPARTMENT_OF_STATE2024',
            'post2024': 'THE_WASHINGTON_POST2024',
            # Remove missing ones
            'alex2020': 'REMOVED',
            'china2024': 'REMOVED',
            'douma2018': 'REMOVED',
            'page2025': 'REMOVED',
            'the1971': 'REMOVED',
        },
        'function/projection-abroad-chapter.qmd': {
            'HRW20221': 'hrw2022',
            # Remove MISSING placeholders
            'MISSING_NoVD': 'REMOVED',
            'MISSING_nvg9': 'REMOVED',
            'MISSING_xgql': 'REMOVED',
        },
        'function/projection-abroad.qmd': {
            'methods': 'REMOVED',
        },
        'mechanisms/academic-initiatives.qmd': {
            'cia1955': 'CIA1955',
        }
    }
    
    print("Fixing citations...\n")
    
    for file_path, replacements in fixes.items():
        # Filter out REMOVED items - we'll handle those separately
        actual_replacements = {k: v for k, v in replacements.items() if v != 'REMOVED'}
        
        if actual_replacements and fix_file(file_path, actual_replacements):
            print(f"[FIXED] {file_path}")
            for old, new in actual_replacements.items():
                print(f"  {old} -> {new}")
        
        # Handle REMOVED citations by showing warning
        removed = {k for k, v in replacements.items() if v == 'REMOVED'}
        if removed:
            print(f"\n[WARNING] {file_path} has citations to remove manually:")
            for citation in removed:
                print(f"  @{citation}")
    
    print("\nDone! Run quarto render to verify.")

if __name__ == "__main__":
    main()
