#!/usr/bin/env python3
"""
Add model-viewer debug script to all pages missing it
"""
import os
import re
from pathlib import Path

DEBUG_SCRIPT_TAG = '<script src="/assets/js/model-viewer-debug.js" defer></script>'

INIT_SCRIPT = '''  <!-- Model Viewer Fix Script - Direct initialization -->
  <script>
    (function() {
      console.log('[Model-Viewer Init] Checking model-viewer status...');
      
      // Wait for model-viewer to be loaded
      const checkModelViewer = () => {
        const viewer = document.querySelector('model-viewer');
        if (!viewer) {
          console.log('[Model-Viewer Init] No model-viewer element found');
          return;
        }
        
        // Check if custom element is registered
        if (window.customElements && window.customElements.get('model-viewer')) {
          console.log('[Model-Viewer Init] model-viewer element is registered ✓');
          return;
        }
        
        // If not registered yet, check again in 500ms
        setTimeout(checkModelViewer, 500);
      };
      
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', checkModelViewer);
      } else {
        setTimeout(checkModelViewer, 100);
      }
    })();
  </script>'''

def fix_page(file_path):
    """Add debug script to a model-viewer page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has debug script
    if 'model-viewer-debug.js' in content:
        return False, "Already has debug script"
    
    # Add debug script tag to head (before closing </head>)
    if DEBUG_SCRIPT_TAG not in content:
        content = content.replace(
            '</head>',
            f'  {DEBUG_SCRIPT_TAG}\n</head>'
        )
    
    # Add initialization script before closing </body> if not present
    if '[Model-Viewer Init]' not in content:
        content = content.replace(
            '</body>',
            f'\n  {INIT_SCRIPT}\n</body>'
        )
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, "Added debug script and initialization"

def main():
    root = Path('/workspaces/Website4.0')
    
    # Find all model-viewer pages
    import subprocess
    result = subprocess.run(
        "find /workspaces/Website4.0 -type f -name 'index.html' -exec grep -l 'model-viewer' {} \\;",
        shell=True,
        capture_output=True,
        text=True
    )
    
    all_pages = [Path(p.strip()) for p in result.stdout.strip().split('\n') if p.strip()]
    print(f"Found {len(all_pages)} model-viewer pages")
    
    fixed = 0
    skipped = 0
    
    for page_path in sorted(all_pages):
        changed, msg = fix_page(page_path)
        rel_path = page_path.relative_to(root)
        
        if changed:
            print(f"✓ Fixed: {rel_path}")
            fixed += 1
        else:
            skipped += 1
    
    print(f"\nTotal: {fixed} fixed, {skipped} already correct")

if __name__ == '__main__':
    main()
