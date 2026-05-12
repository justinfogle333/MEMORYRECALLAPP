# Critical Domains Remediation Plan
**Global Sales Force GEO Sprint Plan**

**Date:** March 21, 2026  
**Prepared for:** Web Development & Technical SEO Team  
**Prepared by:** Manus AI  

---

## 1. Executive Summary

During the initial Generative Engine Optimization (GEO) audit of the 14-brand portfolio, three domains were flagged as requiring critical, immediate attention: `kerbmoving.com`, `ldmovers.com`, and `usa-autotransport.com`. A live diagnostic audit conducted on March 21, 2026, confirmed severe technical issues ranging from parked domains blocking AI crawlers to missing mobile viewport tags.

This document outlines the exact state of each domain and provides a step-by-step remediation plan to bring them up to the baseline technical standard required for Phase 1 of the GEO Sprint Plan.

---

## 2. Remediation Plan: kerbmoving.com

### Current State Assessment
The domain `kerbmoving.com` is currently non-functional as a business asset. It is operating as a parked domain that redirects traffic to a generic content aggregator (`searchhounds.com`) displaying articles about streaming services in Germany. 

More critically for our GEO strategy, the domain actively blocks AI engines. The existing `llms.txt` file contains a `Disallow-Training: /` directive, and the server returns a `405 Method Not Allowed` error on standard HTTP requests. There is zero moving-related content, no schema markup, and no Google Business Profile connection.

### Required Actions

**Step 1: Un-park the Domain**
The domain must be reclaimed from the parking service and pointed to a dedicated hosting environment (e.g., WP Engine, where other portfolio sites are hosted).

**Step 2: Remove AI Blocking Directives**
Delete the existing `llms.txt` file that contains the `Disallow-Training` directive. Replace it with the standard portfolio `llms.txt` template.

**Step 3: Deploy a Minimum Viable Site (MVS)**
Until a full website can be designed, deploy a single-page landing site that includes:
- The brand name, logo, and contact phone number.
- A brief description of services (e.g., "Kerb Moving provides professional long-distance relocation services").
- The `MovingCompany` JSON-LD schema injected into the `<head>`.
- A footer link to the brand's Google Business Profile.

**Step 4: Update `robots.txt`**
Deploy the standard portfolio `robots.txt` file that explicitly allows `GPTBot`, `ClaudeBot`, `PerplexityBot`, and other major AI crawlers.

---

## 3. Remediation Plan: ldmovers.com

### Current State Assessment
The domain `ldmovers.com` successfully executes a 301 redirect to `longdistanceusamovers.com`. However, the destination site (`longdistanceusamovers.com`) suffers from several technical flaws that break the user experience and hinder AI discoverability.

The most glaring issue is broken internal routing. The "Blog" link in the main navigation returns a `404 Not Found` error. Furthermore, the site is completely missing an `llms.txt` file (returning a 404 error), and its `robots.txt` file lacks any explicit directives allowing AI crawlers. While the site does have some schema markup, it is missing the critical `MovingCompany` type required for local business entity recognition.

### Required Actions

**Step 1: Fix Broken Internal Links**
The development team must immediately investigate the WordPress permalink structure or page status for the Blog section. The navigation menu must be updated to point to a live URL, or the 404 page must be redirected to a functional resources page.

**Step 2: Implement AI Discoverability Files**
Create and upload the standard `llms.txt` file to the root directory of `longdistanceusamovers.com`. Update the existing `robots.txt` file to include the explicit `Allow` directives for all major AI user-agents.

**Step 3: Upgrade Schema Markup**
The current schema includes generic types like `WebPage` and `Organization`. The SEO team must inject the specific `MovingCompany` JSON-LD schema into the homepage `<head>` to establish the correct entity type for AI engines.

**Step 4: Add Missing Trust Signals**
Add a comprehensive meta description to the homepage. Create a dedicated FAQ section to provide structured answers for AI extraction, and add a visible link to the Google Business Profile in the site footer.

---

## 4. Remediation Plan: usa-autotransport.com

### Current State Assessment
Unlike the previous two domains, `usa-autotransport.com` is a live, functional, and well-designed website hosted on WP Engine. It features strong content, including a dedicated FAQ section, founder bios, and extensive city-specific service pages. It also successfully implements `MovingCompany` schema markup.

However, it suffers from a critical mobile rendering flaw: the HTML `<head>` is completely missing the standard viewport meta tag. Without this tag, mobile browsers will attempt to render the desktop version of the site, resulting in tiny text and a poor user experience—a factor that heavily penalizes search rankings. Additionally, the site lacks an `llms.txt` file and AI crawler directives in its `robots.txt`.

### Required Actions

**Step 1: Inject the Viewport Meta Tag (Critical)**
The development team must immediately add the following standard viewport meta tag to the `<head>` section of the global header template:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
Once deployed, the site must be tested on mobile devices to ensure the CSS media queries are triggering correctly and the layout is responsive.

**Step 2: Implement AI Discoverability Files**
Create and upload the standard `llms.txt` file to the root directory. Update the existing `robots.txt` file to explicitly allow `GPTBot`, `ClaudeBot`, `PerplexityBot`, and other AI crawlers.

**Step 3: Connect the Entity**
Add a visible link to the brand's Google Business Profile or Google Maps listing in the global footer to establish the entity connection required by AI engines.

---

## 5. Verification Protocol

Once the development team has executed the above remediation steps, the following verification checks must be performed:

| Domain | Verification Check | Expected Result |
|---|---|---|
| **kerbmoving.com** | Navigate to `https://kerbmoving.com` | Site loads a functional landing page (HTTP 200) instead of redirecting to searchhounds.com. |
| **kerbmoving.com** | Navigate to `https://kerbmoving.com/llms.txt` | File loads and does NOT contain `Disallow-Training`. |
| **ldmovers.com** | Click "Blog" in navigation on destination site | Page loads successfully (HTTP 200) with no 404 error. |
| **ldmovers.com** | Check schema on destination site | Google Rich Results Test confirms valid `MovingCompany` schema. |
| **usa-autotransport.com** | Inspect page source | `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is present in the `<head>`. |
| **usa-autotransport.com** | Load site on mobile device | Site scales correctly and is fully readable without horizontal scrolling. |
