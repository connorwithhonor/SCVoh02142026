#!/usr/bin/env python3
"""Debug scraper to see what we're getting"""

from playwright.sync_api import sync_playwright
import time

url = "https://www.santaclaritaopenhouses.com/why-selling-your-santa-clarita-home-with-a-certified-open-house-expert-2026"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Show browser
    context = browser.new_context()
    page = context.new_page()

    page.goto(url, wait_until='domcontentloaded')
    time.sleep(5)

    # Save full HTML
    html = page.content()
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Saved HTML ({len(html)} chars)")

    # Try to find content
    body_text = page.evaluate('() => document.body.innerText')
    print(f"Body text: {len(body_text)} chars")
    print(f"First 500 chars:\n{body_text[:500]}")

    # Try different selectors
    for selector in ['article', 'main', '.post-content', 'body']:
        try:
            elem = page.query_selector(selector)
            if elem:
                text = elem.inner_text()
                print(f"\n{selector}: {len(text)} chars")
                if len(text) > 1000:
                    print(f"First 200 chars: {text[:200]}")
                    break
        except Exception as e:
            print(f"{selector}: Error - {e}")

    input("Press Enter to close browser...")
    browser.close()
