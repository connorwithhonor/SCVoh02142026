# Deployment Checklist - Santa Clarita Open Houses

## Pre-Deployment (Complete ✓)

- [x] All 609 blog posts migrated and cleaned
- [x] Links fixed (465 files updated)
- [x] Dates working correctly
- [x] Code blocks removed
- [x] Zillow disclaimers removed
- [x] Production build tested successfully (613 pages)
- [x] 608 redirects generated in `public/_redirects`
- [x] Netlify configuration completed (`netlify.toml`)
- [x] All changes committed to git

## Netlify Deployment Steps

### 1. Create Netlify Account & Site
```bash
# Install Netlify CLI (optional, can use web interface)
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize site (run from project root)
netlify init
```

**Or use Netlify Web Interface:**
1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Connect your Git repository (GitHub/GitLab/Bitbucket)
4. Configure build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Node version: 20

### 2. Test on Netlify Staging URL
- Netlify will provide a URL like: `your-site-name.netlify.app`
- Test thoroughly:
  - [ ] Homepage loads correctly
  - [ ] Blog index page shows all posts with dates
  - [ ] Individual blog posts load without errors
  - [ ] No black code blocks visible
  - [ ] Internal links work (click several blog-to-blog links)
  - [ ] Images load properly
  - [ ] Mobile responsive design works
  - [ ] Test 5-10 old blog URLs to verify redirects work

### 3. Configure Custom Domain

**In Netlify Dashboard:**
1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Enter: `santaclaritaopenhouses.com`
4. Netlify will provide DNS configuration

**DNS Configuration (at your domain registrar):**

**Option A: Use Netlify DNS (Recommended)**
- Change nameservers to Netlify's nameservers
- Netlify handles everything automatically
- Easiest for SSL/HTTPS setup

**Option B: Use Current DNS Provider**
Add these DNS records:
```
Type: A
Name: @ (or root/apex)
Value: 75.2.60.5

Type: CNAME
Name: www
Value: your-site-name.netlify.app
```

### 4. Enable HTTPS/SSL
- [ ] In Netlify: Site settings → Domain management → HTTPS
- [ ] Click "Verify DNS configuration"
- [ ] Click "Provision certificate" (automatic with Let's Encrypt)
- [ ] Enable "Force HTTPS" redirect
- [ ] Wait 24-48 hours for DNS propagation

### 5. Coordinate with iHouseWeb

**Before switching DNS:**
- [ ] Export any analytics data you need from old site
- [ ] Download any files/images not already migrated
- [ ] Document any special configurations on old hosting

**Communication with iHouseWeb:**
1. Inform them of planned migration date/time
2. Ask them to:
   - Keep old site running for 7 days as backup
   - Provide any final access needed
   - Confirm any contracts/billing to cancel

**Best Time to Switch:**
- Sunday night or early Monday morning (lowest traffic)
- Avoid holidays or peak real estate seasons

### 6. DNS Migration Day

**Step-by-step:**
1. [ ] Take final backup of old site
2. [ ] Verify Netlify staging site is 100% ready
3. [ ] Update DNS records (at 2am if possible)
4. [ ] Monitor for issues for 24 hours

**DNS Propagation:**
- Can take 1-48 hours for global propagation
- Use https://dnschecker.org to monitor propagation
- Test from multiple devices/networks

### 7. Post-Deployment Monitoring (First Week)

**Daily Checks:**
- [ ] Site loads correctly on desktop/mobile
- [ ] Run Google Search Console crawl
- [ ] Check Google Analytics for traffic patterns
- [ ] Monitor Netlify analytics for 404 errors
- [ ] Test contact forms (if any)
- [ ] Check several blog post redirects

**Search Console Updates:**
```
1. Google Search Console (https://search.google.com/search-console)
   - Add new property for Netlify domain if needed
   - Submit new sitemap: https://santaclaritaopenhouses.com/sitemap-index.xml
   - Request re-indexing of key pages

2. Bing Webmaster Tools
   - Submit sitemap
   - Request re-crawl

3. Social Media Updates
   - Update Facebook page URL (if different)
   - Update LinkedIn company profile
   - Update Instagram bio link
   - Update any email signatures
```

## Rollback Plan (If Needed)

If critical issues arise:

1. **Immediate:** Point DNS back to old hosting (iHouseWeb)
   - Change A record back to old IP address
   - Takes 1-24 hours to propagate

2. **Investigation:** Debug issue on Netlify staging
   - Use Netlify deploy previews
   - Check Netlify function logs
   - Review browser console errors

3. **Fix & Retry:** Once fixed, switch DNS again

## SEO Preservation Checklist

- [x] 608 individual blog post 301 redirects configured
- [x] Old URLs will redirect to new /blog/slug format
- [ ] Submit sitemap to Google Search Console
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Monitor Google Search Console for crawl errors (first 30 days)
- [ ] Check rankings for top 10 keywords (weekly for first month)

## Performance Optimization (Post-Launch)

- [ ] Run Lighthouse audit (aim for 90+ scores)
- [ ] Optimize images if needed (use Astro Image component)
- [ ] Enable Netlify Analytics for detailed insights
- [ ] Consider Netlify Forms for contact forms
- [ ] Set up Netlify Functions if needed for any server-side logic

## Ongoing Maintenance

**Monthly:**
- Review Netlify bandwidth/build minutes usage
- Check for broken links
- Update npm dependencies: `npm update`
- Review Google Analytics traffic sources

**Quarterly:**
- Review and update outdated blog posts
- Check SEO rankings
- Audit site performance
- Review and renew SSL certificate (automatic with Netlify)

## Support Contacts

**Netlify Support:**
- Documentation: https://docs.netlify.com
- Support: https://www.netlify.com/support/
- Community: https://answers.netlify.com

**Domain Registrar:**
- [Your domain registrar contact info]

**Emergency Rollback Contact:**
- iHouseWeb: [contact information]

---

## Current Status: ✅ READY FOR DEPLOYMENT

All technical work is complete. The site is production-ready and can be deployed to Netlify whenever you're ready to proceed with the domain migration.
