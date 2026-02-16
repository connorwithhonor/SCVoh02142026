#!/usr/bin/env python3
"""
Fix missing image references in blog posts
"""

import re
from pathlib import Path

def fix_missing_images(content):
    """Remove or fix broken image references"""
    # Pattern: ![](open-house-setup.jpg) or ![](virtual-open-house-setup.jpg)
    # Remove these since they don't exist
    content = re.sub(r'!\[\]\((virtual-)?open-house-setup\.jpg\)', '', content)
    return content

def main():
    blog_dir = Path(__file__).parent.parent / 'src' / 'content' / 'blog'

    fixed_count = 0
    error_count = 0

    for md_file in blog_dir.glob('*.md'):
        try:
            # Read the file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix images
            fixed_content = fix_missing_images(content)

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
