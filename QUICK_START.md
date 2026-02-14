# Quick Start Guide - Get Running in 4 Hours

TL;DR version. Follow these steps to go from zero to automated content machine.

---

## ⚡ Step 1: Scrape Old Site (30 min)

```bash
cd "G:\Santa Clarita Open Houses Code 02142026\migration"
pip install -r requirements.txt
python scraper.py
```

**Answer the prompts:**
- URL: https://santaclaritaopenhouses.com
- Max pages: 100

**Wait for it to finish.**

---

## ⚡ Step 2: Migrate Content (15 min)

```bash
# Copy files
cp scraped_content/blog/*.md "../src/content/blog/"
cp scraped_content/_redirects "../public/"

# Test
cd ..
npm run dev
```

**Visit:** http://localhost:4321/blog

**Check:** Do posts look good? If yes, continue. If no, fix issues.

---

## ⚡ Step 3: Deploy (5 min)

```bash
git add .
git commit -m "Migrate old site content"
git push
```

**Netlify auto-deploys.** Check your temp URL.

---

## ⚡ Step 4: Get API Keys (15 min)

**Anthropic:**
1. Go to: https://console.anthropic.com/
2. Create account → API Keys → Create Key
3. Copy key (save somewhere safe)
4. Add $5 to account

**GitHub:**
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Name: `n8n automation`
4. Check: `repo`
5. Generate → Copy immediately

---

## ⚡ Step 5: n8n Setup (45 min)

**Open n8n:** http://localhost:5678

**Add Credentials:**
1. Settings → Credentials → New
2. Add "HTTP Header Auth" for Anthropic:
   - Name: `x-api-key`
   - Value: [your key]
3. Add "GitHub API" credential:
   - Access Token: [your token]

**Import Workflow:**
1. Workflows → New
2. Three dots → Import
3. Copy JSON from `N8N_AUTOMATION_SETUP.md` (line 54+)
4. Paste → Import

**Configure:**
1. Click "Claude Haiku" node → Select Anthropic credential
2. Click "GitHub" node → Select GitHub credential → Update repo name
3. Save (floppy disk icon)

**Test:**
1. Click "Execute Workflow" (play button)
2. Watch right panel for success
3. Check GitHub for new file
4. Check Netlify for build
5. Visit site - see new post

**Activate:**
- Toggle "Active" switch → turns green
- Done!

---

## ⚡ Step 6: DNS Cutover (30 min)

**In Netlify:**
1. Domain settings
2. Add custom domain: `santaclaritaopenhouses.com`
3. Follow instructions

**In Your Domain Registrar:**
1. Update A record: 75.2.60.5
2. Update CNAME: www → [your-site].netlify.app

**Wait 5-10 minutes.**

**Test:** https://santaclaritaopenhouses.com

---

## ⚡ Step 7: Submit to Google (10 min)

1. Go to: https://search.google.com/search-console
2. Add property: `santaclaritaopenhouses.com`
3. Verify (DNS method)
4. Submit sitemap: `https://santaclaritaopenhouses.com/sitemap-index.xml`

---

## ✅ You're Done!

**What happens now:**
- 3 posts publish per day (6am, 12pm, 6pm PT)
- 90 posts per month
- Google indexes everything
- Rankings climb monthly
- Phone starts ringing with seller leads

**Cost:** $6-9/month

**ROI:** One listing pays for 100+ years of automation

---

## 🆘 If Something Breaks

**Migration issues:**
- Read: `migration/README.md`

**n8n issues:**
- Read: `N8N_SELF_HOSTED_SETUP.md`
- Check Executions tab in n8n for errors

**DNS issues:**
- DNS can take 24-48 hours to propagate
- Use https://dnschecker.org to verify

**Netlify issues:**
- Check build logs in Netlify dashboard
- Most issues are dependency-related

---

## 📞 What's Next?

**Week 1:** Monitor n8n executions daily
**Week 2:** Review content quality
**Month 1:** 90 posts indexed
**Month 3:** Rankings start appearing
**Month 6:** Top 5% positioning
**Month 12:** #1 for most seller keywords

**Just keep the automation running. It compounds daily.**

---

**Need detailed instructions? Read:** `MASTER_ACTION_PLAN.md`

**Ready to dominate? Let's go!** 🚀
