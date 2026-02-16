#!/usr/bin/env python3
"""
Fix invalid YAML escape sequences in blog post frontmatter
"""

import os
import re
from pathlib import Path

def fix_yaml_escapes(content):
    """Fix invalid backslash escape sequences in YAML frontmatter"""
    # Pattern: Find title or description with quotes containing backslash followed by non-escape char
    # Invalid escapes like \M, \R, etc. should be removed
    pattern = r'(title|description):\s*"([^"]*)"'

    def replace_escapes(match):
        field = match.group(1)
        value = match.group(2)
        # Remove leading backslash if it's followed by a regular letter (not a valid escape)
        fixed_value = re.sub(r'\\([a-zA-Z])', r'\1', value)
        return f'{field}: "{fixed_value}"'

    return re.sub(pattern, replace_escapes, content)

def main():
    blog_dir = Path(__file__).parent.parent / 'src' / 'content' / 'blog'

    fixed_count = 0
    error_count = 0

    for md_file in blog_dir.glob('*.md'):
        try:
            # Read the file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix YAML escapes
            fixed_content = fix_yaml_escapes(content)

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
