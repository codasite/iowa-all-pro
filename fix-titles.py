#!/usr/bin/env python3
"""
Fix malformed titles in Astro files
"""

import os
import re
import glob

def fix_astro_file(filepath):
    """Fix a single Astro file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has malformed title
        if re.search(r'title:\s*["\']?[^"\']*\n[^"\']*["\']?', content):
            print(f"Fixing: {filepath}")
            
            # Extract the first part of the title before any line breaks
            title_match = re.search(r'title:\s*["\']?([^"\'\n]*)', content)
            if title_match:
                clean_title = title_match.group(1).strip()
                if clean_title:
                    # Replace the malformed title
                    content = re.sub(r'title:\s*["\']?[^"\']*\n[^"\']*["\']?', f'title: "{clean_title}"', content)
                    
                    # Also fix the h1 tag if it has the same issue
                    content = re.sub(r'<h1>[^<]*\n[^<]*</h1>', f'<h1>{clean_title}</h1>', content)
                    
                    # Fix the set:html content if it has the same issue
                    content = re.sub(r'<h2 class=\'ct-headline\'>[^<]*\n[^<]*</h2>', f'<h2 class=\'ct-headline\'>{clean_title}</h2>', content)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"  ✅ Fixed {filepath}")
                    return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all Astro files"""
    astro_files = glob.glob("src/pages/**/*.astro", recursive=True)
    
    fixed_count = 0
    for filepath in astro_files:
        if fix_astro_file(filepath):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} Astro files")

if __name__ == "__main__":
    main()
