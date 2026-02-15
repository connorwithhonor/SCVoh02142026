#!/usr/bin/env python3
"""Quick script to inspect the blog page structure"""

import requests
from bs4 import BeautifulSoup

url = "https://SantaClaritaOpenHouses.com/blog"

try:
    response = requests.get(url, timeout=30, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    print("=" * 60)
    print(f"Inspecting: {url}")
    print("=" * 60)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Content Length: {len(response.content)} bytes")
    print("\n" + "=" * 60)
    print("Page Title:")
    print("=" * 60)
    title = soup.find('title')
    print(title.get_text() if title else "No title found")

    print("\n" + "=" * 60)
    print("All Links on Page:")
    print("=" * 60)
    links = soup.find_all('a', href=True)
    print(f"Found {len(links)} total links")

    blog_links = [link for link in links if '/blog/' in link.get('href', '')]
    print(f"Found {len(blog_links)} links containing '/blog/'")

    if blog_links:
        print("\nFirst 10 blog links:")
        for i, link in enumerate(blog_links[:10]):
            print(f"  {i+1}. {link.get('href')} - {link.get_text(strip=True)[:50]}")

    print("\n" + "=" * 60)
    print("HTML Structure (first 2000 chars):")
    print("=" * 60)
    print(soup.prettify()[:2000])

    print("\n" + "=" * 60)
    print("Main Content Area:")
    print("=" * 60)
    # Look for common content containers
    for selector in ['main', 'article', '.content', '#content', '.blog', '.posts']:
        elem = soup.select_one(selector)
        if elem:
            print(f"\nFound <{selector}>:")
            print(str(elem)[:500])

except Exception as e:
    print(f"Error: {e}")
