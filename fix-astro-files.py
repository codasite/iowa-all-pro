#!/usr/bin/env python3
"""
Fix Astro files to properly escape content and titles
"""

import os
import re
import glob

def fix_astro_file(filepath):
    """Fix a single Astro file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file has the problematic pattern
        if 'set:html=' in content and not 'set:html={`' in content:
            print(f"Fixing: {filepath}")
            
            # Fix title if it's not quoted
            if re.search(r'title: [^"\'][^"\n]*[&<>]', content):
                content = re.sub(r'title: ([^"\'\n]+)', r'title: "\1"', content)
            
            # Fix set:html to use template literals
            content = re.sub(
                r'<div set:html=([^>]+) />',
                r'<div set:html={`\1`} />',
                content
            )
            
            # Write the fixed content back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all Astro files"""
    astro_files = glob.glob("src/pages/*.astro")
    
    fixed_count = 0
    for filepath in astro_files:
        if fix_astro_file(filepath):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} Astro files")

if __name__ == "__main__":
    main()
