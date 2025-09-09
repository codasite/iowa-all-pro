#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse
import time

def clean_title(title):
    """Clean and format page titles"""
    # Remove extra whitespace and newlines
    title = re.sub(r'\s+', ' ', title.strip())
    # Remove any remaining description: text
    title = re.sub(r'\s+description:\s*$', '', title)
    return title

def extract_page_content(url, page_name):
    """Extract content from a WordPress page"""
    try:
        print(f"Scraping {page_name} from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = clean_title(title_tag.get_text()) if title_tag else page_name.title()
        
        # Find the main content area
        content_div = soup.find('div', class_='ct-inner-content')
        if not content_div:
            # Fallback to looking for content in other common containers
            content_div = soup.find('div', class_='entry-content') or soup.find('main')
        
        if content_div:
            # Get all the HTML content
            content_html = str(content_div)
            # Clean up the HTML
            content_html = re.sub(r'\s+', ' ', content_html)
            content_html = re.sub(r'>\s+<', '><', content_html)
        else:
            content_html = f'<div class="ct-section"><div class="ct-section-inner-wrap"><h2 class="ct-headline">{page_name.title()}</h2><p>Content coming soon...</p></div></div>'
        
        return title, content_html
        
    except Exception as e:
        print(f"Error scraping {page_name}: {e}")
        return page_name.title(), f'<div class="ct-section"><div class="ct-section-inner-wrap"><h2 class="ct-headline">{page_name.title()}</h2><p>Content coming soon...</p></div></div>'

def create_astro_page(page_name, title, content, is_service=False):
    """Create an Astro page with proper Oxygen styling"""
    
    # Determine the file path
    if is_service:
        file_path = f"src/pages/services/{page_name}.astro"
        layout_import = "../../layouts/Layout.astro"
    else:
        file_path = f"src/pages/{page_name}.astro"
        layout_import = "../layouts/Layout.astro"
    
    # Create the Astro content
    astro_content = f'''---
import Layout from '{layout_import}';

const title = "{title}";
const description = '';
---

<Layout {{title}} {{description}}>
  <div class="ct-inner-content">
    <div set:html={{`{content}`}} />
  </div>
</Layout>
'''
    
    # Write the file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(astro_content)
    
    print(f"Created {file_path}")

def main():
    base_url = "https://iowaallpro2.republicleadhunter.com"
    
    # Define all pages to scrape
    pages = [
        # Main pages
        ("about", "About", False),
        ("contact", "Contact", False),
        ("testimonials", "Testimonials", False),
        ("financing", "Financing", False),
        ("privacy-policy", "Privacy Policy", False),
        
        # Service pages
        ("services/cooling", "Cooling Services", True),
        ("services/heating", "Heating Services", True),
        ("services/duct-cleaning", "Duct Cleaning Services", True),
        ("services/indoor-air-quality", "Indoor Air Quality Services", True),
        ("services/commercial-hvac", "Commercial HVAC Services", True),
    ]
    
    for page_path, page_name, is_service in pages:
        url = f"{base_url}/{page_path}/"
        title, content = extract_page_content(url, page_name)
        create_astro_page(page_path.split('/')[-1], title, content, is_service)
        time.sleep(1)  # Be respectful to the server
    
    print("All pages have been rebuilt with proper Oxygen styling!")

if __name__ == "__main__":
    main()
