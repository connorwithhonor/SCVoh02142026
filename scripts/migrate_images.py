#!/usr/bin/env python3
"""
Image Migration Tool for Santa Clarita Open Houses Blog
Scans all blog posts, downloads images from CDN, and updates markdown files.
"""

import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote
import time
from collections import defaultdict

# Configuration
BLOG_DIR = Path(__file__).parent.parent / "src" / "content" / "blog"
PUBLIC_IMAGES_DIR = Path(__file__).parent.parent / "public" / "images" / "blog"
CDN_DOMAINS = [
    "library-ihouseprd.b-cdn.net",
    "idx-acnt-ihouseprd.b-cdn.net",
    "santaclaritaopenhouses.com"
]

# Create images directory if it doesn't exist
PUBLIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def extract_image_urls(markdown_content):
    """Extract all image URLs from markdown content."""
    # Match ![alt](url) and ![](url) patterns
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, markdown_content)
    return [(alt, url) for alt, url in matches]

def is_cdn_image(url):
    """Check if URL is from one of our CDN domains."""
    parsed = urlparse(url)
    return any(domain in parsed.netloc for domain in CDN_DOMAINS)

def sanitize_filename(url):
    """Create a safe filename from URL."""
    parsed = urlparse(url)
    path = parsed.path

    # Remove query parameters for filename
    filename = path.split('/')[-1]
    filename = unquote(filename)

    # Remove special characters
    filename = re.sub(r'[^\w\-.]', '_', filename)

    # Ensure we have an extension
    if '.' not in filename:
        # Try to get extension from URL
        if '.jpg' in url.lower() or '.jpeg' in url.lower():
            filename += '.jpg'
        elif '.png' in url.lower():
            filename += '.png'
        elif '.webp' in url.lower():
            filename += '.webp'
        elif '.gif' in url.lower():
            filename += '.gif'
        else:
            filename += '.jpg'  # Default

    return filename

def download_image(url, destination):
    """Download image from URL to destination path."""
    try:
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()

        with open(destination, 'wb') as f:
            f.write(response.content)

        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def process_blog_post(file_path):
    """Process a single blog post, download images, and update markdown."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    images = extract_image_urls(content)

    if not images:
        return 0, 0, 0  # no images, downloaded, updated

    cdn_images = [(alt, url) for alt, url in images if is_cdn_image(url)]

    if not cdn_images:
        return len(images), 0, 0  # found images but none from CDN

    downloaded = 0
    updated = 0

    for alt, url in cdn_images:
        # Create filename
        filename = sanitize_filename(url)

        # Create subdirectory based on blog post name for organization
        post_name = file_path.stem
        post_image_dir = PUBLIC_IMAGES_DIR / post_name
        post_image_dir.mkdir(exist_ok=True)

        destination = post_image_dir / filename

        # Download image if it doesn't exist
        if not destination.exists():
            print(f"Downloading: {url}")
            if download_image(url, destination):
                downloaded += 1
                print(f"Saved to: {destination.relative_to(PUBLIC_IMAGES_DIR.parent.parent)}")
            else:
                continue  # Skip URL replacement if download failed

            # Rate limiting to be nice to CDN
            time.sleep(0.5)
        else:
            print(f"Already exists: {destination.relative_to(PUBLIC_IMAGES_DIR.parent.parent)}")

        # Update markdown with new URL
        new_url = f"/images/blog/{post_name}/{filename}"
        content = content.replace(url, new_url)
        updated += 1

    # Write updated content back to file if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path.name}\n")

    return len(cdn_images), downloaded, updated

def main():
    """Main migration process."""
    print("=" * 80)
    print("IMAGE MIGRATION TOOL - Santa Clarita Open Houses")
    print("=" * 80)
    print()
    print(f"Blog directory: {BLOG_DIR}")
    print(f"Images will be saved to: {PUBLIC_IMAGES_DIR}")
    print()
    print("Scanning blog posts for images from CDN domains:")
    for domain in CDN_DOMAINS:
        print(f"   - {domain}")
    print()

    # Get all markdown files
    blog_posts = list(BLOG_DIR.glob("*.md"))
    print(f"Found {len(blog_posts)} blog posts")
    print()

    total_images = 0
    total_downloaded = 0
    total_updated = 0
    posts_with_images = 0

    for i, post_file in enumerate(blog_posts, 1):
        print(f"[{i}/{len(blog_posts)}] Processing: {post_file.name}")

        images_found, images_downloaded, images_updated = process_blog_post(post_file)

        if images_found > 0:
            posts_with_images += 1
            total_images += images_found
            total_downloaded += images_downloaded
            total_updated += images_updated

    print()
    print("=" * 80)
    print("MIGRATION SUMMARY")
    print("=" * 80)
    print(f"Posts processed: {len(blog_posts)}")
    print(f"Posts with CDN images: {posts_with_images}")
    print(f"Total CDN images found: {total_images}")
    print(f"Images downloaded: {total_downloaded}")
    print(f"Markdown files updated: {total_updated}")
    print()

    if total_downloaded > 0:
        print("NEXT STEPS:")
        print("1. Review the downloaded images in: public/images/blog/")
        print("2. Test a few blog posts to ensure images display correctly")
        print("3. Commit the changes to git:")
        print(f"   git add public/images/blog/ src/content/blog/")
        print(f'   git commit -m "Migrate {total_downloaded} blog images from CDN to local hosting"')
        print("4. Push to GitHub and Netlify will auto-deploy")
    else:
        print("No new images to download (all already exist locally)")

    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
