# Search Console Fast-Track Checklist

Use this after the latest deploy to confirm indexing health and maximize discoverability.

## 1) Confirm Property + Canonical Domain

- In Google Search Console, make sure your primary property is:
  - https://santaclaritaopenhouses.com
- If you use Domain Property, confirm all protocols/subdomains are covered.

## 2) Submit Sitemap

- Go to: **Indexing → Sitemaps**
- Submit:
  - `https://santaclaritaopenhouses.com/sitemap-index.xml`
- Expected result: **Success** (not “Couldn’t fetch”).

## 3) URL Inspection Priority (Request Indexing)

Inspect these first, then click **Request Indexing** if needed:

1. `https://santaclaritaopenhouses.com/`
2. `https://santaclaritaopenhouses.com/blog`
3. `https://santaclaritaopenhouses.com/about`
4. `https://santaclaritaopenhouses.com/book`
5. 5–10 recent/high-value blog URLs

For each URL, verify:
- URL is on Google (or requested)
- **Canonical** is self-referencing and uses `santaclaritaopenhouses.com`
- Crawled successfully
- Page fetch allowed

## 4) Index Coverage Checks

Go to: **Indexing → Pages**

Review and reduce these buckets over time:
- **Duplicate without user-selected canonical**
- **Crawled - currently not indexed**
- **Discovered - currently not indexed**
- **Soft 404**

Action rule:
- If an important URL is excluded, inspect it and request indexing.
- If a URL should not rank, leave it excluded intentionally.

## 5) Enhancements / Rich Results Signals

Go to: **Enhancements** and **URL Inspection → View crawled page**

Check for:
- Structured data detected on blog posts
- No major parse errors in schema

Note: not every schema type creates a visible rich result. Clean validation still helps understanding and relevance.

## 6) Performance Baseline (Day 0)

Go to: **Performance → Search results**

Save baseline for:
- Total clicks
- Total impressions
- Average CTR
- Average position

Create filters for key pages:
- `/`
- `/blog`
- `/about`
- `/book`

## 7) Re-check Cadence

- **48 hours post-deploy:** verify sitemap + core pages indexed/crawlable
- **7 days:** review coverage movements and query impressions
- **28 days:** compare baseline trend (impressions, CTR, position)

## 8) Optional High-Impact Next Steps

- Add/verify Bing Webmaster Tools with same sitemap
- Connect GA4 + Search Console for landing-page query mapping
- Build internal links from top-traffic blog posts to `/book` and `/about`

---

## Current Site Technical SEO (Already Implemented)

- Canonical site domain set to `https://santaclaritaopenhouses.com`
- Robots file exists at `/robots.txt`
- Sitemap integration enabled (`/sitemap-index.xml`)
- Global metadata + canonical tags configured
- Global + page-level JSON-LD added on core pages
- Malformed absolute blog URLs cleaned

If any page still appears as not indexed after inspection + request, give it 3–10 days before escalating unless there is a clear crawl/render error.
