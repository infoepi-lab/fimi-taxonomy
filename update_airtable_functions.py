#!/usr/bin/env python3
"""
Update Airtable function table with Quarto chapter content
"""
import os
import requests
import json
from pathlib import Path

# Configuration
BASE_ID = "appX0FUC8U8cgWGph"
TABLE_ID = "tbl8t0aTmayDTA7CU"
AIRTABLE_API_TOKEN = ""  # You'll add this when running the script

# Mapping from chapter filenames to function names in Airtable
CHAPTER_TO_FUNCTION = {
    "command-and-control-chapter.qmd": "Command and Control",
    "legitimation-chapter.qmd": "Legitimation",
    "longevity-chapter.qmd": "Longevity",
    "obfuscation-chapter.qmd": "Obfuscation",
    "operational-multipliers-chapter.qmd": "Operational Multipliers",
    "projection-abroad-chapter.qmd": "Projection Abroad",
    "sabotage-chapter.qmd": "Sabotage",
    "spillover-chapter.qmd": "Spillover",
    "structural-terrain-chapter.qmd": "Structural Terrain"
}

def get_airtable_headers(token):
    """Generate headers for Airtable API requests"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_all_records(token):
    """Fetch all records from the function table"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"
    headers = get_airtable_headers(token)
    
    all_records = []
    offset = None
    
    while True:
        params = {}
        if offset:
            params['offset'] = offset
            
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        all_records.extend(data.get('records', []))
        
        offset = data.get('offset')
        if not offset:
            break
    
    return all_records

def update_record(token, record_id, quarto_content):
    """Update a single record's quarto field"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}/{record_id}"
    headers = get_airtable_headers(token)
    
    payload = {
        "fields": {
            "quarto": quarto_content
        }
    }
    
    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    # Get API token from user
    token = input("Enter your Airtable Personal Access Token: ").strip()
    if not token:
        print("Error: No token provided")
        return
    
    # Set the token
    global AIRTABLE_API_TOKEN
    AIRTABLE_API_TOKEN = token
    
    print("\n🔍 Fetching records from Airtable...")
    try:
        records = get_all_records(token)
        print(f"✓ Found {len(records)} records in the function table")
    except Exception as e:
        print(f"❌ Error fetching records: {e}")
        return
    
    # Create a mapping of function name to record ID
    function_to_record = {}
    for record in records:
        fields = record.get('fields', {})
        function_name = fields.get('functions')  # Note: column is 'functions' not 'function'
        if function_name:
            function_to_record[function_name] = record['id']
    
    print(f"\n📋 Found {len(function_to_record)} functions in Airtable:")
    for func_name in sorted(function_to_record.keys()):
        print(f"  - {func_name}")
    
    # Read chapter files and prepare updates
    function_dir = Path("function")
    updates = []
    
    print("\n📖 Reading chapter files...")
    for chapter_file, function_name in CHAPTER_TO_FUNCTION.items():
        chapter_path = function_dir / chapter_file
        
        if not chapter_path.exists():
            print(f"⚠️  Skipping {function_name}: file not found ({chapter_file})")
            continue
        
        if function_name not in function_to_record:
            print(f"⚠️  Skipping {function_name}: not found in Airtable")
            continue
        
        # Read the chapter content
        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        record_id = function_to_record[function_name]
        updates.append({
            'function_name': function_name,
            'record_id': record_id,
            'content': content,
            'file': chapter_file
        })
        
        print(f"✓ {function_name}: {len(content)} characters from {chapter_file}")
    
    if not updates:
        print("\n❌ No updates to perform")
        return
    
    # Confirm before updating
    print(f"\n📝 Ready to update {len(updates)} records in Airtable")
    print("This will update the 'quarto' field with the chapter content.")
    confirm = input("\nProceed with updates? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Cancelled")
        return
    
    # Perform updates
    print("\n🚀 Updating records...")
    success_count = 0
    for update in updates:
        try:
            update_record(token, update['record_id'], update['content'])
            print(f"✓ Updated: {update['function_name']}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to update {update['function_name']}: {e}")
    
    print(f"\n✅ Complete! Successfully updated {success_count}/{len(updates)} records")

if __name__ == "__main__":
    main()
