#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_html_structure(file_path):
    """Remove stray closing divs and extra whitespace after header include"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern to fix: div with header include, followed by empty lines and a closing div, then h1
    # This replaces the pattern with just the include div and h1
    pattern = r'(<div data-include="/header-tr\.html"></div>)\s*\n\s*\n\s*(?:\n\s*)*\s*</div>\s*\n\s*(<h1[^>]*>)'
    replacement = r'\1\n\n  \2'
    
    content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Find all index.html files with model-viewer
root = Path('/workspaces/Website4.0')

# Get all model-viewer pages
model_viewer_pages = []
for index_file in root.rglob('index.html'):
    with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
        if 'model-viewer' in f.read():
            model_viewer_pages.append(index_file)

print(f"Found {len(model_viewer_pages)} model-viewer pages")

fixed_count = 0
for page in sorted(model_viewer_pages):
    if fix_html_structure(page):
        print(f"✓ Fixed: {page.relative_to(root)}")
        fixed_count += 1
    else:
        print(f"  Already OK: {page.relative_to(root)}")

print(f"\nTotal fixed: {fixed_count}")
