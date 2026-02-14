# Santa Clarita Open Houses

A production-ready Astro blog for real estate listings in Santa Clarita, CA.

## Tech Stack

- **Framework**: Astro (latest)
- **Styling**: Tailwind CSS v4
- **CMS**: Decap CMS (Git-based)
- **Deployment**: Netlify

## Key Features

### 1. External Image URLs
The CMS is configured to accept external image URLs (not file uploads). This allows you to paste image URLs from GoHighLevel or any other hosting service directly into the "Hero Image URL" field.

### 2. Syndication Warning Component
Every blog post automatically displays a privacy warning at the top, alerting visitors that syndication sites (Zillow, Redfin) collect and sell their data.

### 3. SEO-Optimized with Schema.org
Each blog post includes JSON-LD structured data combining:
- `BlogPosting` schema for blog content
- `RealEstateListing` schema for real estate properties

### 4. Performance Optimized
- Zero JavaScript for content rendering
- Lazy loading images
- Static site generation
- Optimized for Core Web Vitals

## Project Structure

```
/
├── public/
│   └── admin/
│       ├── config.yml       # Decap CMS configuration
│       └── index.html        # CMS admin interface
├── src/
│   ├── components/
│   │   └── SyndicationWarning.astro  # Privacy warning component
│   ├── content/
│   │   └── blog/             # Blog posts (Markdown)
│   ├── layouts/
│   │   └── BlogPost.astro    # Blog post layout with JSON-LD
│   └── styles/
│       └── global.css        # Tailwind CSS imports
├── astro.config.mjs
├── netlify.toml
└── package.json
```

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Visit `http://localhost:4321` to see your site.

### Access the CMS

Once deployed to Netlify:

1. Visit `https://your-site.netlify.app/admin`
2. Enable Netlify Identity in your Netlify dashboard
3. Invite yourself as a user
4. Log in and start creating posts

## Using the CMS

### Creating a New Blog Post

1. Navigate to `/admin`
2. Click "New Blog Posts"
3. Fill in the fields:
   - **Title**: Post headline
   - **Publish Date**: Publication date and time
   - **Neighborhood**: Santa Clarita neighborhood name
   - **Hero Image URL**: Paste the full URL to your image (e.g., from GoHighLevel)
   - **Description**: Brief summary for SEO
   - **Body**: Write your post content in Markdown

4. Click "Publish" to commit directly to your repository

### Important: Hero Image URLs

The CMS uses a **string field** for hero images, not file uploads. You must:
- Host images externally (GoHighLevel, Cloudinary, etc.)
- Paste the full URL (e.g., `https://example.com/image.jpg`)
- Ensure the URL is publicly accessible

## Deployment to Netlify

### Manual Deployment

1. Push this repository to GitHub
2. Connect your repository to Netlify
3. Configure build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
4. Enable Netlify Identity
5. Enable Git Gateway in Identity settings

## Environment Configuration

No environment variables are required for basic functionality. All configuration is in:
- `public/admin/config.yml` - CMS settings
- `astro.config.mjs` - Site URL and integrations
- `src/consts.ts` - Site title and description

## Content Schema

Blog posts support these frontmatter fields:

```yaml
---
title: string (required)
description: string (required)
pubDate: date (required)
neighborhood: string (optional)
heroImage: string URL (optional)
updatedDate: date (optional)
---
```

## Commands

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |

## Performance Considerations

- Images are lazy-loaded with `loading="lazy"`
- No JavaScript shipped for blog content
- Static HTML generation for fast page loads
- Minimal CSS with Tailwind v4

## Customization

### Update Site Information

Edit `src/consts.ts`:

```typescript
export const SITE_TITLE = 'Your Title';
export const SITE_DESCRIPTION = 'Your description';
```

### Modify Syndication Warning

Edit `src/components/SyndicationWarning.astro` to change the warning message.

### Adjust Schema.org Data

Edit the `jsonLd` object in `src/layouts/BlogPost.astro` to customize structured data.

## License

MIT
