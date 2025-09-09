#!/usr/bin/env node

/**
 * Test script for WordPress conversion
 * This script tests the conversion system with a sample WordPress site
 */

import WordPressConverter from './src/scripts/wordpress-converter.js';

async function testConversion() {
  console.log('🧪 Testing WordPress conversion system...');
  
  // Test with a public WordPress site (WordPress.com demo site)
  const testUrl = 'https://demo.wp-api.org';
  
  console.log(`Testing with: ${testUrl}`);
  
  const converter = new WordPressConverter();
  
  try {
    // Test the conversion
    await converter.processWordPressSite(testUrl, 'test-output');
    
    console.log('✅ Test completed successfully!');
    console.log('Check the test-output directory for converted content.');
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    
    // Provide helpful error information
    if (error.message.includes('python3')) {
      console.log('\n💡 Make sure Python 3 is installed and accessible');
    } else if (error.message.includes('requests')) {
      console.log('\n💡 Make sure to install Python dependencies: pip3 install -r requirements.txt');
    } else if (error.message.includes('ENOENT')) {
      console.log('\n💡 Make sure the wordpress-converter.py file exists');
    }
  }
}

// Run the test
testConversion().catch(console.error);
