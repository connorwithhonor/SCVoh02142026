#!/bin/bash
# Monitor blog scraping progress

while true; do
    clear
    echo "================================"
    echo "Blog Scraping Progress Monitor"
    echo "================================"
    echo ""

    # Count markdown files created
    md_count=$(find ../src/content/blog -name "*.md" -type f | wc -l)
    echo "Markdown files created: $md_count / 609"

    # Show percentage
    percentage=$(echo "scale=1; ($md_count / 609) * 100" | bc)
    echo "Progress: ${percentage}%"

    # Show last few lines of log
    echo ""
    echo "Recent activity:"
    echo "---------------"
    tail -10 full_scrape.log 2>/dev/null | head -5

    echo ""
    echo "Press Ctrl+C to exit monitoring"

    sleep 10
done
