import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function parseArgs(argv) {
  const args = { from: 'src/pages/site', base: '', out: 'public' };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--from' || a === '-f') args.from = argv[++i] ?? args.from;
    else if (a === '--base' || a === '-b') args.base = argv[++i] ?? args.base;
    else if (a === '--out' || a === '-o') args.out = argv[++i] ?? args.out;
  }
  if (!args.base) {
    console.error('Usage: node src/scripts/mirror-assets.js --from src/pages/site --base https://site --out public');
    process.exit(1);
  }
  args.base = args.base.replace(/\/$/, '');
  return args;
}

function walkHtmlFiles(dir) {
  const files = [];
  function walk(current) {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile() && entry.name === 'index.html') files.push(full);
    }
  }
  if (fs.existsSync(dir)) walk(dir);
  return files;
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

async function fetchText(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return await res.text();
}

async function fetchBinary(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  const buf = Buffer.from(await res.arrayBuffer());
  return buf;
}

function extractAssetUrlsFromHtml(html, base) {
  const urls = new Set();
  const add = (u) => {
    try {
      const abs = new URL(u, base);
      urls.add(abs.toString());
    } catch {}
  };
  // Simple regex extraction to avoid cheerio dependency here
  for (const m of html.matchAll(/<link[^>]+href=["']([^"']+)["']/gi)) add(m[1]);
  for (const m of html.matchAll(/<script[^>]+src=["']([^"']+)["']/gi)) add(m[1]);
  for (const m of html.matchAll(/<img[^>]+src=["']([^"']+)["']/gi)) add(m[1]);
  return [...urls];
}

function isFromOrigin(u, origin) {
  try {
    const a = new URL(u);
    return a.origin === origin;
  } catch {
    return false;
  }
}

function toLocalPath(outRoot, urlStr) {
  const u = new URL(urlStr);
  let p = u.pathname;
  if (p.startsWith('/')) p = p.slice(1);
  return path.join(outRoot, p);
}

function findCssUrls(cssText, cssUrl) {
  const urls = new Set();
  const re = /url\(([^)]+)\)/g;
  let m;
  while ((m = re.exec(cssText))) {
    let raw = m[1].trim().replace(/^['"]|['"]$/g, '');
    if (!raw || raw.startsWith('data:')) continue;
    try {
      const abs = new URL(raw, cssUrl);
      urls.add(abs.toString());
    } catch {}
  }
  return [...urls];
}

async function main() {
  const args = parseArgs(process.argv);
  const baseOrigin = new URL(args.base).origin;
  const inAbs = path.isAbsolute(args.from) ? args.from : path.join(process.cwd(), args.from);
  const outAbs = path.isAbsolute(args.out) ? args.out : path.join(process.cwd(), args.out);
  fs.mkdirSync(outAbs, { recursive: true });

  const htmlFiles = walkHtmlFiles(inAbs);
  const toDownload = new Set();

  // Collect asset URLs from HTML
  for (const file of htmlFiles) {
    const html = fs.readFileSync(file, 'utf8');
    for (const u of extractAssetUrlsFromHtml(html, args.base)) {
      if (isFromOrigin(u, baseOrigin)) toDownload.add(u);
    }
  }

  // Download assets, expand CSS dependencies
  const visited = new Set();
  const queue = [...toDownload];
  while (queue.length) {
    const url = queue.shift();
    if (visited.has(url)) continue;
    visited.add(url);
    const dest = toLocalPath(outAbs, url);
    ensureDir(dest);
    try {
      if (/\.css(\?|$)/i.test(url)) {
        const css = await fetchText(url);
        fs.writeFileSync(dest, css, 'utf8');
        // Find url() refs and enqueue those from same origin
        for (const ref of findCssUrls(css, url)) {
          if (isFromOrigin(ref, baseOrigin)) queue.push(ref);
        }
        console.log(`CSS  → ${dest}`);
      } else {
        const buf = await fetchBinary(url);
        fs.writeFileSync(dest, buf);
        console.log(`ASSET→ ${dest}`);
      }
    } catch (e) {
      console.warn(`Skip ${url}: ${e.message}`);
    }
  }

  console.log(`Mirrored ${visited.size} asset(s) to ${outAbs}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});


