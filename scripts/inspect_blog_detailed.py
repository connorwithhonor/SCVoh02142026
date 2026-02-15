#!/usr/bin/env python3
"""Detailed inspection to find blog posts"""

import requests
from bs4 import BeautifulSoup
import json

url = "https://SantaClaritaOpenHouses.com/blog"

try:
    response = requests.get(url, timeout=30, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    response.raise_for_status()

    # Save full HTML for inspection
    with open('blog_page_full.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Saved full HTML to blog_page_full.html")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Look for all divs that might contain blog posts
    print("\n" + "=" * 60)
    print("Looking for blog post containers...")
    print("=" * 60)

    # Search for common blog-related class names
    blog_classes = ['post', 'blog', 'article', 'card', 'item', 'entry']
    for cls in blog_classes:
        elements = soup.find_all(class_=lambda x: x and cls in x.lower())
        if elements:
            print(f"\nFound {len(elements)} elements with class containing '{cls}':")
            for elem in elements[:3]:
                print(f"  - {elem.get('class')}: {str(elem)[:100]}")

    # Look for script tags that might contain JSON data
    print("\n" + "=" * 60)
    print("Checking for JSON/JavaScript data...")
    print("=" * 60)
    scripts = soup.find_all('script')
    print(f"Found {len(scripts)} script tags")

    for script in scripts:
        script_text = script.string or ''
        if 'blog' in script_text.lower() or 'post' in script_text.lower():
            if len(script_text) > 100:
                print(f"\n--- Script containing 'blog' or 'post' (first 500 chars) ---")
                print(script_text[:500])

    # Check for data attributes
    print("\n" + "=" * 60)
    print("Elements with data attributes:")
    print("=" * 60)
    data_elements = soup.find_all(attrs=lambda x: x and any('data-' in str(k) for k in x.keys()))
    print(f"Found {len(data_elements)} elements with data attributes")
    for elem in data_elements[:5]:
        attrs = {k: v for k, v in elem.attrs.items() if k.startswith('data-')}
        print(f"  {elem.name}: {attrs}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
