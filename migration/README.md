# Site Migration Tool - SantaClaritaOpenHouses.com

This tool scrapes your existing SantaClaritaOpenHouses.com website and converts all pages to Astro markdown format for seamless migration.

## Quick Start

### 1. Install Python Dependencies

```bash
cd "G:\Santa Clarita Open Houses Code 02142026\migration"
pip install -r requirements.txt
```

### 2. Run the Scraper

```bash
python scraper.py
```

**It will ask you:**
- Current site URL (default: https://santaclaritaopenhouses.com)
- Maximum pages to scrape (default: 100)

### 3. Review the Results

The scraper creates a `scraped_content/` directory with:

```
scraped_content/
├── blog/                 # All pages as markdown files
│   ├── home.md
│   ├── about.md
│   ├── contact.md
│   └── ... (all other pages)
├── _redirects            # Netlify redirect file (301s)
└── metadata.json         # Crawl metadata for reference
```

### 4. Migrate the Content

**Copy markdown files to your Astro project:**

```bash
# Copy all blog posts
cp scraped_content/blog/*.md "../src/content/blog/"

# Copy redirects file
cp scraped_content/_redirects "../public/"
```

### 5. Test Locally

```bash
cd "G:\Santa Clarita Open Houses Code 02142026"
npm run dev
```

Visit http://localhost:4321/blog to see your migrated posts

### 6. Deploy to Netlify

```bash
git add .
git commit -m "feat: Migrate content from old site"
git push
```

Netlify will automatically deploy. All old URLs will redirect via `_redirects` file.

---

## What the Scraper Does

### Content Extraction
- Extracts page title and meta description
- Grabs main content (tries article, main, .content, #content, body)
- Removes scripts, styles, nav, header, footer, sidebars, comments
- Cleans up excessive whitespace

### Markdown Conversion
- Creates Astro frontmatter with title, description, pubDate
- Adds default heroImage (your Santa Clarita home photo)
- Sets neighborhood to "Santa Clarita"
- Preserves all text content

### URL Mapping
- Generates clean slugs from URLs
- Creates `_redirects` file with 301 redirects
- Example: `/old-page.html` → `/blog/old-page` (301)

### Smart Crawling
- Only follows internal links (stays on your domain)
- Avoids duplicate pages
- Skips anchors, mailto, tel, javascript links
- Respects max page limit

---

## Advanced Usage

### Custom Starting Point

If you want to scrape only blog posts:

```python
scraper = SiteScraper("https://santaclaritaopenhouses.com")
scraper.crawl(start_url="https://santaclaritaopenhouses.com/blog", max_pages=50)
```

### Increase Max Pages

If you have more than 100 pages:

```bash
python scraper.py
# When prompted, enter: 500
```

### Manual URL List

Create `urls.txt` with specific URLs to scrape:

```
https://santaclaritaopenhouses.com/important-page-1
https://santaclaritaopenhouses.com/important-page-2
```

Then modify `scraper.py` to read from file.

---

## Troubleshooting

### "No content found"
Some pages might not use standard HTML structure. Check `metadata.json` to see which pages were scraped.

### "Too many pages"
Reduce max_pages or add filtering logic to `is_valid_url()` method.

### "Missing images"
Images remain on old host. Either:
1. Keep them there (URLs will still work)
2. Download and re-upload to your GoHighLevel account
3. Add image scraping to the script

### "Broken redirects"
Check `_redirects` file format. Each line should be:
```
/old-path    /new-path    301
```

---

## SEO Preservation

This migration strategy preserves SEO by:

1. **301 Redirects**: All old URLs redirect to new URLs
2. **Same titles/descriptions**: Meta data preserved
3. **Content preservation**: All text content migrated
4. **URL structure**: Clean, SEO-friendly slugs
5. **Fast deployment**: Minimize downtime

Google will see the 301s and transfer ranking signals within 2-4 weeks.

---

## Timeline

**Phase 1: Scrape (30 minutes)**
- Run scraper script
- Review scraped content
- Fix any issues

**Phase 2: Test (1 hour)**
- Copy files to Astro project
- Test locally
- Verify all pages render correctly

**Phase 3: Deploy (15 minutes)**
- Push to GitHub
- Netlify auto-deploys
- Test redirects

**Phase 4: DNS Cutover (5 minutes)**
- Point santaclaritaopenhouses.com to Netlify
- Old hosting provider can be cancelled

**Total: ~2 hours for complete migration**

---

## After Migration

1. **Submit new sitemap** to Google Search Console
2. **Monitor Search Console** for crawl errors
3. **Check Google Analytics** for traffic patterns
4. **Fix any broken redirects** within first week
5. **Rankings transfer** in 2-4 weeks

---

## Support

If you encounter issues:
1. Check `metadata.json` to see what was scraped
2. Review individual `.md` files in `scraped_content/blog/`
3. Test redirects in browser developer tools (Network tab)
4. Manually edit any problematic pages

---

**Ready to migrate? Run `python scraper.py` and let's preserve those rankings!** 🚀
