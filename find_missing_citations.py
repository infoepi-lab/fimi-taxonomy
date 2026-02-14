#!/usr/bin/env python3
"""
Find all citations that are used in .qmd files but missing from .bib files
"""
import re
from pathlib import Path
from collections import defaultdict

def extract_citations_from_qmd(file_path):
    """Extract all citation keys from a .qmd file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    citations = set()
    pattern = r'@([\w\-]+)'
    for match in re.finditer(pattern, content):
        key = match.group(1)
        # Filter out common false positives
        if key not in ['fig', 'tbl', 'eq', 'sec', 'lst', 'thm', 'lem', 'cor', 'prp', 'cnj', 'def', 'exm', 'exr']:
            citations.add(key)
    
    return citations

def extract_keys_from_bib(file_path):
    """Extract all entry keys from a .bib file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    keys = set()
    pattern = r'@\w+\{([^,\s]+),'
    for match in re.finditer(pattern, content):
        keys.add(match.group(1))
    
    return keys

def normalize_key(key):
    """Normalize a key for fuzzy matching"""
    return key.replace('-', '').replace('_', '').lower()

def main():
    print("Scanning for citations and bibliography entries...\n")
    
    # Collect all citations from .qmd files
    all_citations = defaultdict(list)  # key -> list of files using it
    
    for qmd_file in Path('.').rglob('*.qmd'):
        if '_site' in str(qmd_file) or '_freeze' in str(qmd_file):
            continue
        citations = extract_citations_from_qmd(qmd_file)
        for citation in citations:
            all_citations[citation].append(str(qmd_file))
    
    print(f"Found {len(all_citations)} unique citation keys used in .qmd files")
    
    # Collect all keys from .bib files
    all_bib_keys = set()
    bib_key_map = {}  # normalized -> actual key
    
    function_dir = Path('function')
    for bib_file in function_dir.glob('*.bib'):
        keys = extract_keys_from_bib(bib_file)
        all_bib_keys.update(keys)
        for key in keys:
            bib_key_map[normalize_key(key)] = key
    
    print(f"Found {len(all_bib_keys)} unique keys in .bib files\n")
    
    # Find missing citations
    missing = {}
    fuzzy_matches = {}
    
    for citation, files in sorted(all_citations.items()):
        if citation not in all_bib_keys:
            # Try fuzzy match
            normalized = normalize_key(citation)
            if normalized in bib_key_map:
                fuzzy_matches[citation] = bib_key_map[normalized]
            else:
                missing[citation] = files
    
    # Report fuzzy matches
    if fuzzy_matches:
        print("=" * 70)
        print("FUZZY MATCHES - Citation key differs from bib entry:")
        print("=" * 70)
        for citation, bib_key in sorted(fuzzy_matches.items()):
            print(f"\n  Citation: @{citation}")
            print(f"  Bib entry: {bib_key}")
            print(f"  -> Need to change either citation or bib key to match")
    
    # Report missing
    if missing:
        print("\n" + "=" * 70)
        print("MISSING CITATIONS - Used in .qmd but not found in any .bib:")
        print("=" * 70)
        for citation, files in sorted(missing.items()):
            print(f"\n  @{citation}")
            print(f"  Used in:")
            for file in files[:3]:  # Show first 3 files
                print(f"    - {file}")
            if len(files) > 3:
                print(f"    ... and {len(files) - 3} more files")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total citations used: {len(all_citations)}")
    print(f"Total bib entries: {len(all_bib_keys)}")
    print(f"Fuzzy matches (need fixing): {len(fuzzy_matches)}")
    print(f"Missing entries: {len(missing)}")
    
    if not fuzzy_matches and not missing:
        print("\n[OK] All citations have matching bibliography entries!")

if __name__ == "__main__":
    main()
