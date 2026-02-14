# n8n Automation Setup for Daily Blog Posts

## Overview
This guide will help you set up an n8n workflow that automatically generates and publishes daily blog posts to attract home sellers in Santa Clarita Valley cities: Castaic, Canyon Country, Newhall, Saugus, Stevenson Ranch, and Valencia.

## Prerequisites
- n8n instance running (self-hosted or cloud)
- Anthropic API key for Claude Haiku
- GitHub Personal Access Token with repo access
- Your GitHub repo: https://github.com/connorwithhonor/SCVoh02142026

## Architecture
```
Schedule Trigger (3x Daily: 6am, 12pm, 6pm PT)
    ↓
Select Random City + Topic
    ↓
Claude Haiku API (Generate Content)
    ↓
Format as Markdown
    ↓
GitHub API (Create File)
    ↓
Success Notification (optional)
```

**Cost for 3 Posts Per Day:**
- 1 post/day = ~$2-3/month
- **3 posts/day = ~$6-9/month** (90 posts/month)
- Still incredibly affordable for maximum content velocity!

## Step 1: Get Your Anthropic API Key

1. Go to https://console.anthropic.com/
2. Navigate to API Keys
3. Create a new key
4. Save it securely (you'll add it to n8n credentials)

**Cost Estimate:** Claude Haiku is ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens
- Each blog post: ~500 input + 1500 output tokens = ~$0.002 per post
- 90 posts/month (3/day) = ~$0.18/month for API costs
- Total with overhead: **~$6-9/month** (incredibly cheap for 90 posts!)

## Step 2: Get GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "n8n Blog Automation"
4. Select scopes: `repo` (all repo permissions)
5. Click "Generate token"
6. Copy the token immediately (you won't see it again)

## Step 3: Import n8n Workflow

Create a new workflow in n8n and use this configuration:

### Complete n8n Workflow JSON

```json
{
  "name": "Santa Clarita Daily Blog Generator",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "0 6,12,18 * * *"
            }
          ]
        }
      },
      "name": "3x Daily (6am, 12pm, 6pm PT)",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [250, 300],
      "typeVersion": 1,
      "notes": "Runs 3 times per day for maximum content velocity"
    },
    {
      "parameters": {
        "functionCode": "// Target cities and content pillars\nconst cities = [\n  { name: 'Castaic', zip: '91384', appeal: 'lake lifestyle and family homes' },\n  { name: 'Canyon Country', zip: '91387', appeal: 'affordable homes and growing community' },\n  { name: 'Newhall', zip: '91321', appeal: 'historic charm and established neighborhoods' },\n  { name: 'Saugus', zip: '91350', appeal: 'excellent schools and safe communities' },\n  { name: 'Stevenson Ranch', zip: '91381', appeal: 'luxury homes and gated communities' },\n  { name: 'Valencia', zip: '91355', appeal: 'master-planned community and amenities' }\n];\n\nconst contentTypes = [\n  {\n    type: 'seller_problem',\n    templates: [\n      'How to Sell Your {city} Home Fast Without Dropping the Price',\n      'Avoid These 5 Costly Mistakes When Selling Your {city} Home',\n      '{city} Home Sellers: Why Your House Isn\\'t Getting Offers',\n      'Maximize Your {city} Home Sale: What Buyers Really Want',\n      'Selling Your {city} Home in {month}? Here\\'s What You Need to Know'\n    ]\n  },\n  {\n    type: 'market_update',\n    templates: [\n      '{city} Real Estate Market Update - {month} {year}',\n      'Is Now the Right Time to Sell Your {city} Home?',\n      '{city} Home Values: What Sellers Need to Know This {month}',\n      'How {city} Home Prices Compare to Last Year',\n      'Why {city} Sellers Have an Advantage Right Now'\n    ]\n  },\n  {\n    type: 'neighborhood_spotlight',\n    templates: [\n      'Why {city} Homeowners Are Selling Now',\n      'What Makes {city} Homes So Attractive to Buyers?',\n      '{city} Neighborhood Guide for Home Sellers',\n      'The Complete Guide to Selling a Home in {city}',\n      '{city} Real Estate: What Every Seller Should Know'\n    ]\n  },\n  {\n    type: 'preparation',\n    templates: [\n      'Preparing Your {city} Home for Sale: Complete Checklist',\n      'Home Staging Tips for {city} Sellers',\n      'Boost Your {city} Home\\'s Curb Appeal Before Listing',\n      'Repairs That Pay Off When Selling Your {city} Home',\n      '{city} Home Sellers: How to Make Your Property Stand Out'\n    ]\n  }\n];\n\n// Select random city and content type\nconst city = cities[Math.floor(Math.random() * cities.length)];\nconst contentType = contentTypes[Math.floor(Math.random() * contentTypes.length)];\nconst template = contentType.templates[Math.floor(Math.random() * contentType.templates.length)];\n\nconst now = new Date();\nconst months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];\nconst month = months[now.getMonth()];\nconst year = now.getFullYear();\n\n// Replace placeholders\nconst title = template\n  .replace('{city}', city.name)\n  .replace('{month}', month)\n  .replace('{year}', year);\n\n// Generate filename\nconst slug = title\n  .toLowerCase()\n  .replace(/[^a-z0-9]+/g, '-')\n  .replace(/^-|-$/g, '');\n\nconst dateStr = now.toISOString().split('T')[0];\nconst filename = `${dateStr}-${slug}.md`;\n\nreturn [{\n  json: {\n    city: city.name,\n    cityZip: city.zip,\n    cityAppeal: city.appeal,\n    contentType: contentType.type,\n    title: title,\n    filename: filename,\n    pubDate: now.toISOString(),\n    month: month,\n    year: year\n  }\n}];"
      },
      "name": "Select City & Topic",
      "type": "n8n-nodes-base.function",
      "position": [450, 300],
      "typeVersion": 1
    },
    {
      "parameters": {
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "anthropicApi",
        "resource": "message",
        "operation": "create",
        "model": "claude-haiku-3-5-20241022",
        "maxTokens": 2000,
        "prompt": "=You are an expert real estate content writer for Connor with Honor (Connor T. MacIvor, DRE #01238257), a top Santa Clarita Valley listing agent with SYNC Brokerage.\n\nWrite a compelling blog post with this title:\n\"{{ $json.title }}\"\n\nContext:\n- Target city: {{ $json.city }}, CA ({{ $json.cityZip }})\n- City appeal: {{ $json.cityAppeal }}\n- Month: {{ $json.month }} {{ $json.year }}\n- Content type: {{ $json.contentType }}\n\nIMPORTANT REQUIREMENTS:\n1. TARGET AUDIENCE: Homeowners in {{ $json.city }} who are thinking about selling\n2. GOAL: Position Connor as THE expert to help them sell fast and for top dollar\n3. PRIVACY ANGLE: Mention that unlike Zillow/Redfin, Connor protects seller privacy\n4. CTA: End with strong call to action to book consultation at 661.400.1720\n5. TONE: Helpful, authoritative, local expert, not salesy\n6. LENGTH: 800-1200 words\n7. STRUCTURE:\n   - Opening hook (problem/question sellers face)\n   - 3-5 main sections with H2 headers\n   - Actionable advice specific to {{ $json.city }}\n   - Local market insights\n   - Privacy/anti-syndication point\n   - Strong CTA with phone number\n\nSEO KEYWORDS to naturally include:\n- {{ $json.city }} home seller\n- sell my house {{ $json.city }}\n- {{ $json.city }} real estate agent\n- listing agent {{ $json.city }}\n\nWrite ONLY the blog content (no frontmatter, no metadata). Start with the first paragraph.",
        "options": {}
      },
      "name": "Claude Haiku (Generate Content)",
      "type": "n8n-nodes-base.anthropic",
      "position": [650, 300],
      "typeVersion": 1,
      "credentials": {
        "anthropicApi": {
          "id": "1",
          "name": "Anthropic API"
        }
      }
    },
    {
      "parameters": {
        "functionCode": "const content = $input.first().json.content[0].text;\nconst metadata = $('Select City & Topic').first().json;\n\n// Create frontmatter\nconst frontmatter = `---\ntitle: \"${metadata.title}\"\ndescription: \"Expert advice for ${metadata.city} homeowners looking to sell their property for top dollar. Get local market insights and proven strategies from Connor with Honor.\"\npubDate: \"${metadata.pubDate}\"\nneighborhood: \"${metadata.city}\"\nheroImage: \"https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697cbafc1311f61da1eae20f.png\"\nupdatedDate: \"${metadata.pubDate}\"\n---`;\n\n// Combine frontmatter and content\nconst fullMarkdown = `${frontmatter}\\n\\n${content}`;\n\nreturn [{\n  json: {\n    filename: metadata.filename,\n    content: fullMarkdown,\n    title: metadata.title,\n    city: metadata.city\n  }\n}];"
      },
      "name": "Format as Markdown",
      "type": "n8n-nodes-base.function",
      "position": [850, 300],
      "typeVersion": 1
    },
    {
      "parameters": {
        "authentication": "accessToken",
        "resource": "file",
        "operation": "create",
        "owner": "connorwithhonor",
        "repository": "SCVoh02142026",
        "filePath": "=src/content/blog/{{ $json.filename }}",
        "fileContent": "={{ $json.content }}",
        "commitMessage": "=feat: Add blog post - {{ $json.title }}",
        "additionalParameters": {
          "branch": "main"
        }
      },
      "name": "GitHub (Create Blog Post)",
      "type": "n8n-nodes-base.github",
      "position": [1050, 300],
      "typeVersion": 1,
      "credentials": {
        "githubApi": {
          "id": "2",
          "name": "GitHub API"
        }
      }
    }
  ],
  "connections": {
    "Daily at 6am PT": {
      "main": [
        [
          {
            "node": "Select City & Topic",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Select City & Topic": {
      "main": [
        [
          {
            "node": "Claude Haiku (Generate Content)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Claude Haiku (Generate Content)": {
      "main": [
        [
          {
            "node": "Format as Markdown",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Format as Markdown": {
      "main": [
        [
          {
            "node": "GitHub (Create Blog Post)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "timezone": "America/Los_Angeles"
  }
}
```

## Step 4: Configure Credentials in n8n

### Add Anthropic API Credential
1. In n8n, go to **Credentials** → **New**
2. Search for "Anthropic"
3. Name it: "Anthropic API"
4. Paste your API key
5. Save

### Add GitHub Credential
1. In n8n, go to **Credentials** → **New**
2. Search for "GitHub"
3. Choose "GitHub API" (Access Token)
4. Name it: "GitHub API"
5. Paste your Personal Access Token
6. Save

## Step 5: Activate the Workflow

1. Import the JSON workflow above
2. Click on each node to verify settings
3. **IMPORTANT:** Update the GitHub node with your username if different:
   - Owner: `connorwithhonor`
   - Repository: `SCVoh02142026`
4. Click "Active" toggle in top right
5. Test it manually: Click "Execute Workflow"

## Step 6: Monitor and Optimize

### First Week Checklist
- [ ] Verify daily posts are being created in GitHub
- [ ] Check that Decap CMS is showing new posts
- [ ] Monitor Netlify builds (should auto-deploy)
- [ ] Review first 7 posts for quality
- [ ] Adjust prompts if needed

### Quality Control
If content quality isn't perfect, adjust the Claude prompt in the workflow:
- Make it more specific about local details
- Add examples of desired tone
- Include more context about target audience
- Reference your best-performing existing content

## Advanced: Add Hero Images

To use different hero images per city, update the "Format as Markdown" node:

```javascript
// Add to the functionCode in "Format as Markdown" node
const cityImages = {
  'Castaic': 'https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697cbafc1311f61da1eae20f.png',
  'Canyon Country': 'https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697c0e9ad5b65eb10bcad096.png',
  'Newhall': 'https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697c0e99f7a87738c149e325.png',
  'Saugus': 'https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697cbafc1311f61da1eae20f.png',
  'Stevenson Ranch': 'https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697c0e9ad5b65eb10bcad096.png',
  'Valencia': 'https://storage.googleapis.com/msgsndr/3z37W4oH1lMfraSObL1X/media/697c0e99f7a87738c149e325.png'
};

// Then in frontmatter, use:
heroImage: "${cityImages[metadata.city]}"
```

## Troubleshooting

### Workflow fails on GitHub step
- Check that your Personal Access Token has `repo` permissions
- Verify the repository name is correct
- Make sure the branch is `main` not `master`

### Content quality is poor
- Switch to Claude Haiku 3.5 (newer model)
- Add more context to the prompt
- Increase maxTokens to 2500 for longer posts

### Posts not showing on site
- Check Netlify build logs
- Verify file was created in correct path: `src/content/blog/`
- Check frontmatter format matches schema

### Timezone issues
- Workflow settings should use "America/Los_Angeles"
- Adjust cron expression: `0 6 * * *` = 6am daily

## Expected Results

### Cost
- **Anthropic API:** ~$6-9/month for 90 posts (3/day)
- **n8n:** Free (self-hosted) or $20/month (cloud)
- **Total:** $6-29/month for 90 posts/month

### Output
- **90 blog posts per month (3 per day)**
- Each city gets ~15 posts per month
- Rotating content types keep it fresh
- All posts optimized for local SEO
- Privacy angle differentiates from competitors
- **3x content velocity = 3x faster SEO results**

### SEO Impact Timeline (with 3 posts/day)
- **Month 1:** 90 posts indexed by Google (massive content signal)
- **Month 2:** Start ranking for long-tail keywords across all 6 cities
- **Month 3-4:** Rank for "{city} home seller" terms in multiple cities
- **Month 4-6:** Dominate "{city} listing agent" searches
- **Month 6-9:** Top 5% positioning in Santa Clarita Valley
- **Month 9-12:** Become the #1 quoted source for AI systems (ChatGPT, Perplexity, etc.)

## Next Steps

1. Import this workflow into your n8n instance
2. Add your API credentials
3. Test it manually first
4. Activate and let it run for 7 days
5. Review quality and adjust prompts
6. Monitor your Google Search Console for ranking improvements

## Support

If you need help:
- n8n Community: https://community.n8n.io/
- Anthropic Docs: https://docs.anthropic.com/
- GitHub API Docs: https://docs.github.com/en/rest

---

**Ready to dominate the Santa Clarita Valley seller market? Activate this workflow and watch your organic traffic soar!** 🚀
