#!/usr/bin/env python3
"""
Update Airtable mechanisms table with Quarto content
"""
import os
import requests
import json
from pathlib import Path

# Configuration
BASE_ID = "appX0FUC8U8cgWGph"
TABLE_ID = ""  # You'll provide this when running
AIRTABLE_API_TOKEN = ""  # You'll add this when running the script

def get_airtable_headers(token):
    """Generate headers for Airtable API requests"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_all_records(token, base_id, table_id):
    """Fetch all records from the mechanisms table"""
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
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

def update_record(token, base_id, table_id, record_id, quarto_content):
    """Update a single record's quarto field"""
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}"
    headers = get_airtable_headers(token)
    
    payload = {
        "fields": {
            "quarto": quarto_content
        }
    }
    
    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def filename_to_mechanism_name(filename):
    """Convert filename to mechanism name"""
    # Remove .qmd extension
    name = filename.replace('.qmd', '')
    # Convert hyphens to spaces and title case
    name = name.replace('-', ' ').title()
    return name

def main():
    # Get configuration from user
    table_id = input("Enter the mechanisms table ID (e.g., tblXXXXXXXXXXXXXX): ").strip()
    if not table_id:
        print("Error: No table ID provided")
        return
    
    token = input("Enter your Airtable Personal Access Token: ").strip()
    if not token:
        print("Error: No token provided")
        return
    
    print("\n🔍 Fetching records from Airtable...")
    try:
        records = get_all_records(token, BASE_ID, table_id)
        print(f"✓ Found {len(records)} records in the mechanisms table")
    except Exception as e:
        print(f"❌ Error fetching records: {e}")
        return
    
    # Create a mapping of mechanism name to record ID
    mechanism_to_record = {}
    for record in records:
        fields = record.get('fields', {})
        mechanism_name = fields.get('mechanism')
        if mechanism_name:
            mechanism_to_record[mechanism_name] = record['id']
    
    print(f"\n📋 Found {len(mechanism_to_record)} mechanisms in Airtable")
    
    # Read mechanism files and prepare updates
    mechanisms_dir = Path("mechanisms")
    qmd_files = list(mechanisms_dir.glob("*.qmd"))
    
    # Exclude index.qmd
    qmd_files = [f for f in qmd_files if f.name != "index.qmd"]
    
    print(f"\n📖 Found {len(qmd_files)} .qmd files in mechanisms/ directory")
    
    updates = []
    not_found = []
    
    for qmd_file in sorted(qmd_files):
        # Read the content
        with open(qmd_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to match by filename
        filename_based_name = filename_to_mechanism_name(qmd_file.name)
        
        # Try to find matching record (try exact match and case-insensitive)
        record_id = None
        matched_name = None
        
        for mech_name in mechanism_to_record.keys():
            if mech_name.lower() == filename_based_name.lower():
                record_id = mechanism_to_record[mech_name]
                matched_name = mech_name
                break
        
        if record_id:
            updates.append({
                'mechanism_name': matched_name,
                'record_id': record_id,
                'content': content,
                'file': qmd_file.name
            })
            print(f"✓ {matched_name}: {len(content)} characters from {qmd_file.name}")
        else:
            not_found.append(qmd_file.name)
    
    if not_found:
        print(f"\n⚠️  Could not match {len(not_found)} files to Airtable records:")
        for filename in sorted(not_found)[:10]:  # Show first 10
            print(f"  - {filename}")
        if len(not_found) > 10:
            print(f"  ... and {len(not_found) - 10} more")
    
    if not updates:
        print("\n❌ No updates to perform")
        return
    
    # Confirm before updating
    print(f"\n📝 Ready to update {len(updates)} records in Airtable")
    print("This will update the 'quarto' field with the mechanism content.")
    confirm = input("\nProceed with updates? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Cancelled")
        return
    
    # Perform updates
    print("\n🚀 Updating records...")
    success_count = 0
    for update in updates:
        try:
            update_record(token, BASE_ID, table_id, update['record_id'], update['content'])
            print(f"✓ Updated: {update['mechanism_name']}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to update {update['mechanism_name']}: {e}")
    
    print(f"\n✅ Complete! Successfully updated {success_count}/{len(updates)} records")

if __name__ == "__main__":
    main()
