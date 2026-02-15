#!/usr/bin/env python3
"""
URL List Scraper - You provide the URLs, it scrapes them
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from datetime import datetime
import json
from pathlib import Path

class URLListScraper:
    def __init__(self, output_dir="scraped_content"):
        self.output_dir = output_dir
        self.pages = []
        self.redirects = []

        Path(output_dir).mkdir(exist_ok=True)
        Path(f"{output_dir}/blog").mkdir(exist_ok=True)

    def get_slug_from_url(self, url):
        """Extract clean slug from URL"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        path = re.sub(r'\.(html|htm|php)$', '', path)
        parts = path.split('/')
        slug = parts[-1] if parts else 'page'
        slug = re.sub(r'[^a-z0-9]+', '-', slug.lower())
        return slug.strip('-') or 'page'

    def scrape_page(self, url):
        """Scrape a single page"""
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title = soup.find('title')
            title_text = title.text.strip() if title else "Untitled"
            title_text = re.sub(r'\s*\|\s*.*$', '', title_text)
            title_text = re.sub(r'\s*-\s*.*$', '', title_text)

            # Extract description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else title_text

            # Extract content
            content_selectors = ['article', '.post-content', '.entry-content', 'main', '.content', '#content']
            content = None
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    break

            if not content:
                content = soup.find('body')

            if content:
                for unwanted in content.select('script, style, nav, header, footer, .sidebar, #sidebar, .comments, .advertisement'):
                    unwanted.decompose()

            text_content = content.get_text(separator='\n\n', strip=True) if content else ""
            text_content = re.sub(r'\n{3,}', '\n\n', text_content)

            if len(text_content) < 100:
                print(f"  ⚠️  Too short, skipping")
                return None

            # Detect neighborhood
            neighborhoods = ['Castaic', 'Canyon Country', 'Newhall', 'Saugus', 'Stevenson Ranch', 'Valencia']
            detected_neighborhood = "Santa Clarita"
            text_check = (url + title_text + text_content).lower()
            for hood in neighborhoods:
                if hood.lower() in text_check:
                    detected_neighborhood = hood
                    break

            slug = self.get_slug_from_url(url)

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

            old_path = urlparse(url).path.rstrip('/') or '/'
            new_path = f"/blog/{slug}"
            self.redirects.append({'old': old_path, 'new': new_path})

            print(f"  ✅ {title_text}")
            return True

        except Exception as e:
            print(f"  ❌ Error: {e}")
            return None

    def scrape_urls(self, urls):
        """Scrape list of URLs"""
        print(f"\n{'='*60}")
        print(f"Scraping {len(urls)} URLs")
        print(f"{'='*60}\n")

        for url in urls:
            self.scrape_page(url.strip())

        print(f"\n{'='*60}")
        print(f"Scraped {len(self.pages)} pages successfully")
        print(f"{'='*60}\n")

    def convert_to_markdown(self, page):
        """Convert to markdown"""
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
        return frontmatter + page['content']

    def save_markdown_files(self):
        """Save markdown files"""
        today = datetime.now().strftime('%Y-%m-%d')
        for i, page in enumerate(self.pages):
            slug = page['slug']
            markdown = self.convert_to_markdown(page)
            filename = f"{self.output_dir}/blog/{today}-migrated-{i+1:03d}-{slug}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"Saved: {filename}")

    def save_redirects(self):
        """Save redirects"""
        if not self.redirects:
            return
        content = "# Redirects from old site\n\n"
        for r in self.redirects:
            content += f"{r['old']}    {r['new']}    301\n"
        with open(f"{self.output_dir}/_redirects", 'w') as f:
            f.write(content)
        print(f"\nSaved {len(self.redirects)} redirects")

    def save_metadata(self):
        """Save metadata"""
        metadata = {
            'scraped_at': datetime.now().isoformat(),
            'total_pages': len(self.pages),
            'pages': [{'url': p['url'], 'slug': p['slug'], 'title': p['title']} for p in self.pages]
        }
        with open(f"{self.output_dir}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)


def main():
    print("=" * 60)
    print("URL List Scraper")
    print("=" * 60)
    print()
    print("INSTRUCTIONS:")
    print("1. Open https://www.santaclaritaopenhouses.com/sitemap.xml in your browser")
    print("2. Copy ALL the URLs (one per line)")
    print("3. Create a file called 'urls.txt' in this directory")
    print("4. Paste all URLs into urls.txt")
    print("5. Run this script again")
    print()

    # Check if urls.txt exists
    if not Path('urls.txt').exists():
        print("❌ urls.txt not found!")
        print()
        print("Creating urls.txt template for you...")
        with open('urls.txt', 'w') as f:
            f.write("# Paste your URLs here, one per line\n")
            f.write("# Example:\n")
            f.write("# https://www.santaclaritaopenhouses.com/blog/post-1\n")
            f.write("# https://www.santaclaritaopenhouses.com/blog/post-2\n")
        print("✅ Created urls.txt - add your URLs and run again!")
        return

    # Read URLs
    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not urls:
        print("❌ No URLs found in urls.txt!")
        print("Add URLs (one per line) and run again.")
        return

    print(f"Found {len(urls)} URLs in urls.txt\n")

    scraper = URLListScraper()
    scraper.scrape_urls(urls)

    if len(scraper.pages) == 0:
        print("\n❌ No pages scraped successfully!")
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
    print(f'2. Run: cp scraped_content/_redirects "../public/"')
    print(f'3. Test: cd .. && npm run dev')
    print()


if __name__ == "__main__":
    main()
