import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import * as cheerio from 'cheerio';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function parseArgs(argv) {
  const args = { inDir: 'src/pages/site', outDir: 'src/pages', overwrite: true };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--in' || a === '-i') args.inDir = argv[++i] ?? args.inDir;
    else if (a === '--out' || a === '-o') args.outDir = argv[++i] ?? args.outDir;
    else if (a === '--no-overwrite') args.overwrite = false;
  }
  return args;
}

function listHtmlFiles(dir) {
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

function toAstroPath(inDir, htmlFile, outDir) {
  const rel = path.relative(inDir, path.dirname(htmlFile));
  const destDir = path.join(outDir, rel);
  return path.join(destDir, 'index.astro');
}

function extractMainHtml(html) {
  const $ = cheerio.load(html);
  let content = $('main').html();
  if (!content) {
    content = $('body').html();
  }
  content = content || '';
  return content.trim();
}

function detectOrigin(html) {
  const $ = cheerio.load(html);
  const origins = new Set();
  const collect = (val) => {
    if (!val) return;
    try {
      const u = new URL(val, 'https://example.com');
      if (u.origin && u.protocol.startsWith('http')) origins.add(u.origin);
    } catch {}
  };
  $('a[href], link[href], script[src], img[src]').each((_, el) => {
    collect($(el).attr('href'));
    collect($(el).attr('src'));
  });
  const preferred = [...origins].find((o) => /iowaallpro|republicleadhunter/.test(o));
  return preferred || 'https://iowaallpro2.republicleadhunter.com';
}

function rewriteInternalAnchors(html, origin) {
  const $ = cheerio.load(html, { decodeEntities: false });
  $('a[href]').each((_, el) => {
    const href = $(el).attr('href');
    if (!href) return;
    try {
      const u = new URL(href, origin);
      const base = new URL(origin);
      if (u.origin === base.origin) {
        const p = u.pathname || '/';
        if (/^\/(wp-|wpcontent|wp-content|wp-admin|wp-json)/i.test(p)) return;
        const newHref = p.endsWith('/') ? p : p + '/';
        $(el).attr('href', newHref + (u.search || '') + (u.hash || ''));
      }
    } catch {}
  });
  return $.root().html() || html;
}

function rewriteAssetsToLocal(html, origin) {
  const $ = cheerio.load(html, { decodeEntities: false });
  const toLocal = (urlStr) => {
    try {
      const u = new URL(urlStr, origin);
      const base = new URL(origin);
      if (u.origin !== base.origin) return urlStr;
      return u.pathname + (u.search || '');
    } catch {
      return urlStr;
    }
  };
  $('img[src]').each((_, el) => {
    const v = $(el).attr('src');
    if (v) $(el).attr('src', toLocal(v));
  });
  $('link[rel="stylesheet"]').each((_, el) => {
    const v = $(el).attr('href');
    if (v) $(el).attr('href', toLocal(v));
  });
  $('script[src]').each((_, el) => {
    const v = $(el).attr('src');
    if (v) $(el).attr('src', toLocal(v));
  });
  return $.root().html() || html;
}

function extractHeadStyles(html, baseUrl) {
  const $ = cheerio.load(html);
  const hrefs = [];
  $('link[rel="stylesheet"]').each((_, el) => {
    const href = $(el).attr('href');
    if (!href) return;
    try {
      const u = new URL(href, baseUrl);
      hrefs.push(u.toString());
    } catch {
      // ignore malformed
    }
  });
  return hrefs;
}

function wrapInLayout(title, contentHtml) {
  return `---
import Layout from '../../layouts/Layout.astro';
---

<Layout title={"${title}"}>
  <main>
${indentHtml(contentHtml, 4)}
  </main>
</Layout>
`;
}

function indentHtml(html, spaces) {
  const pad = ' '.repeat(spaces);
  return html
    .split('\n')
    .map((line) => (line.trim().length ? pad + line : ''))
    .join('\n');
}

function sanitizeTitle(str) {
  return (str || '').replace(/\s+/g, ' ').replace(/"/g, '\"').trim();
}

function ensureDirFor(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function wrapInLayoutDynamic(fromFile, title, contentHtml, headStyles) {
  const fromDir = path.dirname(fromFile);
  const layoutAbs = path.join(process.cwd(), 'src', 'layouts', 'Layout.astro');
  let layoutImport = path.relative(fromDir, layoutAbs);
  layoutImport = layoutImport.split(path.sep).join('/');
  if (!layoutImport.startsWith('.')) layoutImport = './' + layoutImport;
  const contentSerialized = JSON.stringify(contentHtml);
  const stylesSerialized = JSON.stringify(headStyles || []);
  return `---
import Layout from '${layoutImport}';
const contentHtml = ${contentSerialized};
const headStyles = ${stylesSerialized};
---

<Layout title={"${title}">
  <Fragment slot="head">
    {headStyles.map((href) => (<link rel="stylesheet" href={href} />))}
  </Fragment>
  <main set:html={contentHtml} />
</Layout>
`;
}

function generatePages(inDir, outDir, overwrite) {
  const files = listHtmlFiles(inDir);
  let count = 0;
  for (const file of files) {
    const html = fs.readFileSync(file, 'utf8');
    const $ = cheerio.load(html);
    const title = sanitizeTitle($('title').first().text() || 'Page');
    const origin = detectOrigin(html);
    // Extract head styles and rewrite to local
    const headStylesAbs = extractHeadStyles(html, origin);
    const headStylesLocal = headStylesAbs.map((u) => {
      try {
        const uu = new URL(u);
        if (uu.origin === new URL(origin).origin) return uu.pathname + (uu.search || '');
        return u;
      } catch { return u; }
    });
    // Extract and rewrite main content assets and anchors
    const mainRaw = extractMainHtml(html);
    const mainWithLocalAssets = rewriteAssetsToLocal(mainRaw, origin);
    const mainHtml = rewriteInternalAnchors(mainWithLocalAssets, origin);
    const dest = toAstroPath(inDir, file, outDir);
    ensureDirFor(dest);
    if (!overwrite && fs.existsSync(dest)) {
      console.log(`Skip existing ${dest}`);
    } else {
      const astro = wrapInLayoutDynamic(dest, title, mainHtml, headStylesLocal);
      fs.writeFileSync(dest, astro, 'utf8');
      console.log(`Wrote ${dest}`);
    }
    count++;
  }
  console.log(`Generated ${count} Astro page(s).`);
}

function main() {
  const args = parseArgs(process.argv);
  const inAbs = path.isAbsolute(args.inDir) ? args.inDir : path.join(process.cwd(), args.inDir);
  const outAbs = path.isAbsolute(args.outDir) ? args.outDir : path.join(process.cwd(), args.outDir);
  generatePages(inAbs, outAbs, args.overwrite);
}

main();


