# Image Migration Guide

## Problem

All 609 blog posts currently reference images hosted on external CDN domains:
- `library-ihouseprd.b-cdn.net` (iHouse template/branding images)
- `idx-acnt-ihouseprd.b-cdn.net` (blog post images you uploaded)
- `santaclaritaopenhouses.com` (old site images)

**When the old site is shut down and/or your iHouse account is closed, these images will break**, leaving all blog posts with broken image links.

## Solution

The `migrate_images.py` script will:
1. Scan all 609 blog post markdown files
2. Find all images hosted on the CDN domains above
3. Download each image to `public/images/blog/[post-name]/[image-filename]`
4. Update the markdown files to reference the new local paths
5. Commit the changes to git

## How to Run

### Prerequisites

Ensure you have Python 3 installed and the `requests` library:

```bash
pip install requests
```

### Run the Migration

```bash
cd "G:\Santa Clarita Open Houses Code 02142026"
python scripts/migrate_images.py
```

### What Happens

The script will:
- Create organized subdirectories for each blog post's images
- Download images (with rate limiting to be nice to the CDN)
- Update markdown files with new image paths
- Show progress for all 609 posts
- Provide a summary of images downloaded and files updated

Example output:
```
[1/609] Processing: valencia-real-estate-market-january-2026-270-homes-53-days-to-sell.md
📥 Downloading: https://idx-acnt-ihouseprd.b-cdn.net/AR1197716/file_manager/valencia-real-estate-2026.webp
✅ Saved to: public/images/blog/valencia-real-estate-market-january-2026/valencia-real-estate-2026.webp
✏️  Updated: valencia-real-estate-market-january-2026-270-homes-53-days-to-sell.md
```

### Estimated Time

- **~609 blog posts** with varying numbers of images
- **Rate limited** to 0.5 seconds between downloads
- **Estimated total time:** 30-60 minutes (depends on total number of images)

## After Migration

### 1. Verify Images

Check a few blog posts locally to ensure images display:

```bash
npm run dev
```

Visit:
- http://localhost:4321/blog/valencia-real-estate-market-january-2026-270-homes-53-days-to-sell
- http://localhost:4321/blog/canyon-country-real-estate-january-2026-225-listings-68-days-inventory-surge
- http://localhost:4321/blog/2024-santa-clarita-real-estate-market-trends-what-buyers-and-sellers-need

### 2. Commit Changes

```bash
git add public/images/blog/ src/content/blog/
git commit -m "Migrate blog images from CDN to local hosting

- Downloaded all images from library-ihouseprd.b-cdn.net and idx-acnt-ihouseprd.b-cdn.net
- Updated 609 blog post markdown files to reference local image paths
- Organized images by blog post in public/images/blog/[post-name]/
- Ensures images remain intact when old iHouse account is closed

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### 3. Push to GitHub

```bash
git push origin main
```

Netlify will automatically deploy with all images hosted locally.

### 4. Test Production

After deployment, verify images on the live site:
- https://santaclaritaopenhouses.com/blog

## File Organization

Images will be organized like this:

```
public/
└── images/
    └── blog/
        ├── valencia-real-estate-market-january-2026/
        │   ├── valencia-real-estate-2026.webp
        │   └── market-graph-valencia.png
        ├── canyon-country-real-estate-january-2026/
        │   ├── canyon-country-2026-market.webp
        │   └── inventory-chart.jpg
        └── [608 more blog post directories]/
            └── [their respective images]
```

This structure:
- ✅ Keeps images organized by blog post
- ✅ Makes it easy to find/update images for specific posts
- ✅ Prevents filename conflicts
- ✅ Serves images directly from your site (no external dependencies)

## What About heroImage in Frontmatter?

The script will also update `heroImage` URLs in the frontmatter if they reference CDN domains.

Example:
```yaml
# Before
heroImage: "https://idx-acnt-ihouseprd.b-cdn.net/AR1197716/file_manager/valencia-2026.webp"

# After
heroImage: "/images/blog/valencia-real-estate-market-january-2026/valencia-2026.webp"
```

## Troubleshooting

### Images Not Downloading

If some images fail to download:
- Check internet connection
- Verify CDN URLs are still accessible
- Re-run the script (it will skip already-downloaded images)

### Disk Space

If you have hundreds of images:
- Check available disk space before running
- Images will be saved to `public/images/blog/`
- Typical blog post has 1-5 images at 50-500KB each

### Git Large Files

If you have very large images (>100MB total):
- Git might complain about large files
- Consider using Git LFS (Large File Storage)
- Or optimize images before committing

## Rollback Plan

If something goes wrong:

```bash
# Restore original markdown files
git checkout HEAD -- src/content/blog/

# Remove downloaded images
rm -rf public/images/blog/
```

## Questions?

Contact Connor:
- **Phone:** 661.400.1720
- **Email:** connor@santaclaritaopenhouses.com
