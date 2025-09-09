#!/usr/bin/env node

/**
 * WordPress to Astro Conversion Example
 * 
 * This script demonstrates how to use the WordPress converter
 */

import WordPressConverter from './wordpress-converter.js';

async function main() {
  // Get WordPress URL from command line arguments
  const wpUrl = process.argv[2];
  
  if (!wpUrl) {
    console.log('❌ Please provide a WordPress URL');
    console.log('Usage: npm run convert <wordpress_url>');
    console.log('Example: npm run convert https://example.com');
    process.exit(1);
  }
  
  // Create converter instance
  const converter = new WordPressConverter();
  
  try {
    // Run the conversion
    await converter.processWordPressSite(wpUrl);
    
    console.log('\n🎉 Conversion completed successfully!');
    console.log('\nNext steps:');
    console.log('1. Review the converted content in src/content/');
    console.log('2. Check images in public/images/');
    console.log('3. Run "npm run dev" to preview your site');
    console.log('4. Customize the design and content as needed');
    
  } catch (error) {
    console.error('❌ Conversion failed:', error.message);
    process.exit(1);
  }
}

// Run the main function
main().catch(console.error);
