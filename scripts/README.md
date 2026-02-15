# Blog Scraper for SantaClaritaOpenHouses.com

A Python tool to extract all blog posts from SantaClaritaOpenHouses.com/blog and save them in JSON and Markdown formats.

## Features

- 🔍 Automatically discovers all blog post URLs from the blog index page
- 📝 Extracts title, content, metadata (date, author), and images
- 💾 Saves data in both JSON (for programmatic use) and Markdown (for readability)
- 🎯 Smart content extraction with multiple fallback selectors
- ⏱️ Polite scraping with delays between requests

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python blog_scraper.py
```

## Output

The scraper creates a `scraped_blogs` directory with:

### 1. JSON File (`blog_posts.json`)
Contains all posts with full metadata:
```json
[
  {
    "metadata": {
      "url": "https://SantaClaritaOpenHouses.com/blog/post-title",
      "title": "Post Title",
      "published_date": "2024-01-01",
      "author": "Author Name",
      "images": [...]
    },
    "content": "Full text content...",
    "html": "Original HTML..."
  }
]
```

### 2. Markdown Files (`markdown/`)
Individual `.md` files for each post with frontmatter:
```markdown
---
title: Post Title
url: https://...
published_date: 2024-01-01
---

# Post Title

Content here...
```

## Customization

You can modify the scraper by editing `blog_scraper.py`:

- **Change selectors**: Update the `content_selectors`, `title_selectors`, etc. to match the site's HTML structure
- **Add metadata fields**: Extract additional data like tags, categories, etc.
- **Adjust delay**: Change `time.sleep(1)` to be more or less aggressive
- **Filter posts**: Add logic to skip certain posts based on criteria

## Troubleshooting

**No posts found?**
- The website structure may have changed
- Check the HTML selectors in the script
- Open the blog page in a browser and inspect the HTML structure

**Some content missing?**
- The script uses multiple fallback selectors
- You may need to add specific selectors for that site's structure

## Legal & Ethical Use

- Respect the website's `robots.txt`
- Use scraped content responsibly and ethically
- Consider rate limiting and server load
- Ensure compliance with copyright and terms of service
