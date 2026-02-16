#!/usr/bin/env python3
"""
Fix publishDate format in all blog posts by removing microseconds
"""

import os
import re
from pathlib import Path

def fix_date_format(content):
    """Add pubDate field matching publishDate value"""
    # Match the publishDate line
    pattern = r'(publishDate: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}))\n'
    # Replace with publishDate and pubDate (same value)
    replacement = r'\1\npubDate: \2\n'
    return re.sub(pattern, replacement, content)

def main():
    blog_dir = Path(__file__).parent.parent / 'src' / 'content' / 'blog'

    fixed_count = 0
    error_count = 0

    for md_file in blog_dir.glob('*.md'):
        try:
            # Read the file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix the dates
            fixed_content = fix_date_format(content)

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
