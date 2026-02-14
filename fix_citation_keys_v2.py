#!/usr/bin/env python3
"""
Fix citation key mismatches between .qmd files and .bib files
Enhanced version that handles hyphens and suffixes
"""
import re
from pathlib import Path

def normalize_key(key):
    """Normalize a citation key by removing hyphens and converting to lowercase"""
    return key.replace('-', '').lower()

def extract_citations_from_qmd(file_path):
    """Extract all citation keys from a .qmd file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    citations = set()
    pattern = r'@([\w\-]+)'
    for match in re.finditer(pattern, content):
        citations.add(match.group(1))
    
    return citations

def extract_keys_from_bib(file_path):
    """Extract all entry keys from a .bib file with normalization"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    keys = {}
    pattern = r'@\w+\{([^,\s]+),'
    for match in re.finditer(pattern, content):
        actual_key = match.group(1)
        normalized = normalize_key(actual_key)
        keys[normalized] = actual_key
    
    return keys

def fix_bib_keys(bib_file, key_mappings):
    """Fix citation keys in a .bib file"""
    with open(bib_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    for old_key, new_key in key_mappings.items():
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
        bib_keys = extract_keys_from_bib(bib_file)
        
        key_mappings = {}
        for citation in all_citations:
            citation_normalized = normalize_key(citation)
            
            # Try exact match first
            if citation_normalized in bib_keys:
                actual_key = bib_keys[citation_normalized]
                if actual_key != citation:
                    key_mappings[actual_key] = citation
            else:
                # Try with '1' suffix
                citation_with_suffix = citation_normalized + '1'
                if citation_with_suffix in bib_keys:
                    actual_key = bib_keys[citation_with_suffix]
                    if normalize_key(actual_key) != citation_normalized:
                        # Map the suffixed key to the non-suffixed citation
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
        print("No mismatches found!")

if __name__ == "__main__":
    main()
