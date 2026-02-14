# 🚀 Run This to Scrape Seller Content

## Quick Instructions

**1. Install dependencies** (one time):
```bash
pip install -r requirements.txt
```

**2. Scrape seller-relevant blog posts**:
```bash
python scrape_sitemap.py
```

This will:
- ✅ Read https://www.santaclaritaopenhouses.com/sitemap.xml
- ✅ Scrape only seller-relevant posts (filters by keywords)
- ✅ Convert to Astro markdown format
- ✅ Generate redirect file
- ✅ Save everything to `scraped_content/` directory

**3. Review what was scraped**:
```bash
cd scraped_content/blog
ls  # See all .md files
```

**4. Copy to your Astro project**:
```bash
# From migration directory
cp scraped_content/blog/*.md "../src/content/blog/"
cp scraped_content/_redirects "../public/"
```

**5. Test locally**:
```bash
cd ..
npm run dev
```

Visit: http://localhost:4321/blog

**6. Deploy**:
```bash
git add .
git commit -m "feat: Migrate seller-focused blog posts"
git push
```

Netlify auto-deploys!

---

## What Gets Scraped?

The scraper looks for these **seller keywords**:
- sell, selling, seller
- list, listing, agent
- market, price, pricing, value
- commission, negotiate
- tips, guide, how to
- prepare, staging, repair
- City names (Castaic, Canyon Country, etc.)

**It automatically skips:**
- Buyer-focused content
- General news
- Irrelevant pages

---

## Expected Results

You should get **10-50 seller-focused blog posts** (depending on your old site).

Each will be:
- ✅ Converted to markdown
- ✅ Has proper frontmatter (title, description, date, heroImage)
- ✅ Mapped to `/blog/slug-name` URL
- ✅ Has 301 redirect from old URL

---

## If Nothing Gets Scraped

The scraper might be too strict. Edit `scrape_sitemap.py` line 24-32 to add more keywords:

```python
self.seller_keywords = [
    'sell', 'selling', 'seller',
    # ... add your keywords here
]
```

---

## Time Required

- **Scraping:** 5-10 minutes (depending on # of posts)
- **Review:** 10 minutes
- **Copy files:** 1 minute
- **Test:** 5 minutes
- **Deploy:** 2 minutes

**Total: ~25 minutes** 🚀

---

## After This

1. ✅ Old seller content migrated
2. ✅ Redirects in place
3. ✅ Ready for DNS cutover
4. ⏭️ Next: Set up n8n automation (see `N8N_SELF_HOSTED_SETUP.md`)

**You're almost there!**
