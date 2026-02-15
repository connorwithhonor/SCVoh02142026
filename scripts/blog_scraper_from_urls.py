#!/usr/bin/env python3
"""
Blog Post Scraper for SantaClaritaOpenHouses.com
Extracts blog posts from a list of URLs and saves them to JSON and Markdown files
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
    def __init__(self, base_url="https://www.santaclaritaopenhouses.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def load_urls_from_file(self, filename='blog_urls.txt'):
        """Load blog URLs from a text file"""
        urls = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
        return urls

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
        title_selectors = ['h1', 'article h1', '.post-title', '.blog-title', 'meta[property="og:title"]']
        for selector in title_selectors:
            if 'meta' in selector:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get('content', '')
                    break
            else:
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
            'main',
            '[class*="content"]'
        ]

        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Remove script and style elements
                for script in content_elem(['script', 'style', 'nav', 'footer', 'header']):
                    script.decompose()
                content = content_elem.get_text(separator='\n', strip=True)
                if len(content) > 200:  # Make sure we got substantial content
                    break

        # Extract metadata
        meta_data = {
            'url': url,
            'title': title or 'Untitled',
            'scraped_at': datetime.now().isoformat(),
        }

        # Try to find date
        date_selectors = ['time', '.post-date', '.published', '[datetime]', 'meta[property="article:published_time"]']
        for selector in date_selectors:
            if 'meta' in selector:
                date_elem = soup.select_one(selector)
                if date_elem:
                    meta_data['published_date'] = date_elem.get('content', '')
                    break
            else:
                date_elem = soup.select_one(selector)
                if date_elem:
                    meta_data['published_date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)
                    break

        # Try to find author
        author_selectors = ['.author', '.post-author', '[rel="author"]', 'meta[name="author"]']
        for selector in author_selectors:
            if 'meta' in selector:
                author_elem = soup.select_one(selector)
                if author_elem:
                    meta_data['author'] = author_elem.get('content', '')
                    break
            else:
                author_elem = soup.select_one(selector)
                if author_elem:
                    meta_data['author'] = author_elem.get_text(strip=True)
                    break

        # Extract description/excerpt
        desc_selectors = ['meta[name="description"]', 'meta[property="og:description"]']
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                meta_data['description'] = desc_elem.get('content', '')
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

        meta_data['images'] = images[:5]  # Limit to first 5 images

        return {
            'metadata': meta_data,
            'content': content or 'No content extracted',
            'html': str(soup.select_one('article') or soup.select_one('main') or '')[:5000]  # Limit HTML size
        }

    def save_to_json(self, posts, filename='blog_posts.json'):
        """Save all posts to a JSON file"""
        output_dir = 'scraped_blogs'
        os.makedirs(output_dir, exist_ok=True)

        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

        print(f"\nSaved {len(posts)} posts to {filepath}")
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
description: {metadata.get('description', 'N/A')}
---

# {metadata['title']}

{post['content']}

---

## Images
"""

            for img in metadata.get('images', []):
                md_content += f"\n- ![]({img['url']}) - {img['alt']}"

            md_content += f"\n\n---\n\nSource: {metadata['url']}\n"

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)

        print(f"Saved {len(posts)} markdown files to {output_dir}")
        return output_dir

    def scrape_all(self, urls_file='blog_urls.txt'):
        """Main method to scrape all blog posts from URL list"""
        print("=" * 60)
        print("Blog Scraper for SantaClaritaOpenHouses.com")
        print("=" * 60)

        # Load URLs from file
        blog_urls = self.load_urls_from_file(urls_file)

        if not blog_urls:
            print(f"No URLs found in {urls_file}. Please check the file.")
            return

        print(f"\nFound {len(blog_urls)} URLs to scrape")

        # Extract content from each post
        all_posts = []
        failed_urls = []

        for i, url in enumerate(blog_urls, 1):
            print(f"\n[{i}/{len(blog_urls)}] ", end='')
            post_data = self.extract_post_content(url)

            if post_data:
                all_posts.append(post_data)
            else:
                failed_urls.append(url)

            # Be nice to the server - wait between requests
            if i < len(blog_urls):
                time.sleep(0.5)

        # Save results
        if all_posts:
            print("\n" + "=" * 60)
            print("Saving results...")
            print("=" * 60)

            self.save_to_json(all_posts)
            self.save_to_markdown(all_posts)

            print("\n" + "=" * 60)
            print(f"Successfully scraped {len(all_posts)} blog posts!")
            if failed_urls:
                print(f"Failed to scrape {len(failed_urls)} URLs:")
                for url in failed_urls[:5]:
                    print(f"  - {url}")
                if len(failed_urls) > 5:
                    print(f"  ... and {len(failed_urls) - 5} more")
            print("=" * 60)
        else:
            print("No posts were successfully scraped.")


def main():
    scraper = BlogScraper()
    scraper.scrape_all()


if __name__ == "__main__":
    main()
