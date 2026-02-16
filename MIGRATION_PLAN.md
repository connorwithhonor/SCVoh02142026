# Santa Clarita Open Houses - Domain Migration Plan

## 🎯 Goal
Migrate **santaclaritaopenhouses.com** from iHouseWeb to Netlify with zero SEO penalty and preserve all traffic.

---

## 📋 Pre-Migration Checklist

### 1. **Current State Audit** ✅
- [x] 609 blog posts migrated and cleaned
- [x] Internal links updated to new routes
- [x] Schema validation working
- [x] Dev site running successfully

### 2. **Build & Test**
- [ ] Run production build: `npm run build`
- [ ] Test build locally: `npm run preview`
- [ ] Verify all 609 blog posts load correctly
- [ ] Test navigation and internal links
- [ ] Check mobile responsiveness

---

## 🚀 Migration Steps

### Phase 1: Setup Netlify (Before DNS Change)

1. **Create Netlify Account & Deploy**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli

   # Login to Netlify
   netlify login

   # Deploy to Netlify
   netlify init
   ```

2. **Configure Build Settings in Netlify**
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Node version: 18 or higher

3. **Get Netlify Subdomain**
   - Netlify will give you: `your-site-name.netlify.app`
   - Test this thoroughly before proceeding

### Phase 2: Setup 301 Redirects (CRITICAL for SEO)

4. **Create Redirect Rules**

   Create `public/_redirects` file:
   ```
   # Redirect all old blog URLs to new structure
   /blog/:slug  /blog/:slug  200

   # Redirect old pages to new routes
   /contact  /contact  200
   /free-market-analysis  /contact  301
   /santa-clarita-market-report  /blog  301
   /active-listings  /  301
   /mortgage-rates  /blog  301
   /advanced-search  /  301
   /dream-home-finder  /contact  301
   /testimonials  /  301
   /about  /  301

   # Catch-all: redirect any unmatched to home
   /*  /  404
   ```

5. **Create `netlify.toml` Configuration**
   ```toml
   [build]
     command = "npm run build"
     publish = "dist"

   [[redirects]]
     from = "/blog/*"
     to = "/blog/:splat"
     status = 200

   [[headers]]
     for = "/*"
     [headers.values]
       X-Frame-Options = "DENY"
       X-XSS-Protection = "1; mode=block"
       X-Content-Type-Options = "nosniff"
   ```

### Phase 3: DNS Configuration

6. **Before Changing DNS - Document Current Setup**
   - Login to current domain registrar
   - Screenshot current DNS settings
   - Note all A records, CNAME records, MX records (email!)
   - **IMPORTANT**: Save email (MX) records - don't lose email!

7. **Add Custom Domain in Netlify**
   - Go to Netlify Dashboard → Domain Settings
   - Add `santaclaritaopenhouses.com`
   - Add `www.santaclaritaopenhouses.com`
   - Netlify will provide DNS records

8. **Update DNS Records**

   At your domain registrar (GoDaddy, Namecheap, etc.):

   **Option A: Use Netlify DNS (Recommended)**
   - Change nameservers to Netlify's:
     ```
     dns1.p01.nsone.net
     dns2.p01.nsone.net
     dns3.p01.nsone.net
     dns4.p01.nsone.net
     ```

   **Option B: Keep Current DNS, Add Records**
   - A Record: `@` → Netlify's IP (from dashboard)
   - CNAME: `www` → `your-site.netlify.app`

   **⚠️ CRITICAL**: Re-add MX records for email!

### Phase 4: SSL/HTTPS Setup

9. **Enable HTTPS in Netlify**
   - Netlify auto-provisions SSL certificate
   - Force HTTPS redirect
   - Wait for certificate (can take up to 24 hours)

### Phase 5: SEO Preservation

10. **Submit to Search Engines**
    ```
    Create sitemap.xml (Astro does this automatically)
    ```

11. **Update Google Search Console**
    - Add new property for Netlify domain
    - Submit sitemap: `https://santaclaritaopenhouses.com/sitemap-index.xml`
    - Monitor for crawl errors

12. **Set Up Google Analytics** (if using)
    - Add tracking code to `src/layouts/BlogPost.astro`
    - Verify tracking works

### Phase 6: Inform iHouseWeb

13. **Coordinate with iHouseWeb**
    - Email them 1 week before migration
    - Request they keep old site live for 30 days as backup
    - Ask for final database export/backup
    - Request 301 redirect from old hosting to new domain (if possible)

---

## 🔍 Post-Migration Checklist

### Immediate (Day 1)
- [ ] Verify site loads at santaclaritaopenhouses.com
- [ ] Test all 609 blog posts load
- [ ] Check SSL certificate is active
- [ ] Test contact forms (if any)
- [ ] Verify social media links work
- [ ] Test site on mobile devices

### Week 1
- [ ] Monitor Google Search Console for errors
- [ ] Check Google Analytics traffic
- [ ] Test email is still working
- [ ] Monitor site performance in Netlify
- [ ] Check for 404 errors in Netlify analytics

### Week 2-4
- [ ] Monitor search rankings
- [ ] Track organic traffic trends
- [ ] Fix any discovered broken links
- [ ] Update social media profiles with new site
- [ ] Update Google Business Profile

---

## 📊 SEO Impact Minimization

### Best Practices We're Following:
✅ **301 Redirects**: All old URLs redirect to new ones
✅ **Content Preservation**: All 609 blog posts migrated
✅ **URL Structure**: Keeping `/blog/post-name` format
✅ **Meta Data**: All titles, descriptions preserved
✅ **Source URLs**: Stored in frontmatter for redirect mapping
✅ **Sitemap**: Astro generates automatically
✅ **HTTPS**: SSL certificate from day 1

### Expected Impact:
- **Traffic dip**: 10-20% for 2-4 weeks (normal)
- **Recovery**: Full recovery in 4-8 weeks
- **Rankings**: Minimal impact with proper redirects

---

## 🆘 Rollback Plan

If something goes wrong:

1. **Immediate Rollback** (within 48 hours)
   - Change DNS back to old hosting
   - TTL is usually 3600 seconds (1 hour)

2. **Email Issues**
   - Re-add MX records immediately
   - Email typically recovers within minutes

3. **Contact Support**
   - iHouseWeb support
   - Netlify support (support@netlify.com)
   - Domain registrar support

---

## 📝 Important URLs to Track

### Current Site (iHouseWeb)
- Main: https://www.santaclaritaopenhouses.com
- Blog: https://www.santaclaritaopenhouses.com/blog

### New Site (Netlify)
- Staging: https://[your-site].netlify.app
- Production: https://santaclaritaopenhouses.com (after DNS)

### Admin Panels
- Netlify Dashboard: https://app.netlify.com
- Domain Registrar: [Your domain registrar URL]
- Google Search Console: https://search.google.com/search-console

---

## ⏱️ Timeline Estimate

| Phase | Duration | Status |
|-------|----------|--------|
| Build & Test | 1-2 days | ⏳ Pending |
| Setup Netlify | 1 hour | ⏳ Pending |
| Create Redirects | 2 hours | ⏳ Pending |
| DNS Change | 5 minutes | ⏳ Pending |
| DNS Propagation | 1-48 hours | ⏳ Pending |
| SSL Setup | 1-24 hours | ⏳ Pending |
| Monitoring | 30 days | ⏳ Pending |

**Total**: 3-5 days for full migration + 30 days monitoring

---

## 🎓 Next Steps

1. **Run**: `npm run build` to test production build
2. **Review**: This migration plan thoroughly
3. **Backup**: Get final backup from iHouseWeb
4. **Schedule**: Pick migration date (avoid weekends/holidays)
5. **Deploy**: Follow Phase 1 steps above

---

## 📞 Support Contacts

- **Netlify Support**: support@netlify.com
- **iHouseWeb**: [Contact info]
- **Domain Registrar**: [Contact info]
- **Developer** (Me/Claude): Available for questions

---

## ✅ Success Criteria

Migration is successful when:
- [ ] Site loads at main domain
- [ ] All 609 blog posts accessible
- [ ] No major SEO ranking drops after 2 weeks
- [ ] Email still works
- [ ] Forms work (if applicable)
- [ ] SSL certificate active
- [ ] Google Search Console shows no critical errors

---

**Last Updated**: February 16, 2026
**Status**: Ready for Build & Test Phase
