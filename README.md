# Iowa All Pro - WordPress to Astro Conversion

This project converts an Oxygen/WordPress website to a modern Astro static site.

## 🚀 Project Structure

```
/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable Astro components
│   ├── layouts/           # Page layouts
│   ├── pages/             # Astro pages (file-based routing)
│   ├── scripts/           # Conversion utilities
│   ├── styles/            # Global styles
│   └── data/              # Static data files
├── wordpress-export/      # WordPress export files
├── astro.config.mjs       # Astro configuration
└── package.json
```

## 🛠️ Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

## 📦 WordPress Conversion Process

### Step 1: Export WordPress Content
- Export your WordPress site using the built-in export tool
- Place the export file in the `wordpress-export/` directory

### Step 2: Convert Content
- Use the conversion scripts in `src/scripts/` to process WordPress content
- Convert HTML to Markdown and extract assets

### Step 3: Migrate Assets
- Copy images and media files to the `public/` directory
- Update image references in converted content

### Step 4: Build Astro Site
- Create Astro pages and components
- Implement responsive design with Tailwind CSS
- Test and optimize performance

## 🧞 Available Commands

| Command                | Action                                           |
| :--------------------- | :----------------------------------------------- |
| `npm install`          | Installs dependencies                            |
| `npm run dev`          | Starts local dev server at `localhost:4321`      |
| `npm run build`        | Build your production site to `./dist/`          |
| `npm run preview`      | Preview your build locally, before deploying     |
| `npm run astro ...`    | Run CLI commands like `astro add`, `astro check` |

## 🎨 Technologies Used

- **Astro** - Static site generator
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type safety
- **Cheerio** - HTML parsing for WordPress content
- **Turndown** - HTML to Markdown conversion

## 📝 Next Steps

1. Export your WordPress site
2. Run conversion scripts
3. Customize the design and layout
4. Deploy to your hosting platform

## 👀 Resources

- [Astro Documentation](https://docs.astro.build)
- [Tailwind CSS](https://tailwindcss.com)
- [WordPress Export Guide](https://wordpress.org/support/article/tools-export-screen/)