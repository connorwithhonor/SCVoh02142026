#!/usr/bin/env python3
"""
Generate Netlify _redirects file from blog post frontmatter.
Extracts source URLs and creates 301 redirects to new blog routes.
"""

import os
import re
from pathlib import Path

def extract_source_and_slug(filepath):
    """Extract source URL and generate slug from blog post frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract source URL from frontmatter
    source_match = re.search(r'^source:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
    if not source_match:
        return None, None

    source_url = source_match.group(1).strip()

    # Generate slug from filename
    slug = Path(filepath).stem

    return source_url, slug

def generate_redirects():
    """Generate _redirects file for Netlify."""
    blog_dir = Path('src/content/blog')
    redirects = []

    # Process all blog posts
    for md_file in sorted(blog_dir.glob('*.md')):
        source_url, slug = extract_source_and_slug(md_file)
        if source_url and slug:
            # Extract path from source URL
            path_match = re.search(r'santaclaritaopenhouses\.com(/.*?)(?:\?|#|$)', source_url)
            if path_match:
                old_path = path_match.group(1).rstrip('/')
                new_path = f'/blog/{slug}'
                redirects.append((old_path, new_path))

    # Write _redirects file
    output_file = Path('public/_redirects')
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('# Blog post redirects from old site to new site\n')
        f.write('# Format: old_path new_path 301\n\n')

        for old_path, new_path in redirects:
            f.write(f'{old_path} {new_path} 301\n')

        # Add common redirects
        f.write('\n# Common page redirects\n')
        f.write('/blog.html /blog 301\n')
        f.write('/blog.htm /blog 301\n')

    print(f'Generated {len(redirects)} redirects in public/_redirects')
    return len(redirects)

if __name__ == '__main__':
    os.chdir(Path(__file__).parent.parent)
    count = generate_redirects()
    print(f'Success! Created {count} blog post redirects.')
