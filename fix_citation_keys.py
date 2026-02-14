#!/usr/bin/env python3
"""
Fix citation key mismatches between .qmd files and .bib files
"""
import re
from pathlib import Path
from collections import defaultdict

def extract_citations_from_qmd(file_path):
    """Extract all citation keys from a .qmd file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all citations like [@key] or [@key1; @key2]
    citations = set()
    # Pattern: @ followed by word characters (letters, numbers, underscores)
    pattern = r'@([\w\-]+)'
    for match in re.finditer(pattern, content):
        citations.add(match.group(1))
    
    return citations

def extract_keys_from_bib(file_path):
    """Extract all entry keys from a .bib file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all entry keys like @ARTICLE{key,
    keys = {}
    pattern = r'@\w+\{([^,\s]+),'
    for match in re.finditer(pattern, content):
        key = match.group(1)
        keys[key.lower()] = key  # Map lowercase to actual key
    
    return keys

def fix_bib_keys(bib_file, key_mappings):
    """Fix citation keys in a .bib file"""
    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # Replace each old key with new key
    for old_key, new_key in key_mappings.items():
        # Pattern to match the entry declaration
        pattern = r'(@\w+\{)' + re.escape(old_key) + r','
        
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1' + new_key + ',', content)
            changes.append(f"  {old_key} -> {new_key}")
    
    if changes:
        with open(bib_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return changes

def main():
    # Collect all citations from .qmd files
    all_citations = set()
    
    print("Scanning .qmd files for citations...")
    for qmd_file in Path('.').rglob('*.qmd'):
        if '_site' in str(qmd_file):
            continue
        citations = extract_citations_from_qmd(qmd_file)
        all_citations.update(citations)
    
    print(f"Found {len(all_citations)} unique citation keys in .qmd files\n")
    
    # Process each .bib file
    print("Processing .bib files...\n")
    
    function_dir = Path('function')
    bib_files = list(function_dir.glob('*.bib'))
    
    total_fixes = 0
    
    for bib_file in sorted(bib_files):
        # Get all keys from this bib file
        bib_keys = extract_keys_from_bib(bib_file)
        
        # Find mismatches
        key_mappings = {}
        for citation in all_citations:
            citation_lower = citation.lower()
            if citation_lower in bib_keys:
                actual_key = bib_keys[citation_lower]
                if actual_key != citation:
                    # Found a mismatch - map it
                    key_mappings[actual_key] = citation
        
        if key_mappings:
            print(f"{bib_file.name}:")
            changes = fix_bib_keys(bib_file, key_mappings)
            for change in changes:
                print(change)
            print()
            total_fixes += len(changes)
    
    print(f"\nTotal keys fixed: {total_fixes}")
    
    if total_fixes == 0:
        print("No mismatches found - all citation keys already match!")

if __name__ == "__main__":
    main()
