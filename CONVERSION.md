# WordPress to Astro Conversion Guide

This project includes a comprehensive WordPress to Astro conversion system that uses the WordPress REST API to fetch and convert content.

## Features

- ✅ Fetches posts and pages via WordPress REST API
- ✅ Downloads and processes images
- ✅ Converts WordPress content to Astro-compatible format
- ✅ Creates proper frontmatter for posts and pages
- ✅ Generates Astro page files for WordPress pages
- ✅ Handles categories, tags, and metadata
- ✅ Preserves content structure and formatting

## Prerequisites

- Python 3.6 or higher
- Node.js and npm
- Access to a WordPress site with REST API enabled

## Quick Start

### Method 1: Using the Bash Script (Recommended)

```bash
# Make the script executable (if not already done)
chmod +x convert.sh

# Run the conversion
./convert.sh https://your-wordpress-site.com
```

### Method 2: Using Python Directly

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run the converter
python3 wordpress-converter.py https://your-wordpress-site.com
```

### Method 3: Using Node.js

```bash
# Run the Node.js wrapper
npm run convert https://your-wordpress-site.com
```

## Usage Examples

### Basic Conversion
```bash
./convert.sh https://example.com
```

### Custom Output Directory
```bash
./convert.sh https://example.com custom-output-dir
```

### Using Python Directly
```bash
python3 wordpress-converter.py https://example.com src/content
```

## Output Structure

After conversion, your project will have:

```
src/
├── content/
│   ├── posts/           # Converted blog posts
│   └── pages/           # Converted pages
├── pages/               # Astro page files
└── scripts/             # Conversion scripts

public/
└── images/              # Downloaded images
```

## Configuration

### WordPress REST API Requirements

The WordPress site must have:
- REST API enabled (default in WordPress 4.7+)
- Public access to posts and pages
- Media files accessible via URL

### Customizing the Conversion

You can modify the Python script (`wordpress-converter.py`) to:
- Change the output format
- Add custom field processing
- Modify image handling
- Customize frontmatter generation

## Troubleshooting

### Common Issues

1. **Python not found**
   ```bash
   # Install Python 3
   sudo apt-get install python3 python3-pip  # Ubuntu/Debian
   brew install python3                       # macOS
   ```

2. **Permission denied**
   ```bash
   chmod +x convert.sh
   ```

3. **WordPress API not accessible**
   - Check if the site URL is correct
   - Ensure REST API is enabled
   - Verify the site is publicly accessible

4. **Image download fails**
   - Check if images are publicly accessible
   - Verify image URLs are correct
   - Check network connectivity

### Debug Mode

To see detailed output during conversion:

```bash
python3 wordpress-converter.py https://example.com 2>&1 | tee conversion.log
```

## Advanced Usage

### Custom Image Processing

The converter automatically downloads images and updates references. You can customize this behavior in the `download_image` method.

### Custom Content Processing

Modify the `process_content` method to add custom HTML processing, link rewriting, or content transformations.

### Custom Frontmatter

Update the `convert_post_to_frontmatter` and `convert_page_to_astro` methods to customize the generated frontmatter.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your WordPress site is accessible
3. Check the conversion logs for error messages
4. Ensure all dependencies are installed correctly

## License

This conversion system is part of your Astro project and follows the same license terms.
