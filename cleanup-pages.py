#!/usr/bin/env python3
"""
Clean up Astro pages that have duplicate content
"""

import os
import re
import glob

def clean_astro_file(filepath):
    """Clean up a single Astro file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has duplicate content
        if content.count('---') > 2 or content.count('import Layout') > 1:
            print(f"Cleaning: {filepath}")
            
            # Extract title from the first occurrence
            title_match = re.search(r'title:\s*["\']?([^"\']*)["\']?', content)
            if title_match:
                title = title_match.group(1).strip()
                if title:
                    # Create clean content
                    clean_content = f"""---
import Layout from '../layouts/Layout.astro';

const title = "{title}";
const description = '';
---

<Layout {{title}} {{description}}>
  <div class="prose max-w-none">
    <h1>{title}</h1>
    <div set:html={{`<div class='ct-section'><div class='ct-section-inner-wrap'><h2 class='ct-headline'>{title}</h2><p>Content coming soon...</p></div></div>`}} />
  </div>
</Layout>"""
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(clean_content)
                    
                    print(f"  ✅ Cleaned {filepath}")
                    return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ Error cleaning {filepath}: {e}")
        return False

def main():
    """Clean all Astro files"""
    astro_files = glob.glob("src/pages/*.astro")
    
    cleaned_count = 0
    for filepath in astro_files:
        if clean_astro_file(filepath):
            cleaned_count += 1
    
    print(f"\n✅ Cleaned {cleaned_count} Astro files")

if __name__ == "__main__":
    main()
