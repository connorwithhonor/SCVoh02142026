#!/usr/bin/env python3
"""
Fix and redirect links in blog posts
- Remove or fix malformed links
- Update old site links to new routes
- Create internal blog cross-links where relevant
"""

import re
from pathlib import Path

# Map old URLs to new routes
URL_REDIRECTS = {
    'https://www.santaclaritaopenhouses.com/contact': '/contact',
    'https://www.santaclaritaopenhouses.com/free-market-analysis': '/contact',
    'https://www.santaclaritaopenhouses.com/santa-clarita-market-report': '/blog',
    'https://www.santaclaritaopenhouses.com/active-listings': '/',
    'https://www.santaclaritaopenhouses.com/blog': '/blog',
    'https://www.santaclaritaopenhouses.com/mortgage-rates': '/blog',
    'https://www.santaclaritaopenhouses.com/advanced-search': '/',
    'https://www.santaclaritaopenhouses.com/dream-home-finder': '/contact',
    'https://www.santaclaritaopenhouses.com/testimonials': '/',
    'https://www.santaclaritaopenhouses.com/about': '/',
    'https://www.santaclaritaopenhouses.com/homes-for-sale-in-valencia-ca': '/',
    'https://www.santaclaritaopenhouses.com/homes-for-sale-in-canyon-country-ca': '/',
    'https://www.santaclaritaopenhouses.com/homes-for-sale-in-saugus-ca': '/',
    'https://www.santaclaritaopenhouses.com/homes-for-sale-in-stevenson-ranch-ca': '/',
    'https://www.santaclaritaopenhouses.com/': '/',
    'https://www.santaclaritaopenhouses.com': '/',
    'https://zoommescv.com': '/',
    'https://SantaClaritaOpenhouses.com/book': '/contact',
}

def fix_links(content):
    """Fix and redirect links in content"""
    # Split frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    frontmatter = parts[1]
    body = parts[2]

    # Fix malformed links with ]( patterns
    body = re.sub(r'\]\(https://[^\)]+\]\(https://([^\)]+)\)', r'](https://\1)', body)

    # Replace old site URLs with new routes
    for old_url, new_route in URL_REDIRECTS.items():
        # Handle both with and without markdown link text
        body = body.replace(f']({old_url})', f']({new_route})')
        body = body.replace(f'({old_url})', f'({new_route})')

    # Remove links to pages that don't exist (like specific property pages)
    # Keep the link text but remove the broken URL
    body = re.sub(r'\[([^\]]+)\]\(https://www\.santaclaritaopenhouses\.com/[^\)]+\)', r'\1', body)

    return f'---{frontmatter}---{body}'

def main():
    blog_dir = Path(__file__).parent.parent / 'src' / 'content' / 'blog'

    fixed_count = 0
    error_count = 0

    for md_file in blog_dir.glob('*.md'):
        try:
            # Read the file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix links
            fixed_content = fix_links(content)

            # Only write if changes were made
            if fixed_content != content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                fixed_count += 1
                print(f"Fixed: {md_file.name}")

        except Exception as e:
            error_count += 1
            print(f"Error processing {md_file.name}: {e}")

    print(f"\nComplete!")
    print(f"Files fixed: {fixed_count}")
    print(f"Errors: {error_count}")

if __name__ == '__main__':
    main()
