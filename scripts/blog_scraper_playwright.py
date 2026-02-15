#!/usr/bin/env python3
"""
Advanced Blog Post Scraper for SantaClaritaOpenHouses.com
Uses Playwright to handle JavaScript rendering
Exports to Astro-compatible markdown format
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import json
import os
from datetime import datetime
import re
import time


class AstroBlogScraper:
    def __init__(self, base_url="https://www.santaclaritaopenhouses.com"):
        self.base_url = base_url

    def load_urls_from_file(self, filename='blog_urls.txt'):
        """Load blog URLs from a text file"""
        urls = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
        return urls

    def clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text

    def extract_slug_from_url(self, url):
        """Extract slug from URL for filename"""
        # Get the last part of the URL
        slug = url.rstrip('/').split('/')[-1]
        # Clean it up
        slug = re.sub(r'[^a-z0-9-]', '', slug.lower())
        return slug[:100]  # Limit length

    def extract_post_content(self, page, url):
        """Extract content from a single blog post using Playwright"""
        print(f"Scraping: {url}")

        try:
            # Navigate to the page
            page.goto(url, wait_until='domcontentloaded', timeout=30000)

            # Wait for main content to load - try multiple selectors
            selectors_to_wait = [
                'article', 'main', '.post-content', '[class*="content"]',
                'p', 'h1', 'h2'  # Basic content elements
            ]

            for selector in selectors_to_wait:
                try:
                    page.wait_for_selector(selector, timeout=5000)
                    break
                except:
                    continue

            # Give JavaScript significant time to fully render
            time.sleep(5)

            # Extract title
            title = None
            title_selectors = [
                'h1',
                'article h1',
                '.post-title',
                '.blog-title',
                'meta[property="og:title"]'
            ]

            for selector in title_selectors:
                try:
                    if 'meta' in selector:
                        elem = page.query_selector(selector)
                        if elem:
                            title = elem.get_attribute('content')
                            break
                    else:
                        elem = page.query_selector(selector)
                        if elem:
                            title = elem.inner_text().strip()
                            if title and title != 'Loading Realty One Group - Success':
                                break
                except:
                    continue

            # First, let's see what the page actually contains
            page_text = page.evaluate('() => document.body.innerText')
            print(f"  Page has {len(page_text)} characters of text")

            # Extract main content HTML
            content_html = ""
            content_text = ""
            content_selectors = [
                'article',
                '[role="main"]',
                '.post-content',
                '.blog-content',
                '.entry-content',
                'main article',
                'main',
                'body'  # Last resort
            ]

            # Get the full body content and clean it
            content_html = page.evaluate("""() => {
                const body = document.body.cloneNode(true);
                const removeSelectors = [
                    'nav', 'footer', 'header', 'script', 'style',
                    '.navigation', '.sidebar', '.menu', '.navbar'
                ];
                removeSelectors.forEach(sel => {
                    body.querySelectorAll(sel).forEach(el => el.remove());
                });
                return body.innerHTML;
            }""")

            content_text = page.evaluate("""() => {
                const body = document.body.cloneNode(true);
                const removeSelectors = [
                    'nav', 'footer', 'header', 'script', 'style',
                    '.navigation', '.sidebar', '.menu', '.navbar'
                ];
                removeSelectors.forEach(sel => {
                    body.querySelectorAll(sel).forEach(el => el.remove());
                });
                return body.innerText;
            }""")

            print(f"  Extracted {len(content_text)} chars of content")

            # Extract metadata
            meta_data = {
                'url': url,
                'title': self.clean_text(title) or 'Untitled',
                'scraped_at': datetime.now().isoformat(),
            }

            # Extract published date
            date_selectors = [
                'time[datetime]',
                '.post-date',
                '.published',
                'meta[property="article:published_time"]'
            ]

            for selector in date_selectors:
                try:
                    elem = page.query_selector(selector)
                    if elem:
                        if 'meta' in selector:
                            meta_data['publishDate'] = elem.get_attribute('content')
                        else:
                            meta_data['publishDate'] = elem.get_attribute('datetime') or elem.inner_text()
                        break
                except:
                    continue

            # Extract author
            author_selectors = [
                '.author',
                '.post-author',
                '[rel="author"]',
                'meta[name="author"]'
            ]

            for selector in author_selectors:
                try:
                    elem = page.query_selector(selector)
                    if elem:
                        if 'meta' in selector:
                            meta_data['author'] = elem.get_attribute('content')
                        else:
                            meta_data['author'] = elem.inner_text()
                        break
                except:
                    continue

            # Extract description
            desc_selectors = [
                'meta[name="description"]',
                'meta[property="og:description"]'
            ]

            for selector in desc_selectors:
                try:
                    elem = page.query_selector(selector)
                    if elem:
                        meta_data['description'] = elem.get_attribute('content')
                        break
                except:
                    continue

            # Extract featured image
            img_selectors = [
                'meta[property="og:image"]',
                'article img',
                '.featured-image img',
                '.post-thumbnail img'
            ]

            for selector in img_selectors:
                try:
                    elem = page.query_selector(selector)
                    if elem:
                        if 'meta' in selector:
                            meta_data['heroImage'] = elem.get_attribute('content')
                        else:
                            meta_data['heroImage'] = elem.get_attribute('src')
                        break
                except:
                    continue

            # Extract categories/tags if available
            try:
                tags = []
                tag_elements = page.query_selector_all('.tag, .category, [rel="tag"]')
                for tag_elem in tag_elements[:5]:  # Limit to 5 tags
                    tag_text = tag_elem.inner_text().strip()
                    if tag_text:
                        tags.append(tag_text)
                if tags:
                    meta_data['tags'] = tags
            except:
                pass

            return {
                'metadata': meta_data,
                'content_text': self.clean_text(content_text),
                'content_html': content_html,
            }

        except PlaywrightTimeout:
            print(f"   Timeout loading {url}")
            return None
        except Exception as e:
            print(f"   Error scraping {url}: {e}")
            return None

    def html_to_markdown(self, html):
        """Convert HTML to markdown (basic conversion)"""
        if not html:
            return ""

        # Basic HTML to Markdown conversion
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)

        # Convert common tags
        html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', html)
        html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', html)
        html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', html)
        html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n\n', html)
        html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.DOTALL)
        html = re.sub(r'<br\s*/?>', '\n', html)
        html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html)
        html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html)
        html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html)
        html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html)
        html = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', html)
        html = re.sub(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>', r'![\2](\1)', html)
        html = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'![](\1)', html)
        html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html, flags=re.DOTALL)
        html = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\1\n', html, flags=re.DOTALL)
        html = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\1\n', html, flags=re.DOTALL)

        # Remove remaining HTML tags
        html = re.sub(r'<[^>]+>', '', html)

        # Clean up whitespace
        html = re.sub(r'\n\n\n+', '\n\n', html)
        html = html.strip()

        return html

    def save_to_astro_markdown(self, posts, output_dir='../src/content/blog'):
        """Save posts as Astro content collection markdown files"""
        os.makedirs(output_dir, exist_ok=True)

        saved_count = 0
        for post in posts:
            metadata = post['metadata']
            slug = self.extract_slug_from_url(metadata['url'])

            # Create frontmatter
            frontmatter = f"""---
