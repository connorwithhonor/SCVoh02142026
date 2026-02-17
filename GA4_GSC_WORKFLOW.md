# GA4 + Search Console Workflow (SEO Revenue Focus)

Use this workflow to connect ranking movement to lead intent and conversion actions.

## 1) Ensure Properties Are Connected

- In GA4: **Admin → Product Links → Search Console Links**
- Link Search Console property for:
  - `https://santaclaritaopenhouses.com`

## 2) Confirm Core Events in GA4

Track at minimum:
- `page_view`
- click-to-call events (`tel:` click)
- outbound booking click (`/book` or embedded scheduler interactions)
- form submission events (if available)

## 3) Build SEO Landing Page Report

In GA4 Explore or Looker Studio, include:
- Landing page
- Organic users
- Engaged sessions
- Event count (calls, booking clicks, submits)

Priority pages:
- `/`
- `/blog`
- `/about`
- `/book`

## 4) Build Query-to-Page View (Search Console)

In Search Console, monitor:
- Queries driving impressions
- Page-level CTR and average position
- Query/page mismatches (high impressions, low CTR)

Action trigger:
- High impressions + low CTR → improve title/description and on-page promise clarity.
- Good CTR + low conversions → improve CTA and internal links to `/book`.

## 5) Weekly SEO Operations Rhythm

- Monday: check Search Console coverage + indexing anomalies
- Wednesday: review top query shifts + CTR by page
- Friday: review GA4 conversions from organic landing pages

## 6) Simple KPI Targets

- Index health: no growth in critical excluded pages
- Visibility: impressions trend up over 28-day windows
- Efficiency: CTR improves on top 20 pages
- Business: more organic click-to-call and booking actions

## 7) Content Decision Rule

When a blog post gets traffic but low conversion contribution:
- Add stronger internal links to `/book` and `/about`
- Add one seller-intent CTA block near end of article
- Re-check 14-day change in organic conversion events
