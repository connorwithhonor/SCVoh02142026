#!/usr/bin/env python3
"""
Targeted Sitemap Scraper for SantaClaritaOpenHouses.com
Scrapes only seller-relevant blog posts from sitemap.xml
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import re
from datetime import datetime
import json
from pathlib import Path
import xml.etree.ElementTree as ET

class SitemapScraper:
    def __init__(self, sitemap_url, output_dir="scraped_content"):
        self.sitemap_url = sitemap_url
        self.output_dir = output_dir
        self.pages = []
        self.redirects = []

        # Seller-relevant keywords to filter by
        self.seller_keywords = [
            'sell', 'selling', 'seller', 'sellers',
            'list', 'listing', 'agent',
            'market', 'price', 'pricing', 'value', 'valuation',
            'home seller', 'property seller',
            'tips', 'guide', 'how to',
            'commission', 'negotiate',
            'prepare', 'staging', 'repair',
            'castaic', 'canyon country', 'newhall', 'saugus', 'stevenson ranch', 'valencia'
        ]

        # Create output directories
        Path(output_dir).mkdir(exist_ok=True)
        Path(f"{output_dir}/blog").mkdir(exist_ok=True)

    def fetch_sitemap_urls(self):
        """Fetch all URLs from sitemap"""
        print(f"Fetching sitemap: {self.sitemap_url}")

        try:
            response = requests.get(self.sitemap_url, timeout=10)
            response.raise_for_status()

            # Parse XML
            root = ET.fromstring(response.content)

            # Handle namespace
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            urls = []
            for url_element in root.findall('.//ns:url', namespace):
                loc = url_element.find('ns:loc', namespace)
                if loc is not None:
                    urls.append(loc.text)

            print(f"Found {len(urls)} URLs in sitemap")
            return urls

        except Exception as e:
            print(f"Error fetching sitemap: {e}")
            return []

    def is_seller_relevant(self, url, title="", content=""):
        """Check if URL/content is relevant to sellers"""
        # Combine all text for checking
        text_to_check = f"{url} {title} {content}".lower()

        # Check for seller keywords
        for keyword in self.seller_keywords:
            if keyword in text_to_check:
                return True

        return False

    def get_slug_from_url(self, url):
        """Extract clean slug from URL"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')

        # Remove common extensions
        path = re.sub(r'\.(html|htm|php)$', '', path)

        # Get last part of path for blog posts
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
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract metadata
            title = soup.find('title')
            title_text = title.text.strip() if title else ""

            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'].strip() if meta_desc else ""

            # Extract main content
            content_selectors = [
                'article',
                'main',
                '.post-content',
                '.entry-content',
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
                for unwanted in content.select('script, style, nav, header, footer, .sidebar, #sidebar, .comments, .advertisement'):
                    unwanted.decompose()

            # Extract text content
            text_content = content.get_text(separator='\n\n', strip=True) if content else ""

            # Clean up excessive whitespace
            text_content = re.sub(r'\n{3,}', '\n\n', text_content)

            # Check if relevant to sellers
            if not self.is_seller_relevant(url, title_text, text_content):
                print(f"  ❌ Skipping (not seller-relevant): {title_text}")
                return None

            print(f"  ✅ Keeping (seller-relevant): {title_text}")

            # Generate slug
            slug = self.get_slug_from_url(url)

            # Store page data
            page_data = {
                'url': url,
                'slug': slug,
                'title': title_text,
                'description': description,
                'content': text_content,
                'scraped_at': datetime.now().isoformat()
            }

            self.pages.append(page_data)

            # Add to redirect mapping
            old_path = urlparse(url).path
            new_path = f"/blog/{slug}"
            self.redirects.append({
                'old': old_path,
                'new': new_path
            })

            return page_data

        except Exception as e:
            print(f"  ⚠️  Error: {e}")
            return None

    def scrape_from_sitemap(self):
        """Scrape all seller-relevant pages from sitemap"""
        urls = self.fetch_sitemap_urls()

        if not urls:
            print("No URLs found in sitemap!")
            return

        print(f"\n{'='*60}")
        print(f"Scraping {len(urls)} URLs from sitemap...")
        print(f"{'='*60}\n")

        for url in urls:
            self.scrape_page(url)

        print(f"\n{'='*60}")
        print(f"Scraped {len(self.pages)} seller-relevant pages")
        print(f"Skipped {len(urls) - len(self.pages)} non-seller pages")
        print(f"{'='*60}\n")

    def convert_to_markdown(self, page):
        """Convert page to Astro markdown format"""
        title = page['title'].replace('"', '\\"')
        description = page['description'].replace('"', '\\"') if page['description'] else title

        # Try to detect neighborhood from URL or title
        neighborhoods = ['Castaic', 'Canyon Country', 'Newhall', 'Saugus', 'Stevenson Ranch', 'Valencia']
        detected_neighborhood = "Santa Clarita"

        for neighborhood in neighborhoods:
            if neighborhood.lower() in (page['url'] + page['title'] + page['content']).lower():
                detected_neighborhood = neighborhood
                break

        frontmatter = f"""---
title: "{title}"
description: "{description}"
pubDate: "{datetime.now().isoformat()}"
heroImage: "https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697cbafc1311f61da1eae20f.png"
neighborhood: "{detected_neighborhood}"
updatedDate: "{datetime.now().isoformat()}"
---

"""

        markdown = frontmatter + page['content']
        return markdown

    def save_markdown_files(self):
        """Save all pages as markdown files"""
        for page in self.pages:
            slug = page['slug']
            markdown = self.convert_to_markdown(page)

            # Add date prefix to filename for chronological ordering
            today = datetime.now().strftime('%Y-%m-%d')
            filename = f"{self.output_dir}/blog/{today}-{slug}.md"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown)

            print(f"Saved: {filename}")

    def save_redirects(self):
        """Save redirect mappings for Netlify"""
        redirect_content = "# Redirects from old site to new site\n\n"

        for redirect in self.redirects:
            redirect_content += f"{redirect['old']}    {redirect['new']}    301\n"

        with open(f"{self.output_dir}/_redirects", 'w') as f:
            f.write(redirect_content)

        print(f"\nSaved {len(self.redirects)} redirects to {self.output_dir}/_redirects")

    def save_metadata(self):
        """Save metadata for reference"""
        metadata = {
            'sitemap_url': self.sitemap_url,
            'scraped_at': datetime.now().isoformat(),
            'total_pages': len(self.pages),
            'pages': [
                {
                    'url': p['url'],
                    'slug': p['slug'],
                    'title': p['title']
                }
                for p in self.pages
            ]
        }

        with open(f"{self.output_dir}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"Saved metadata to {self.output_dir}/metadata.json")


def main():
    """Main execution"""
    print("=" * 60)
    print("SantaClaritaOpenHouses.com Sitemap Scraper")
    print("(Seller-Relevant Content Only)")
    print("=" * 60)
    print()

    # Default sitemap URL
    sitemap_url = "https://www.santaclaritaopenhouses.com/sitemap.xml"

    print(f"Sitemap: {sitemap_url}")
    print()

    # Create scraper and run
    scraper = SitemapScraper(sitemap_url)
    scraper.scrape_from_sitemap()

    if len(scraper.pages) == 0:
        print("\n❌ No seller-relevant pages found!")
        print("This could mean:")
        print("- The sitemap has no blog posts")
        print("- The blog posts aren't about selling")
        print("- The keywords need adjustment")
        return

    # Save results
    print("\n" + "=" * 60)
    print("Saving results...")
    print("=" * 60)

    scraper.save_markdown_files()
    scraper.save_redirects()
    scraper.save_metadata()

    print("\n" + "=" * 60)
    print("Scraping complete!")
    print("=" * 60)
    print(f"\nScraped {len(scraper.pages)} seller-relevant pages")
    print(f"Output directory: {scraper.output_dir}/")
    print(f"\nNext steps:")
    print(f'1. Review scraped content in {scraper.output_dir}/blog/')
    print(f'2. Run: cp scraped_content/blog/*.md "../src/content/blog/"')
    print(f'3. Run: cp scraped_content/_redirects "../public/"')
    print(f'4. Test locally: npm run dev')
    print(f'5. Deploy: git add . && git commit -m "Migrate seller content" && git push')
    print()


if __name__ == "__main__":
    main()
