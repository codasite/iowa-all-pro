#!/usr/bin/env python3
"""
Comprehensive fix for all Astro pages to ensure they work properly
"""

import os
import re
import glob

def fix_astro_file(filepath):
    """Fix a single Astro file comprehensively"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Fixing: {filepath}")
        
        # Extract title from frontmatter
        title_match = re.search(r'title:\s*["\']?([^"\']*)["\']?', content)
        if not title_match:
            print(f"  No title found in {filepath}")
            return False
        
        original_title = title_match.group(1).strip()
        if not original_title:
            print(f"  Empty title in {filepath}")
            return False

        # Escape title for Astro
        escaped_title = original_title.replace('"', '\\"').replace("'", "\\'")

        # Find and fix set:html content
        html_content_match = re.search(r'<div set:html=(.*?) />', content, re.DOTALL)
        
        if html_content_match:
            original_html_content = html_content_match.group(1).strip()
            
            # Clean up the content
            if original_html_content and original_html_content != '=' and original_html_content != '':
                # Ensure content is wrapped in backticks for template literal
                if not original_html_content.startswith('`') or not original_html_content.endswith('`'):
                    escaped_html_content = f"`{original_html_content.strip('`')}`"
                else:
                    escaped_html_content = original_html_content
            else:
                # If no content, provide a basic structure
                escaped_html_content = f"`<div class='ct-section'><div class='ct-section-inner-wrap'><h2 class='ct-headline'>{escaped_title}</h2><p>Content coming soon...</p></div></div>`"
        else:
            # If no set:html found, add one
            escaped_html_content = f"`<div class='ct-section'><div class='ct-section-inner-wrap'><h2 class='ct-headline'>{escaped_title}</h2><p>Content coming soon...</p></div></div>`"

        # Reconstruct the Astro file content
        new_content = content
        
        # Fix title in frontmatter
        new_content = re.sub(r'title:\s*["\']?[^"\']*["\']?', f'title: "{escaped_title}"', new_content, 1)
        
        # Fix or add set:html content
        if html_content_match:
            new_content = re.sub(r'<div set:html=.*? />', f'<div set:html={escaped_html_content} />', new_content, 1)
        else:
            # Add set:html if missing
            new_content = re.sub(r'<h1>.*?</h1>', f'<h1>{escaped_title}</h1>\n    <div set:html={escaped_html_content} />', new_content, 1)

        # Add Layout import and props if not present
        if "import Layout from '../layouts/Layout.astro';" not in new_content:
            new_content = new_content.replace("---", f"---\nimport Layout from '../layouts/Layout.astro';\n\nconst title = \"{escaped_title}\";\nconst description = '';")
            new_content = new_content.replace("<Layout>", "<Layout {title} {description}>")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ Fixed {filepath}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all Astro files"""
    astro_files = glob.glob("src/pages/*.astro")
    
    print(f"Found {len(astro_files)} Astro files to check")
    
    fixed_count = 0
    for filepath in astro_files:
        if fix_astro_file(filepath):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} Astro files")

if __name__ == "__main__":
    main()
