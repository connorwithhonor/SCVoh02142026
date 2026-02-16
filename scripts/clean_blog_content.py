#!/usr/bin/env python3
"""
Clean up scraped blog content by removing code blocks and other artifacts
"""

import re
from pathlib import Path

def clean_content(content):
    """Remove code blocks and other scraping artifacts"""
    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    frontmatter = parts[1]
    body = parts[2]

    # Remove code blocks (``` or ~~~)
    body = re.sub(r'```[\s\S]*?```', '', body)
    body = re.sub(r'~~~[\s\S]*?~~~', '', body)

    # Remove inline code with HTML/JS looking content
    body = re.sub(r'`[^`]*?<[^>]+>[^`]*?`', '', body)

    # Remove any remaining HTML script/style tags
    body = re.sub(r'<script[\s\S]*?</script>', '', body, flags=re.IGNORECASE)
    body = re.sub(r'<style[\s\S]*?</style>', '', body, flags=re.IGNORECASE)

    # Remove excessive blank lines (more than 2 consecutive)
    body = re.sub(r'\n{3,}', '\n\n', body)

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

            # Clean the content
            cleaned_content = clean_content(content)

            # Only write if changes were made
            if cleaned_content != content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                fixed_count += 1
                print(f"Cleaned: {md_file.name}")

        except Exception as e:
            error_count += 1
            print(f"Error processing {md_file.name}: {e}")

    print(f"\nComplete!")
    print(f"Files cleaned: {fixed_count}")
    print(f"Errors: {error_count}")

if __name__ == '__main__':
    main()
