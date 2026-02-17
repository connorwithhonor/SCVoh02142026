# Bing Webmaster + IndexNow Checklist

Use this to expand visibility beyond Google and speed URL discovery.

## 1) Add Site in Bing Webmaster Tools

- Go to Bing Webmaster Tools.
- Add property: `https://santaclaritaopenhouses.com`
- Verify ownership (recommended: import from Google Search Console if available).

## 2) Submit Sitemap in Bing

- In Bing Webmaster, open **Sitemaps**.
- Submit:
  - `https://santaclaritaopenhouses.com/sitemap-index.xml`

## 3) Verify robots + sitemap access

- Check these URLs in browser:
  - `https://santaclaritaopenhouses.com/robots.txt`
  - `https://santaclaritaopenhouses.com/sitemap-index.xml`
- Confirm both return 200.

## 4) IndexNow Key (Implemented)

- Key file path on your site:
  - `https://santaclaritaopenhouses.com/7c13072f5d5a4a4b89e7b3550054f246.txt`
- This key is used by your local submit script.

## 5) Submit URLs with IndexNow

After deploys or major content updates, run:

- `npm run indexnow:submit`

This script:
- Reads your sitemap index
- Expands child sitemaps
- Submits URL batches to IndexNow API

You can also submit specific URLs only:

- `npm run indexnow:submit -- https://santaclaritaopenhouses.com/ https://santaclaritaopenhouses.com/book`

## 6) Bing Priority URL Inspection

Inspect/index these first:

1. `https://santaclaritaopenhouses.com/`
2. `https://santaclaritaopenhouses.com/blog`
3. `https://santaclaritaopenhouses.com/about`
4. `https://santaclaritaopenhouses.com/book`
5. Recent blog post URLs

## 7) Monthly Bing SEO Health Review

Track:
- Indexed pages trend
- Crawl issues
- Search clicks/impressions
- Top queries and pages

If indexed count stalls while sitemap is healthy, submit a focused batch via IndexNow for newly published URLs.
