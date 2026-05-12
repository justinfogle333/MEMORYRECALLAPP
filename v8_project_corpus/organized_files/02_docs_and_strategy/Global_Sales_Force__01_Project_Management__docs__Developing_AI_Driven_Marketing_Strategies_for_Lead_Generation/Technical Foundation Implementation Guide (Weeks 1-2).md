# Technical Foundation Implementation Guide (Weeks 1-2)
**Global Sales Force GEO Sprint Plan**

**Date:** March 18, 2026  
**Prepared for:** Web Development & Technical SEO Team  
**Prepared by:** Manus AI  

---

## 1. Executive Summary

This document provides the exact technical specifications and site-by-site instructions required to execute Phase 1 (Weeks 1-2) of the Global Sales Force GEO Sprint Plan. The objective is to ensure all 14 domains are fully crawlable, readable, and understood by AI engines (ChatGPT, Perplexity, Google AI Overviews).

Currently, the portfolio is largely invisible to AI engines due to missing `llms.txt` files, ambiguous `robots.txt` directives, and incomplete schema markup. This guide provides the code templates to fix these issues.

---

## 2. The `llms.txt` Implementation (Priority 1)

The `llms.txt` file is a new standard proposed in late 2024 that acts as a sitemap specifically for Large Language Models [1]. It provides AI crawlers with a clean, markdown-formatted summary of the site's most important content.

**Current Status:** 9 out of 14 sites are missing this file. `kerbmoving.com` has one, but it explicitly blocks AI training.

### Action Required
Create a plain text file named `llms.txt` (UTF-8 encoded, under 10KB) and upload it to the root directory of every domain (e.g., `https://crosscountrymovers.com/llms.txt`).

### `llms.txt` Master Template
*Note: Replace bracketed text with brand-specific details.*

```markdown
# [Brand Name]

> [Brand Name] is a professional moving company specializing in [Long-Distance / Auto Transport / Local] moves across the United States. We provide transparent pricing, expert logistics, and fully insured relocation services.

## Services
- [URL to Services Page]: Overview of our moving and packing services
- [URL to FAQ Page]: Frequently asked questions about moving costs, timelines, and logistics

## About
- [URL to About Page]: Company history, licensing information, and team bios
- [URL to Reviews Page]: Verified customer testimonials and ratings

## Optional
- [URL to Blog]: Moving tips, city guides, and relocation advice
```

---

## 3. The `robots.txt` Configuration (Priority 2)

AI companies use specific user-agents to crawl the web for training data and real-time search results [2]. If these bots are not explicitly allowed, they may skip the site.

**Current Status:** Most sites have a generic `User-agent: *` directive. While this technically allows all bots, explicitly allowing AI crawlers is the new best practice for GEO to ensure maximum visibility.

### Action Required
Update the `robots.txt` file in the root directory of all 14 domains to explicitly allow the major AI crawlers.

### `robots.txt` Master Template

```text
User-agent: *
Allow: /

# Explicitly allow AI crawlers for Generative Engine Optimization (GEO)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: https://[domain.com]/sitemap.xml
```

---

## 4. Schema Markup Implementation (Priority 3)

Schema markup (JSON-LD) is how we explicitly tell AI engines what a business does, where it operates, and how it is rated [3]. 

**Current Status:** 4 sites have no schema at all. The remaining 10 have basic schema, but many are missing the specific `MovingCompany` type.

### Action Required
Inject the following JSON-LD script into the `<head>` section of the homepage for all 14 domains.

### `MovingCompany` Schema Master Template

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MovingCompany",
  "name": "[Brand Name]",
  "url": "https://[domain.com]",
  "telephone": "[Phone Number]",
  "logo": "https://[domain.com]/logo.png",
  "image": "https://[domain.com]/hero-image.jpg",
  "description": "Professional [Long-Distance/Auto] moving services provided by [Brand Name].",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street Address]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[Zip Code]",
    "addressCountry": "US"
  },
  "areaServed": {
    "@type": "Country",
    "name": "United States"
  },
  "priceRange": "$$",
  "sameAs": [
    "[URL to Google Business Profile]",
    "[URL to Facebook Page]",
    "[URL to Yelp Page]"
  ]
}
</script>
```

---

## 5. Site-by-Site Action Checklist

This checklist details the specific technical gaps for each of the 14 domains based on the GEO audit.

| Domain | Missing `llms.txt` | Needs `robots.txt` Update | Missing Schema | Missing GBP Link | Special Fixes Required |
|---|---|---|---|---|---|
| **ultimatemovers.net** | No (Has file) | Yes | **YES** | Yes | Add meta description to homepage |
| **california-seattleexpress.com** | **YES** | Yes | No | Yes | None |
| **crosscountrymovers.com** | No (Has file) | Yes | No | Yes | None |
| **crosscountrymovingcompany.net** | No (Has file) | Yes | No | Yes | None |
| **eastcoastwestcoastmovers.com** | **YES** | Yes | No | Yes | None |
| **flatpriceautotransport.com** | **YES** | Yes | No | Yes | Add meta description to homepage |
| **kerbmoving.com** | No (Has file) | Yes | **YES** | Yes | **CRITICAL:** Remove AI blocking directives; un-park domain |
| **ldmovers.com** | **YES** | **YES (Missing)** | No | Yes | **CRITICAL:** Fix redirect loop to longdistanceusamovers.com |
| **longdistancemovers.com** | No (Has file) | Yes | No | Yes | None |
| **longdistancemovingexperts.com** | **YES** | Yes | No | Yes | Fix broken 'Cities' link in navigation |
| **longdistanceusamovers.com** | **YES** | Yes | **YES** | Yes | Add meta description to homepage |
| **state2statemovers.com** | **YES** | Yes | No | No (Has link) | None |
| **tricolongdistancemovers.com** | **YES** | Yes | **YES** | Yes | Add meta description to homepage |
| **usa-autotransport.com** | **YES** | Yes | No | Yes | **CRITICAL:** Add mobile viewport meta tag; add meta description |

---

## 6. Quality Assurance & Verification

Before marking Phase 1 complete, the development team must verify the following:
1. Navigate to `https://[domain.com]/llms.txt` for all 14 sites and verify the markdown renders correctly.
2. Navigate to `https://[domain.com]/robots.txt` and verify the AI crawler user-agents are present.
3. Run all 14 homepages through the **Google Rich Results Test** tool to verify the `MovingCompany` schema is valid and error-free.
4. Verify that clicking the Google Business Profile link in the footer successfully opens the correct Google Maps listing.

---

## References

[1] llms-txt. "The /llms.txt file." https://llmstxt.org/
[2] xSeek. "AI Robots.txt Guide: Managing All AI & LLM Crawlers." https://www.xseek.io/docs/ai-robots-txt-guide
[3] Schema.org. "MovingCompany." https://schema.org/MovingCompany
