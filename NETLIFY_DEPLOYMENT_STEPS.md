# Netlify Deployment - Step by Step

## Step 1: Create Netlify Account & Connect GitHub

1. Go to **https://app.netlify.com/signup**
2. Click **"Sign up with GitHub"** (easiest option)
3. Authorize Netlify to access your GitHub account

## Step 2: Create New Site

1. Click **"Add new site"** button (top right)
2. Select **"Import an existing project"**
3. Choose **"Deploy with GitHub"**
4. Find and select your repository: **connorwithhonor/SCVoh02142026**
5. Netlify will show deployment settings

## Step 3: Configure Build Settings

**You should see these settings already filled in (from netlify.toml):**

- **Branch to deploy:** `main`
- **Build command:** `npm run build`
- **Publish directory:** `dist`
- **Node version:** 20 (set automatically)

**If you see empty fields, fill them in as shown above.**

Click **"Deploy site"** button

## Step 4: Wait for First Build

- Netlify will start building your site (takes 1-3 minutes)
- You'll see build logs scrolling
- Wait for "Site is live" message
- You'll get a temporary URL like: `random-name-123456.netlify.app`

## Step 5: Test Staging Site

1. Click the staging URL Netlify gives you
2. Test these pages:
   - Homepage: `https://your-site.netlify.app/`
   - Blog index: `https://your-site.netlify.app/blog`
   - A random blog post (click one from the blog page)
   - About page: `https://your-site.netlify.app/about`
   - Book page: `https://your-site.netlify.app/book`

3. Test a redirect (pick any old blog URL):
   - Try: `https://your-site.netlify.app/5-top-seller-mistakes-made-when-selling-santa-clarita-real-estate-in-2025`
   - Should redirect to: `https://your-site.netlify.app/blog/5-top-seller-mistakes-made-when-selling-santa-clarita-real-estate-in-2025`

## Step 6: Add Custom Domain

1. In Netlify dashboard, go to **Site settings** → **Domain management**
2. Click **"Add custom domain"**
3. Enter: `santaclaritaopenhouses.com`
4. Click **"Verify"**
5. Netlify will say "This domain is already registered"
6. Click **"Add domain"** to confirm

## Step 7: Configure DNS with Netlify Nameservers

1. Netlify will show you their nameservers (usually 4 of them)
2. They look like:
   ```
   dns1.p01.nsone.net
   dns2.p01.nsone.net
   dns3.p01.nsone.net
   dns4.p01.nsone.net
   ```
   **Copy these nameservers** - you'll need them for GoDaddy

3. **In GoDaddy** (the screenshot you showed):
   - Make sure "I'll use my own nameservers" is selected
   - Replace all 4 iHouseWeb nameservers with Netlify's nameservers
   - Click **"Save"**

## Step 8: Wait for DNS Propagation

- DNS changes take 1-48 hours to propagate (usually 2-6 hours)
- You can check progress at: **https://dnschecker.org**
- Enter `santaclaritaopenhouses.com` and check if it points to Netlify

## Step 9: Enable HTTPS/SSL

1. Once DNS propagates, go back to Netlify
2. **Site settings** → **Domain management** → **HTTPS**
3. Click **"Verify DNS configuration"**
4. Click **"Provision certificate"** (automatic with Let's Encrypt)
5. Wait 30 seconds - 2 minutes
6. Enable **"Force HTTPS"** toggle (redirects http to https)

## Step 10: Submit to Search Engines

1. **Google Search Console**: https://search.google.com/search-console
   - Add property: `santaclaritaopenhouses.com`
   - Verify ownership (Netlify makes this easy)
   - Submit sitemap: `https://santaclaritaopenhouses.com/sitemap-index.xml`

2. **Bing Webmaster Tools**: https://www.bing.com/webmasters
   - Add site
   - Submit sitemap

## Step 11: Monitor (First Week)

- [ ] Check Google Search Console daily for crawl errors
- [ ] Monitor traffic in Google Analytics
- [ ] Test 5-10 random old blog URLs to verify redirects work
- [ ] Check that all 609 blog posts are accessible

---

## Troubleshooting

### Build Fails on Netlify
- Check build logs for errors
- Most common: Node version mismatch (should be 20)
- Solution: Clear cache and retry deploy

### DNS Not Propagating
- Wait longer (can take 24-48 hours)
- Check with `nslookup santaclaritaopenhouses.com`
- Verify nameservers are correct in GoDaddy

### SSL Certificate Fails
- Make sure DNS is fully propagated first
- Netlify won't provision SSL until DNS points to them
- If stuck, contact Netlify support (very responsive)

### Redirects Not Working
- Check `public/_redirects` file exists in build output
- Netlify reads this automatically
- Test in incognito/private window (avoid cache)

---

## Current Status

✅ Code pushed to GitHub: https://github.com/connorwithhonor/SCVoh02142026
✅ All 609 blog posts ready
✅ 658 redirects configured
✅ SEO protection in place
✅ Production build tested and working

**Next:** Follow steps above to deploy to Netlify!
