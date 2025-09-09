#!/bin/bash

# WordPress to Astro Conversion Script
# This script converts a WordPress site to Astro using the REST API

echo "🚀 Starting WordPress to Astro conversion..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if WordPress URL is provided
if [ $# -eq 0 ]; then
    echo "❌ Please provide a WordPress URL"
    echo "Usage: ./convert.sh <wordpress_url> [output_dir]"
    echo "Example: ./convert.sh https://example.com"
    exit 1
fi

# Run the conversion
echo "🔄 Converting WordPress content..."
python3 wordpress-converter.py "$@"

echo "✅ Conversion complete!"
echo ""
echo "Next steps:"
echo "1. Review the converted content in src/content/ and src/pages/"
echo "2. Update images in public/images/"
echo "3. Run 'npm run dev' to preview your site"
echo "4. Customize the design and content as needed"
