#!/usr/bin/env python3
"""
Site Migration Scraper for SantaClaritaOpenHouses.com
Scrapes existing site and converts to Astro markdown format
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re
from datetime import datetime
import json
from pathlib import Path

class SiteScraper:
    def __init__(self, base_url, output_dir="scraped_content"):
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.visited_urls = set()
        self.pages = []
        self.redirects = []

        # Create output directories
        Path(output_dir).mkdir(exist_ok=True)
        Path(f"{output_dir}/blog").mkdir(exist_ok=True)
        Path(f"{output_dir}/images").mkdir(exist_ok=True)

    def is_valid_url(self, url):
        """Check if URL belongs to the same domain"""
        parsed = urlparse(url)
        base_parsed = urlparse(self.base_url)
        return parsed.netloc == base_parsed.netloc or parsed.netloc == ''

    def get_slug_from_url(self, url):
        """Extract clean slug from URL"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')

        # Remove common extensions
        path = re.sub(r'\.(html|htm|php)$', '', path)

        # Convert to slug format
        slug = re.sub(r'[^a-z0-9]+', '-', path.lower())
        slug = slug.strip('-')

        return slug or 'home'

    def scrape_page(self, url):
        """Scrape a single page"""
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract metadata
            title = soup.find('title')
            title = title.text.strip() if title else "Untitled"

            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'].strip() if meta_desc else ""

            # Extract main content
            # Try common content containers
            content_selectors = [
                'article',
                'main',
                '.content',
                '#content',
                '.post-content',
                '.entry-content',
                'body'
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
                for unwanted in content.select('script, style, nav, header, footer, .sidebar, #sidebar, .comments'):
                    unwanted.decompose()

            # Extract text content
            text_content = content.get_text(separator='\n\n', strip=True) if content else ""

            # Clean up excessive whitespace
            text_content = re.sub(r'\n{3,}', '\n\n', text_content)

            # Get HTML content (for reference)
            html_content = str(content) if content else ""

            # Generate slug
            slug = self.get_slug_from_url(url)

            # Store page data
            page_data = {
                'url': url,
                'slug': slug,
                'title': title,
                'description': description,
                'content': text_content,
                'html': html_content,
                'scraped_at': datetime.now().isoformat()
            }

            self.pages.append(page_data)

            # Add to redirect mapping
            if url != self.base_url:
                old_path = urlparse(url).path
                new_path = f"/blog/{slug}"
                self.redirects.append({
                    'old': old_path,
                    'new': new_path
                })

            return soup

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def crawl(self, start_url=None, max_pages=100):
        """Crawl the site starting from start_url"""
        if start_url is None:
            start_url = self.base_url

        to_visit = [start_url]

        while to_visit and len(self.visited_urls) < max_pages:
            url = to_visit.pop(0)

            if url in self.visited_urls:
                continue

            if not self.is_valid_url(url):
                continue

            self.visited_urls.add(url)
            soup = self.scrape_page(url)

            if soup:
                # Find all links on page
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)

                    # Only follow internal links
                    if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                        # Skip anchors, mailto, tel, etc.
                        if not full_url.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                            to_visit.append(full_url)

        print(f"\nScraped {len(self.pages)} pages")

    def convert_to_markdown(self, page):
        """Convert page to Astro markdown format"""
        # Clean title for frontmatter
        title = page['title'].replace('"', '\\"')
        description = page['description'].replace('"', '\\"') if page['description'] else title

        # Generate frontmatter
        frontmatter = f"""---
title: "{title}"
description: "{description}"
pubDate: "{datetime.now().isoformat()}"
heroImage: "https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697cbafc1311f61da1eae20f.png"
neighborhood: "Santa Clarita"
---

"""

        # Combine frontmatter and content
        markdown = frontmatter + page['content']

        return markdown

    def save_markdown_files(self):
        """Save all pages as markdown files"""
        for page in self.pages:
            slug = page['slug']
            markdown = self.convert_to_markdown(page)

            # Save to blog directory
            filename = f"{self.output_dir}/blog/{slug}.md"

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
            'base_url': self.base_url,
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
    print("SantaClaritaOpenHouses.com Migration Scraper")
    print("=" * 60)
    print()

    # Get base URL from user
    base_url = input("Enter the current site URL (e.g., https://santaclaritaopenhouses.com): ").strip()

    if not base_url:
        print("Using default: https://santaclaritaopenhouses.com")
        base_url = "https://santaclaritaopenhouses.com"

    # Ask for max pages
    max_pages_input = input("Maximum pages to scrape (default: 100): ").strip()
    max_pages = int(max_pages_input) if max_pages_input else 100

    print(f"\nStarting crawl of {base_url}")
    print(f"Maximum pages: {max_pages}")
    print("-" * 60)

    # Create scraper and run
    scraper = SiteScraper(base_url)
    scraper.crawl(max_pages=max_pages)

    # Save results
    print("\n" + "=" * 60)
    print("Saving results...")
    print("=" * 60)

    scraper.save_markdown_files()
    scraper.save_redirects()
    scraper.save_metadata()

    print("\n" + "=" * 60)
    print("Migration scraping complete!")
    print("=" * 60)
    print(f"\nScraped {len(scraper.pages)} pages")
    print(f"Output directory: {scraper.output_dir}/")
    print(f"\nNext steps:")
    print(f"1. Review scraped content in {scraper.output_dir}/blog/")
    print(f"2. Copy markdown files to src/content/blog/")
    print(f"3. Copy _redirects file to public/ directory")
    print(f"4. Test locally, then deploy to Netlify")
    print()


if __name__ == "__main__":
    main()