title: "{metadata.get('title', 'Untitled').replace('"', '\\"')}"
description: "{metadata.get('description', '').replace('"', '\\"')[:200]}"
publishDate: {metadata.get('publishDate', datetime.now().isoformat())}
"""

            if metadata.get('author'):
                frontmatter += f"author: \"{metadata['author']}\"\n"

            if metadata.get('heroImage'):
                frontmatter += f"heroImage: \"{metadata['heroImage']}\"\n"

            if metadata.get('tags'):
                frontmatter += f"tags: {json.dumps(metadata['tags'])}\n"

            frontmatter += f"""source: "{metadata['url']}"
---

"""

            # Convert HTML to markdown or use text content
            if post.get('content_html'):
                content = self.html_to_markdown(post['content_html'])
            else:
                content = post.get('content_text', 'No content available')

            # Create full markdown file
            full_content = frontmatter + content

            # Save file
            filename = f"{slug}.md"
            filepath = os.path.join(output_dir, filename)

            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                saved_count += 1
            except Exception as e:
                print(f"   Error saving {filename}: {e}")

        print(f"\n Saved {saved_count} Astro markdown files to {output_dir}")
        return output_dir

    def save_to_json(self, posts, filename='blog_posts_full.json'):
        """Save all posts to a JSON file"""
        output_dir = 'scraped_blogs'
        os.makedirs(output_dir, exist_ok=True)

        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

        print(f" Saved {len(posts)} posts to {filepath}")
        return filepath

    def scrape_all(self, urls_file='blog_urls.txt', max_posts=None, start_from=0):
        """Main method to scrape all blog posts"""
        print("=" * 70)
        print("Advanced Blog Scraper for SantaClaritaOpenHouses.com")
        print("=" * 70)

        # Load URLs from file
        blog_urls = self.load_urls_from_file(urls_file)

        if not blog_urls:
            print(f" No URLs found in {urls_file}")
            return

        # Apply limits if specified
        if start_from > 0:
            blog_urls = blog_urls[start_from:]
        if max_posts:
            blog_urls = blog_urls[:max_posts]

        print(f"\n Will scrape {len(blog_urls)} URLs (starting from #{start_from + 1})")
        print(f"  Estimated time: {len(blog_urls) * 3 / 60:.1f} minutes\n")

        # Extract content using Playwright
        all_posts = []
        failed_urls = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()

            for i, url in enumerate(blog_urls, 1):
                print(f"\n[{i + start_from}/{len(blog_urls) + start_from}] ", end='')

                post_data = self.extract_post_content(page, url)

                if post_data:
                    all_posts.append(post_data)
                    print(f"   Success: {post_data['metadata']['title'][:60]}")
                else:
                    failed_urls.append(url)

                # Progress checkpoint every 50 posts
                if i % 50 == 0 and all_posts:
                    print(f"\n Checkpoint: Saving {len(all_posts)} posts...")
                    self.save_to_json(all_posts, f'checkpoint_{i}.json')

            browser.close()

        # Save final results
        if all_posts:
            print("\n" + "=" * 70)
            print(" Saving final results...")
            print("=" * 70)

            self.save_to_json(all_posts)
            self.save_to_astro_markdown(all_posts)

            print("\n" + "=" * 70)
            print(f" Successfully scraped {len(all_posts)} blog posts!")
            if failed_urls:
                print(f"  Failed to scrape {len(failed_urls)} URLs")
                print(f"   Check scraped_blogs/failed_urls.txt for details")

                # Save failed URLs
                with open('scraped_blogs/failed_urls.txt', 'w') as f:
                    f.write('\n'.join(failed_urls))
            print("=" * 70)
        else:
            print("\n No posts were successfully scraped.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Scrape blog posts from SantaClaritaOpenHouses.com')
    parser.add_argument('--max', type=int, help='Maximum number of posts to scrape')
    parser.add_argument('--start', type=int, default=0, help='Start from this post number')
    parser.add_argument('--urls', default='blog_urls.txt', help='File containing blog URLs')

    args = parser.parse_args()

    scraper = AstroBlogScraper()
    scraper.scrape_all(urls_file=args.urls, max_posts=args.max, start_from=args.start)


if __name__ == "__main__":
    main()
