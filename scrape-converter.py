#!/usr/bin/env python3
"""
WordPress Page Scraper for Design Conversion
This script scrapes the actual rendered WordPress pages to preserve design and content
"""

import requests
import json
import os
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from slugify import slugify
from bs4 import BeautifulSoup
import time

class WordPressPageScraper:
    def __init__(self, wp_url, output_dir="src/content"):
        self.wp_url = wp_url.rstrip('/')
        self.output_dir = output_dir
        self.images_dir = "public/images"
        self.pages_dir = "src/pages"
        
        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/posts", exist_ok=True)
        os.makedirs(f"{self.output_dir}/pages", exist_ok=True)
        
        # Headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def get_page_urls(self):
        """Get all page URLs from the sitemap or by crawling"""
        # First, let's get the pages from the API to get the slugs
        api_url = f"{self.wp_url}/wp-json/wp/v2/pages"
        response = requests.get(api_url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"❌ Error fetching pages from API: {response.status_code}")
            return []
        
        pages = response.json()
        page_urls = []
        
        for page in pages:
            slug = page.get('slug', '')
            if slug:
                if slug == 'home':
                    page_urls.append(self.wp_url)
                else:
                    page_urls.append(f"{self.wp_url}/{slug}/")
        
        return page_urls
    
    def download_image(self, image_url, filename):
        """Download and save image"""
        try:
            response = requests.get(image_url, headers=self.headers)
            if response.status_code == 200:
                # Create filename from URL
                parsed_url = urlparse(image_url)
                original_filename = os.path.basename(parsed_url.path)
                name, ext = os.path.splitext(original_filename)
                if not ext:
                    ext = '.jpg'  # Default extension
                
                # Use provided filename or generate one
                if not filename:
                    filename = f"{slugify(name)}{ext}"
                
                filepath = os.path.join(self.images_dir, filename)
                
                # Save image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return f"/images/{filename}"
        except Exception as e:
            print(f"❌ Error downloading image {image_url}: {e}")
        
        return image_url  # Return original URL if download fails
    
    def process_content(self, soup, page_url):
        """Process the scraped content for Astro"""
        # Process images
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # Make absolute URL
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = self.wp_url + src
                elif not src.startswith('http'):
                    src = urljoin(page_url, src)
                
                # Download image and update src
                filename = f"wp_{slugify(src.split('/')[-1])}"
                new_src = self.download_image(src, filename)
                img['src'] = new_src
        
        # Process links to other pages
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and self.wp_url in href:
                # Convert WordPress URLs to Astro URLs
                link['href'] = href.replace(self.wp_url, '')
        
        return soup
    
    def scrape_page(self, page_url):
        """Scrape a single page"""
        try:
            print(f"🔍 Scraping: {page_url}")
            response = requests.get(page_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"❌ Error scraping {page_url}: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "Untitled"
            
            # Remove common WordPress elements we don't want
            for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Find the main content area
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|post'))
            
            if not main_content:
                # If no main content found, try to find the body content
                main_content = soup.find('body')
                if main_content:
                    # Remove header, nav, footer
                    for element in main_content.find_all(['header', 'nav', 'footer']):
                        element.decompose()
            
            if main_content:
                # Process the content
                processed_soup = self.process_content(main_content, page_url)
                content_html = str(processed_soup)
            else:
                content_html = str(soup)
            
            return {
                'title': title,
                'content': content_html,
                'url': page_url
            }
            
        except Exception as e:
            print(f"❌ Error scraping {page_url}: {e}")
            return None
    
    def convert_to_astro_page(self, page_data, slug):
        """Convert scraped page data to Astro format"""
        title = page_data['title']
        content = page_data['content']
        
        # Create frontmatter
        frontmatter = {
            'title': title,
            'description': '',
            'draft': False
        }
        
        # Create Astro content
        astro_content = "---\n"
        for key, value in frontmatter.items():
            astro_content += f"{key}: {json.dumps(value)}\n"
        astro_content += "---\n\n"
        astro_content += content
        
        # Save markdown file
        filename = f"{slug}.md"
        filepath = os.path.join(self.output_dir, 'pages', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(astro_content)
        
        # Escape the title and content for Astro
        escaped_title = title.replace('"', '\\"').replace("'", "\\'")
        escaped_content = content.replace('"', '\\"').replace("'", "\\'")
        
        # Create Astro page file
        page_content = f"""---
title: "{escaped_title}"
description: ''
---

<Layout>
  <div class="prose max-w-none">
    <h1>{escaped_title}</h1>
    <div set:html={`{escaped_content}`} />
  </div>
</Layout>
"""
        
        # Save Astro page file
        if slug == 'home':
            astro_filepath = os.path.join(self.pages_dir, 'index.astro')
        else:
            astro_filepath = os.path.join(self.pages_dir, f"{slug}.astro")
        
        with open(astro_filepath, 'w', encoding='utf-8') as f:
            f.write(page_content)
        
        return filepath, astro_filepath
    
    def run_scraping(self):
        """Run the complete scraping process"""
        print("🚀 Starting WordPress page scraping...")
        print(f"WordPress URL: {self.wp_url}")
        print(f"Output directory: {self.output_dir}")
        
        # Get page URLs
        page_urls = self.get_page_urls()
        print(f"📊 Found {len(page_urls)} pages to scrape")
        
        if not page_urls:
            print("❌ No pages found to scrape")
            return
        
        # Scrape each page
        for i, page_url in enumerate(page_urls, 1):
            print(f"\n📄 Scraping page {i}/{len(page_urls)}: {page_url}")
            
            page_data = self.scrape_page(page_url)
            if page_data:
                # Extract slug from URL
                slug = page_url.replace(self.wp_url, '').strip('/')
                if not slug:
                    slug = 'home'
                
                # Convert to Astro
                md_path, astro_path = self.convert_to_astro_page(page_data, slug)
                print(f"   ✅ Created: {md_path}")
                print(f"   ✅ Created: {astro_path}")
            
            # Be respectful - add a small delay
            time.sleep(1)
        
        print("\n✅ Scraping complete!")
        print(f"\nNext steps:")
        print(f"1. Review the converted content in {self.output_dir}/")
        print(f"2. Check images in {self.images_dir}/")
        print(f"3. Run 'npm run dev' to preview your site")
        print(f"4. Customize the design and content as needed")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 scrape-converter.py <wordpress_url> [output_dir]")
        print("Example: python3 scrape-converter.py https://example.com")
        sys.exit(1)
    
    wp_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "src/content"
    
    scraper = WordPressPageScraper(wp_url, output_dir)
    scraper.run_scraping()

if __name__ == "__main__":
    main()
