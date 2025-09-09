import fs from 'fs';
import path from 'path';
import * as cheerio from 'cheerio';
import TurndownService from 'turndown';
import { execSync } from 'child_process';

/**
 * WordPress to Astro Content Converter
 * 
 * This script helps convert WordPress content to Astro-compatible format
 * Uses the Python converter for full WordPress REST API integration
 */

class WordPressConverter {
  constructor() {
    this.turndownService = new TurndownService({
      headingStyle: 'atx',
      bulletListMarker: '-',
      codeBlockStyle: 'fenced'
    });
  }

  /**
   * Convert WordPress HTML content to Markdown
   * @param {string} htmlContent - WordPress HTML content
   * @returns {string} - Markdown content
   */
  convertHtmlToMarkdown(htmlContent) {
    if (!htmlContent) return '';
    
    // Clean up WordPress-specific HTML
    const $ = cheerio.load(htmlContent);
    
    // Remove WordPress-specific classes and attributes
    $('*').removeAttr('class').removeAttr('id').removeAttr('style');
    
    // Convert to markdown
    return this.turndownService.turndown($.html());
  }

  /**
   * Extract images from WordPress content and prepare for Astro
   * @param {string} htmlContent - WordPress HTML content
   * @returns {Array} - Array of image objects with src, alt, etc.
   */
  extractImages(htmlContent) {
    if (!htmlContent) return [];
    
    const $ = cheerio.load(htmlContent);
    const images = [];
    
    $('img').each((i, el) => {
      const $img = $(el);
      images.push({
        src: $img.attr('src'),
        alt: $img.attr('alt') || '',
        title: $img.attr('title') || '',
        width: $img.attr('width'),
        height: $img.attr('height')
      });
    });
    
    return images;
  }

  /**
   * Convert WordPress post data to Astro frontmatter
   * @param {Object} wpPost - WordPress post object
   * @returns {Object} - Astro frontmatter object
   */
  convertPostToFrontmatter(wpPost) {
    return {
      title: wpPost.title || '',
      description: wpPost.excerpt || '',
      pubDate: wpPost.date || new Date().toISOString(),
      author: wpPost.author || '',
      tags: wpPost.categories || [],
      draft: wpPost.status !== 'publish'
    };
  }

  /**
   * Run the Python WordPress converter
   * @param {string} wpUrl - WordPress site URL
   * @param {string} outputDir - Output directory for converted content
   */
  async runPythonConverter(wpUrl, outputDir = 'src/content') {
    try {
      console.log(`🚀 Running Python WordPress converter...`);
      console.log(`WordPress URL: ${wpUrl}`);
      console.log(`Output directory: ${outputDir}`);
      
      // Run the Python converter
      const command = `python3 wordpress-converter.py "${wpUrl}" "${outputDir}"`;
      execSync(command, { stdio: 'inherit' });
      
      console.log('✅ Python conversion completed successfully!');
      
    } catch (error) {
      console.error('❌ Error running Python converter:', error.message);
      throw error;
    }
  }

  /**
   * Process WordPress site using REST API
   * @param {string} wpUrl - WordPress site URL
   * @param {string} outputDir - Output directory for converted content
   */
  async processWordPressSite(wpUrl, outputDir = 'src/content') {
    try {
      console.log(`Processing WordPress site: ${wpUrl}`);
      
      // Use the Python converter for full REST API integration
      await this.runPythonConverter(wpUrl, outputDir);
      
      console.log(`Output directory: ${outputDir}`);
      console.log('WordPress site processing completed!');
      
    } catch (error) {
      console.error('Error processing WordPress site:', error);
    }
  }
}

export default WordPressConverter;
