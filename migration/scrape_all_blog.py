#!/usr/bin/env python3
"""
Simple Blog Scraper - Grabs ALL blog posts
No filtering, just gets everything
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re
from datetime import datetime
import json
from pathlib import Path

class BlogScraper:
    def __init__(self, base_url, output_dir="scraped_content"):
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.visited_urls = set()
        self.pages = []
        self.redirects = []

        # Create output directories
        Path(output_dir).mkdir(exist_ok=True)
        Path(f"{output_dir}/blog").mkdir(exist_ok=True)

    def is_same_domain(self, url):
        """Check if URL is on same domain"""
        parsed = urlparse(url)
        base_parsed = urlparse(self.base_url)
        return parsed.netloc == base_parsed.netloc or parsed.netloc == ''

    def is_blog_post(self, url):
        """Check if URL looks like a blog post"""
        url_lower = url.lower()

        # Common blog post patterns
        blog_patterns = [
            '/blog/',
            '/post/',
            '/posts/',
            '/article/',
            '/articles/',
        ]

        # Check if URL contains blog patterns
        for pattern in blog_patterns:
            if pattern in url_lower:
                return True

        # Check if it's a dated post (2020/01/post-name, etc.)
        if re.search(r'/\d{4}/\d{2}/', url):
            return True

        return False

    def get_slug_from_url(self, url):
        """Extract clean slug from URL"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')

        # Remove common extensions
        path = re.sub(r'\.(html|htm|php)$', '', path)

        # Get last part for blog posts
        parts = path.split('/')
        slug = parts[-1] if parts else 'page'

        # Clean slug
        slug = re.sub(r'[^a-z0-9]+', '-', slug.lower())
        slug = slug.strip('-')

        return slug or 'page'

    def scrape_page(self, url):
        """Scrape a single page"""
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract metadata
            title = soup.find('title')
            title_text = title.text.strip() if title else "Untitled"

            # Clean title (remove site name)
            title_text = re.sub(r'\s*\|\s*.*$', '', title_text)
            title_text = re.sub(r'\s*-\s*.*$', '', title_text)

            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else title_text

            # Extract main content
            content_selectors = [
                'article',
                '.post-content',
                '.entry-content',
                'main',
                '.content',
                '#content',
            ]

            content = None
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    break

            if not content:
                content = soup.find('body')

            # Remove unwanted elements
            if content:
                for unwanted in content.select('script, style, nav, header, footer, .sidebar, #sidebar, .comments, .comment, .advertisement, .ad, .share, .social'):
                    unwanted.decompose()

            # Extract text content
            text_content = content.get_text(separator='\n\n', strip=True) if content else ""

            # Clean up excessive whitespace
            text_content = re.sub(r'\n{3,}', '\n\n', text_content)
            text_content = re.sub(r' +', ' ', text_content)

            # Skip if too short
            if len(text_content) < 100:
                print(f"  ⚠️  Skipping (too short): {title_text}")
                return None

            print(f"  ✅ Saved: {title_text}")

            # Generate slug
            slug = self.get_slug_from_url(url)

            # Detect neighborhood
            neighborhoods = ['Castaic', 'Canyon Country', 'Newhall', 'Saugus', 'Stevenson Ranch', 'Valencia']
            detected_neighborhood = "Santa Clarita"

            text_to_check = (url + title_text + text_content).lower()
            for neighborhood in neighborhoods:
                if neighborhood.lower() in text_to_check:
                    detected_neighborhood = neighborhood
                    break

            # Store page data
            page_data = {
                'url': url,
                'slug': slug,
                'title': title_text,
                'description': description,
                'content': text_content,
                'neighborhood': detected_neighborhood,
                'scraped_at': datetime.now().isoformat()
            }

            self.pages.append(page_data)

            # Add to redirect mapping
            old_path = urlparse(url).path.rstrip('/')
            if not old_path:
                old_path = '/'
            new_path = f"/blog/{slug}"

            self.redirects.append({
                'old': old_path,
                'new': new_path
            })

            return soup

        except Exception as e:
            print(f"  ❌ Error: {e}")
            return None

    def crawl(self, start_url=None, max_pages=200):
        """Crawl the site"""
        if start_url is None:
            start_url = self.base_url

        to_visit = [start_url]

        # Try common blog URLs
        common_blog_urls = [
            f"{self.base_url}/blog",
            f"{self.base_url}/blog/",
            f"{self.base_url}/posts",
            f"{self.base_url}/posts/",
            f"{self.base_url}/articles",
        ]

        for blog_url in common_blog_urls:
            if blog_url not in to_visit:
                to_visit.append(blog_url)

        print(f"\n{'='*60}")
        print(f"Starting crawl of {self.base_url}")
        print(f"Looking for blog posts...")
        print(f"{'='*60}\n")

        while to_visit and len(self.visited_urls) < max_pages:
            url = to_visit.pop(0)

            if url in self.visited_urls:
                continue

            if not self.is_same_domain(url):
                continue

            self.visited_urls.add(url)

            # Only scrape if it looks like a blog post
            if self.is_blog_post(url) or url == start_url or '/blog' in url:
                soup = self.scrape_page(url)
            else:
                # Just get links, don't scrape content
                try:
                    response = requests.get(url, timeout=10, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    soup = BeautifulSoup(response.content, 'html.parser')
                except:
                    soup = None

            if soup:
                # Find all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)

                    # Clean URL
                    full_url = full_url.split('#')[0]  # Remove anchors
                    full_url = full_url.split('?')[0]  # Remove query params

                    if self.is_same_domain(full_url) and full_url not in self.visited_urls:
                        if not any(skip in full_url for skip in ['mailto:', 'tel:', 'javascript:']):
                            to_visit.append(full_url)

        print(f"\n{'='*60}")
        print(f"Crawl complete!")
        print(f"Found {len(self.pages)} blog posts")
        print(f"{'='*60}\n")

    def convert_to_markdown(self, page):
        """Convert page to Astro markdown format"""
        title = page['title'].replace('"', '\\"')
        description = page['description'].replace('"', '\\"')

        frontmatter = f"""---
title: "{title}"
description: "{description}"
pubDate: "{datetime.now().isoformat()}"
heroImage: "https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697cbafc1311f61da1eae20f.png"
neighborhood: "{page['neighborhood']}"
updatedDate: "{datetime.now().isoformat()}"
---

"""

        markdown = frontmatter + page['content']
        return markdown

    def save_markdown_files(self):
        """Save all pages as markdown files"""
        today = datetime.now().strftime('%Y-%m-%d')

        for i, page in enumerate(self.pages):
            slug = page['slug']
            markdown = self.convert_to_markdown(page)

            # Add counter to avoid duplicates
            filename = f"{self.output_dir}/blog/{today}-migrated-{i+1:03d}-{slug}.md"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown)

            print(f"Saved: {os.path.basename(filename)}")

    def save_redirects(self):
        """Save redirect mappings"""
        if not self.redirects:
            print("No redirects to save")
            return

        redirect_content = "# Redirects from old site to new site\n\n"

        for redirect in self.redirects:
            redirect_content += f"{redirect['old']}    {redirect['new']}    301\n"

        with open(f"{self.output_dir}/_redirects", 'w') as f:
            f.write(redirect_content)

        print(f"\nSaved {len(self.redirects)} redirects")

    def save_metadata(self):
        """Save metadata"""
        metadata = {
            'base_url': self.base_url,
            'scraped_at': datetime.now().isoformat(),
            'total_pages': len(self.pages),
            'pages': [{'url': p['url'], 'slug': p['slug'], 'title': p['title']} for p in self.pages]
        }

        with open(f"{self.output_dir}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"Saved metadata.json")


def main():
    print("=" * 60)
    print("SantaClaritaOpenHouses.com Blog Scraper")
    print("Grabbing ALL blog posts")
    print("=" * 60)
    print()

    base_url = "https://www.santaclaritaopenhouses.com"

    print(f"Target: {base_url}")
    print(f"Max pages: 200")
    print()

    scraper = BlogScraper(base_url)
    scraper.crawl(max_pages=200)

    if len(scraper.pages) == 0:
        print("\n❌ No blog posts found!")
        print("\nPossible reasons:")
        print("- Site structure is different than expected")
        print("- Blog is on a different URL")
        print("- Access is restricted")
        return

    print("\n" + "=" * 60)
    print("Saving results...")
    print("=" * 60 + "\n")

    scraper.save_markdown_files()
    scraper.save_redirects()
    scraper.save_metadata()

    print("\n" + "=" * 60)
    print("✅ DONE!")
    print("=" * 60)
    print(f"\nScraped {len(scraper.pages)} blog posts")
    print(f"\nNext steps:")
    print(f'1. Run: cp scraped_content/blog/*.md "../src/content/blog/"')
    print(f'2. Run: cp scraped_content/_redirects "../public/" (if file exists)')
    print(f'3. Test: cd .. && npm run dev')
    print(f'4. Deploy: git add . && git commit -m "Migrate blog posts" && git push')
    print()


if __name__ == "__main__":
    main()
