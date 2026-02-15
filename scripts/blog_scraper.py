#!/usr/bin/env python3
"""
Blog Post Scraper for SantaClaritaOpenHouses.com
Extracts all blog posts and saves them to JSON and Markdown files
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from urllib.parse import urljoin
import re
import time


class BlogScraper:
    def __init__(self, base_url="https://SantaClaritaOpenHouses.com"):
        self.base_url = base_url
        self.blog_url = f"{base_url}/blog"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_all_blog_posts(self):
        """Fetch all blog post URLs from the blog index page"""
        print(f"Fetching blog index from {self.blog_url}...")

        try:
            response = self.session.get(self.blog_url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching blog index: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all blog post links - adjust selectors based on actual site structure
        blog_links = []

        # Common patterns for blog post links
        patterns = [
            {'name': 'article a', 'selector': 'article a[href]'},
            {'name': 'blog-post link', 'selector': 'a.blog-post, a.post-link'},
            {'name': 'h2/h3 links', 'selector': 'h2 a, h3 a'},
            {'name': 'links with /blog/', 'selector': f'a[href*="/blog/"]'},
        ]

        for pattern in patterns:
            links = soup.select(pattern['selector'])
            if links:
                print(f"Found {len(links)} links using pattern: {pattern['name']}")
                for link in links:
                    href = link.get('href')
                    if href and '/blog/' in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in blog_links and full_url != self.blog_url:
                            blog_links.append(full_url)

        # Deduplicate
        blog_links = list(set(blog_links))
        print(f"Found {len(blog_links)} unique blog post URLs")

        return blog_links

    def extract_post_content(self, url):
        """Extract content from a single blog post"""
        print(f"Scraping: {url}")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = None
        title_selectors = ['h1', 'article h1', '.post-title', '.blog-title']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                break

        # Extract main content
        content = None
        content_selectors = [
            'article',
            '.post-content',
            '.blog-content',
            '.entry-content',
            'main article',
            '[class*="content"]'
        ]

        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Remove script and style elements
                for script in content_elem(['script', 'style', 'nav', 'footer']):
                    script.decompose()
                content = content_elem.get_text(separator='\n', strip=True)
                break

        # Extract metadata
        meta_data = {
            'url': url,
            'title': title or 'Untitled',
            'scraped_at': datetime.now().isoformat(),
        }

        # Try to find date
        date_selectors = ['time', '.post-date', '.published', '[datetime]']
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                meta_data['published_date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)
                break

        # Try to find author
        author_selectors = ['.author', '.post-author', '[rel="author"]']
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                meta_data['author'] = author_elem.get_text(strip=True)
                break

        # Extract images
        images = []
        for img in soup.select('article img, .post-content img, main img'):
            img_url = img.get('src')
            if img_url:
                images.append({
                    'url': urljoin(self.base_url, img_url),
                    'alt': img.get('alt', '')
                })

        meta_data['images'] = images

        return {
            'metadata': meta_data,
            'content': content or 'No content extracted',
            'html': str(soup.select_one('article') or soup.select_one('main') or '')
        }

    def save_to_json(self, posts, filename='blog_posts.json'):
        """Save all posts to a JSON file"""
        output_dir = 'scraped_blogs'
        os.makedirs(output_dir, exist_ok=True)

        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(posts)} posts to {filepath}")
        return filepath

    def save_to_markdown(self, posts):
        """Save each post as a separate Markdown file"""
        output_dir = 'scraped_blogs/markdown'
        os.makedirs(output_dir, exist_ok=True)

        for i, post in enumerate(posts):
            metadata = post['metadata']

            # Create safe filename
            safe_title = re.sub(r'[^\w\s-]', '', metadata['title'])
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            filename = f"{i+1:03d}-{safe_title[:50]}.md"

            filepath = os.path.join(output_dir, filename)

            # Create markdown content
            md_content = f"""---
title: {metadata['title']}
url: {metadata['url']}
scraped_at: {metadata['scraped_at']}
published_date: {metadata.get('published_date', 'N/A')}
author: {metadata.get('author', 'N/A')}
---

# {metadata['title']}

{post['content']}

---

## Images
"""

            for img in metadata.get('images', []):
                md_content += f"\n- ![]({img['url']}) - {img['alt']}"

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)

        print(f"Saved {len(posts)} markdown files to {output_dir}")
        return output_dir

    def scrape_all(self):
        """Main method to scrape all blog posts"""
        print("=" * 60)
        print("Blog Scraper for SantaClaritaOpenHouses.com")
        print("=" * 60)

        # Get all blog post URLs
        blog_urls = self.get_all_blog_posts()

        if not blog_urls:
            print("No blog posts found. Please check the website structure.")
            return

        # Extract content from each post
        all_posts = []
        for url in blog_urls:
            post_data = self.extract_post_content(url)
            if post_data:
                all_posts.append(post_data)

            # Be nice to the server
            time.sleep(1)

        # Save results
        if all_posts:
            self.save_to_json(all_posts)
            self.save_to_markdown(all_posts)

            print("=" * 60)
            print(f"Successfully scraped {len(all_posts)} blog posts!")
            print("=" * 60)
        else:
            print("No posts were successfully scraped.")


def main():
    scraper = BlogScraper()
    scraper.scrape_all()


if __name__ == "__main__":
    main()
