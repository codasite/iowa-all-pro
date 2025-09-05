import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import * as cheerio from 'cheerio';

// ESM __dirname support
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function parseArgs(argv) {
  const args = { base: '', out: 'src/pages/site', max: 30 };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--base' || a === '-b') args.base = argv[++i] ?? '';
    else if (a === '--out' || a === '-o') args.out = argv[++i] ?? args.out;
    else if (a === '--max' || a === '-m') args.max = Number(argv[++i] ?? args.max);
  }
  if (!args.base) {
    console.error('Usage: node src/scripts/wp-scraper.js --base https://example.com [--out src/pages/site] [--max 50]');
    process.exit(1);
  }
  // Ensure no trailing slash
  args.base = args.base.replace(/\/$/, '');
  return args;
}

function isInternalUrl(url, baseOrigin) {
  try {
    const u = new URL(url, baseOrigin);
    const b = new URL(baseOrigin);
    if (u.origin !== b.origin) return false;
    const p = u.pathname;
    if (p.startsWith('/wp-json') || p.startsWith('/wp-admin') || p.startsWith('/wp-login')) return false;
    if (p.endsWith('.xml') || p.endsWith('.pdf') || p.endsWith('.zip') || p.match(/\.(png|jpe?g|webp|gif|svg|js|css)$/i)) return false;
    return true;
  } catch {
    return false;
  }
}

function toOutPath(baseOrigin, pageUrl, outRoot) {
  const u = new URL(pageUrl, baseOrigin);
  let p = u.pathname;
  if (p.endsWith('/')) p = p.slice(0, -1);
  if (p === '') return path.join(outRoot, 'index.html');
  return path.join(outRoot, p, 'index.html');
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function rewriteAssets($, baseOrigin) {
  const b = new URL(baseOrigin);
  // Make asset URLs absolute to the source origin so they load from the remote server in dev
  $('img').each((_, el) => {
    const src = $(el).attr('src');
    if (!src) return;
    try {
      const u = new URL(src, baseOrigin);
      $(el).attr('src', u.toString());
    } catch {}
  });
  $('link[rel="stylesheet"]').each((_, el) => {
    const href = $(el).attr('href');
    if (!href) return;
    try {
      const u = new URL(href, baseOrigin);
      $(el).attr('href', u.toString());
    } catch {}
  });
  $('script[src]').each((_, el) => {
    const src = $(el).attr('src');
    if (!src) return;
    try {
      const u = new URL(src, baseOrigin);
      $(el).attr('src', u.toString());
    } catch {}
  });
}

async function fetchHtml(url) {
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; SiteScraper/1.0; +https://astro.build)',
      'Accept': 'text/html,application/xhtml+xml'
    }
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return await res.text();
}

async function crawlAndSave({ base, out, max }) {
  const baseUrl = base;
  const origin = new URL(baseUrl).origin;
  const queue = [baseUrl];
  const visited = new Set();
  let count = 0;

  while (queue.length && count < max) {
    const current = queue.shift();
    if (!current || visited.has(current)) continue;
    visited.add(current);
    try {
      console.log(`Fetching: ${current}`);
      const html = await fetchHtml(current);
      const $ = cheerio.load(html);

      // Remove WP admin bar if present
      $('#wpadminbar').remove();

      // Rewrite local assets to /wp-content paths
      rewriteAssets($, origin);

      const outFile = toOutPath(origin, current, out);
      ensureDir(outFile);
      fs.writeFileSync(outFile, $.html(), 'utf8');
      console.log(`Saved → ${outFile}`);
      count++;

      // Discover more internal links
      $('a[href]').each((_, el) => {
        const href = $(el).attr('href');
        if (!href) return;
        try {
          const u = new URL(href, origin);
          const normalized = u.toString().replace(/#.*$/, '');
          if (isInternalUrl(normalized, origin) && !visited.has(normalized)) {
            queue.push(normalized);
          }
        } catch {}
      });
    } catch (err) {
      console.warn(`Skip ${current}: ${err.message}`);
    }
  }

  console.log(`Done. Visited ${count} pages.`);
}

async function main() {
  const args = parseArgs(process.argv);
  const outAbs = path.isAbsolute(args.out) ? args.out : path.join(process.cwd(), args.out);
  fs.mkdirSync(outAbs, { recursive: true });
  await crawlAndSave({ base: args.base, out: outAbs, max: args.max });
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});


