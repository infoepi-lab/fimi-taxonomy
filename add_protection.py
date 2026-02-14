import os
import re
from pathlib import Path

def add_protected_content(file_path):
    """Add protected-content div to a QMD file if not already present."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already protected
    if '{.protected-content}' in content:
        print(f"  Already protected: {file_path}")
        return False
    
    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) >= 3:
        # Has frontmatter
        frontmatter = f"---{parts[1]}---"
        body = parts[2].strip()
    else:
        # No frontmatter
        frontmatter = ""
        body = content.strip()
    
    # Wrap body in protected-content div
    if body:
        protected_body = f"\n\n::: {{.protected-content}}\n\n{body}\n\n:::\n"
    else:
        protected_body = body
    
    # Reassemble
    if frontmatter:
        new_content = f"{frontmatter}\n{protected_body}"
    else:
        new_content = protected_body
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Protected: {file_path}")
    return True

def main():
    base_dir = Path('C:/Users/ERosa/Github/v4.0-infomap')
    
    # Files and directories to skip
    skip_files = {
        'index.qmd',  # Front page stays public
        'notes.qmd',  # Blog listing page
    }
    
    skip_dirs = {
        '.git', '.quarto', '_site', '_freeze', 'renv', '.Rproj.user', '_manuscripts'
    }
    
    protected_count = 0
    
    # Find all .qmd files
    print("\nAdding protected-content wrapper to pages...\n")
    
    for root, dirs, files in os.walk(base_dir):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.qmd') and file not in skip_files:
                file_path = Path(root) / file
                
                # Skip if in skip_files or is an index file that should stay public
                relative_path = file_path.relative_to(base_dir)
                
                if add_protected_content(file_path):
                    protected_count += 1
    
    print(f"\nProtected {protected_count} pages")
    print("index.qmd remains public (front page)")
    print("notes.qmd remains public (blog listing)")

if __name__ == '__main__':
    main()
