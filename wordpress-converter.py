#!/usr/bin/env python3
"""
WordPress to Astro Conversion Script
This script converts a WordPress site to Astro using the REST API
"""

import requests
import json
import os
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from slugify import slugify
from bs4 import BeautifulSoup
from PIL import Image
import io

class WordPressToAstroConverter:
    def __init__(self, wp_url, output_dir="src/content"):
        self.wp_url = wp_url.rstrip('/')
        self.api_url = f"{self.wp_url}/wp-json/wp/v2"
        self.output_dir = output_dir
        self.images_dir = "public/images"
        self.pages_dir = "src/pages"
        
        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/posts", exist_ok=True)
        os.makedirs(f"{self.output_dir}/pages", exist_ok=True)
        
    def fetch_posts(self, per_page=100):
        """Fetch all posts from WordPress API"""
        print("📝 Fetching posts...")
        posts = []
        page = 1
        
        while True:
            url = f"{self.api_url}/posts"
            params = {
                'per_page': per_page,
                'page': page,
                'status': 'publish',
                '_embed': 'true'
            }
            
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"❌ Error fetching posts: {response.status_code}")
                break
                
            data = response.json()
            if not data:
                break
                
            posts.extend(data)
            page += 1
            print(f"   Fetched {len(posts)} posts so far...")
            
        return posts
    
    def fetch_pages(self, per_page=100):
        """Fetch all pages from WordPress API"""
        print("📄 Fetching pages...")
        pages = []
        page = 1
        
        while True:
            url = f"{self.api_url}/pages"
            params = {
                'per_page': per_page,
                'page': page,
                'status': 'publish',
                '_embed': 'true'
            }
            
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"❌ Error fetching pages: {response.status_code}")
                break
                
            data = response.json()
            if not data:
                break
                
            pages.extend(data)
            page += 1
            print(f"   Fetched {len(pages)} pages so far...")
            
        return pages
    
    def fetch_media(self, media_id):
        """Fetch media details from WordPress API"""
        url = f"{self.api_url}/media/{media_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    
    def download_image(self, image_url, filename):
        """Download and save image"""
        try:
            response = requests.get(image_url)
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
    
    def process_content(self, content):
        """Process WordPress content for Astro"""
        if not content:
            return ""
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Process images
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # Download image and update src
                filename = f"wp_{slugify(src.split('/')[-1])}"
                new_src = self.download_image(src, filename)
                img['src'] = new_src
        
        # Process links to other posts/pages
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and self.wp_url in href:
                # Convert WordPress URLs to Astro URLs
                # This is a basic implementation - you might want to customize this
                link['href'] = href.replace(self.wp_url, '')
        
        return str(soup)
    
    def convert_post_to_astro(self, post):
        """Convert WordPress post to Astro format"""
        # Extract post data
        title = post.get('title', {}).get('rendered', '') if isinstance(post.get('title'), dict) else str(post.get('title', ''))
        content = post.get('content', {}).get('rendered', '') if isinstance(post.get('content'), dict) else str(post.get('content', ''))
        excerpt = post.get('excerpt', {}).get('rendered', '') if isinstance(post.get('excerpt'), dict) else str(post.get('excerpt', ''))
        date = post.get('date', '')
        slug = post.get('slug', '')
        
        # Process content
        processed_content = self.process_content(content)
        
        # Handle categories safely
        categories = post.get('categories', [])
        if isinstance(categories, list):
            # If categories are just IDs, we'll need to fetch them separately
            category_names = []
            for cat in categories:
                if isinstance(cat, dict):
                    category_names.append(cat.get('name', ''))
                else:
                    # It's just an ID, we'll skip for now
                    pass
        else:
            category_names = []
        
        # Create frontmatter
        frontmatter = {
            'title': title,
            'description': BeautifulSoup(excerpt, 'html.parser').get_text().strip() if excerpt else '',
            'pubDate': date,
            'author': post.get('_embedded', {}).get('author', [{}])[0].get('name', '') if post.get('_embedded', {}).get('author') else '',
            'tags': category_names,
            'draft': post.get('status') != 'publish'
        }
        
        # Create Astro content
        astro_content = "---\n"
        for key, value in frontmatter.items():
            if isinstance(value, list):
                astro_content += f"{key}:\n"
                for item in value:
                    astro_content += f"  - {item}\n"
            else:
                astro_content += f"{key}: {json.dumps(value)}\n"
        astro_content += "---\n\n"
        astro_content += processed_content
        
        # Save file
        filename = f"{slug}.md" if slug else f"post-{post.get('id', 'unknown')}.md"
        filepath = os.path.join(self.output_dir, 'posts', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(astro_content)
        
        return filepath
    
    def convert_page_to_astro(self, page):
        """Convert WordPress page to Astro format"""
        # Extract page data
        title = page.get('title', {}).get('rendered', '') if isinstance(page.get('title'), dict) else str(page.get('title', ''))
        content = page.get('content', {}).get('rendered', '') if isinstance(page.get('content'), dict) else str(page.get('content', ''))
        slug = page.get('slug', '')
        
        # Process content
        processed_content = self.process_content(content)
        
        # Create frontmatter
        frontmatter = {
            'title': title,
            'description': '',
            'draft': page.get('status') != 'publish'
        }
        
        # Create Astro content
        astro_content = "---\n"
        for key, value in frontmatter.items():
            astro_content += f"{key}: {json.dumps(value)}\n"
        astro_content += "---\n\n"
        astro_content += processed_content
        
        # Save file
        filename = f"{slug}.md" if slug else f"page-{page.get('id', 'unknown')}.md"
        filepath = os.path.join(self.output_dir, 'pages', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(astro_content)
        
        return filepath
    
    def create_astro_pages(self, pages):
        """Create Astro page files for WordPress pages"""
        print("📄 Creating Astro pages...")
        
        for page in pages:
            slug = page.get('slug', '')
            if not slug:
                continue
                
            # Get page data safely
            title = page.get('title', {}).get('rendered', '') if isinstance(page.get('title'), dict) else str(page.get('title', ''))
            content = page.get('content', {}).get('rendered', '') if isinstance(page.get('content'), dict) else str(page.get('content', ''))
            
            # Create page file
            page_content = f"""---
title: {title}
description: ''
---

<Layout>
  <div class="prose max-w-none">
    <h1>{title}</h1>
    <div set:html={content} />
  </div>
</Layout>
"""
            
            # Handle special pages
            if slug == 'home':
                filepath = os.path.join(self.pages_dir, 'index.astro')
            else:
                filepath = os.path.join(self.pages_dir, f"{slug}.astro")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page_content)
            
            print(f"   Created: {filepath}")
    
    def run_conversion(self):
        """Run the complete conversion process"""
        print("🚀 Starting WordPress to Astro conversion...")
        print(f"WordPress URL: {self.wp_url}")
        print(f"Output directory: {self.output_dir}")
        
        # Fetch content
        posts = self.fetch_posts()
        pages = self.fetch_pages()
        
        print(f"\n📊 Found {len(posts)} posts and {len(pages)} pages")
        
        # Convert posts
        print("\n📝 Converting posts...")
        for i, post in enumerate(posts, 1):
            filepath = self.convert_post_to_astro(post)
            print(f"   [{i}/{len(posts)}] {filepath}")
        
        # Convert pages
        print("\n📄 Converting pages...")
        for i, page in enumerate(pages, 1):
            filepath = self.convert_page_to_astro(page)
            print(f"   [{i}/{len(pages)}] {filepath}")
        
        # Create Astro page files
        self.create_astro_pages(pages)
        
        print("\n✅ Conversion complete!")
        print(f"\nNext steps:")
        print(f"1. Review the converted content in {self.output_dir}/")
        print(f"2. Check images in {self.images_dir}/")
        print(f"3. Run 'npm run dev' to preview your site")
        print(f"4. Customize the design and content as needed")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 wordpress-converter.py <wordpress_url> [output_dir]")
        print("Example: python3 wordpress-converter.py https://example.com")
        sys.exit(1)
    
    wp_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "src/content"
    
    converter = WordPressToAstroConverter(wp_url, output_dir)
    converter.run_conversion()

if __name__ == "__main__":
    main()
