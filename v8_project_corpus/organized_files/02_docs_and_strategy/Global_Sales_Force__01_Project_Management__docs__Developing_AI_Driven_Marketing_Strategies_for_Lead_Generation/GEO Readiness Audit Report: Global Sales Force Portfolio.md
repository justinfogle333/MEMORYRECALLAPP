
**Date:** March 18, 2026  
**Prepared for:** Alex & Justin, Global Sales Force  
**Prepared by:** Manus AI  

## Executive Summary

As part of the initiative to dominate AI search recommendations (ChatGPT, Perplexity, Google AI Overviews), an automated audit was conducted across all 14 domains in the Global Sales Force portfolio. The audit evaluated each site against 13 critical Generative Engine Optimization (GEO) factors, including schema markup, AI crawler accessibility, and content structure.

**The Good News:** The portfolio has a strong technical foundation. Almost all sites load quickly, use HTTPS, and are mobile-responsive. Furthermore, 10 out of 14 sites already have some form of schema markup implemented.

**The Critical Gap:** The portfolio is largely invisible to AI engines due to missing specific GEO signals. Most notably, 13 out of 14 sites lack a visible link to a Google Business Profile, 9 sites are missing the new `llms.txt` standard, and 7 sites lack structured FAQ content (which AI engines rely on heavily for answers).

---

## Portfolio Scorecard Overview

The 14 brands were scored out of 100 possible points based on their AI readiness. 

![Overall Scorecard](/home/ubuntu/scorecard_overall.png)

### Top Performers (Ready for Phase 2)
These sites have the strongest foundation and require the least amount of technical work before moving to content and community engagement strategies:
1. **crosscountrymovers.com** — 90/100 (A)
2. **state2statemovers.com** — 87/100 (A)
3. **crosscountrymovingcompany.net** — 82/100 (B)

### Critical Attention Required
These sites are currently blocking AI crawlers, failing to load properly, or missing almost all GEO signals:
12. **ldmovers.com** — 56/100 (C) *(Redirects to longdistanceusamovers.com with broken internal links)*
13. **longdistanceusamovers.com** — 47/100 (D) *(Missing schema, llms.txt, and FAQs)*
14. **kerbmoving.com** — 25/100 (F) *(Currently a parked domain lander that explicitly blocks AI training)*

---

## Category Performance Analysis

We evaluated the portfolio across five key categories. The chart below shows the average score across all 14 brands for each category.

![Category Averages](/home/ubuntu/scorecard_categories.png)

### 1. Technical Foundation (Average: 96%)
The portfolio excels here. Sites are secure (HTTPS), mobile-responsive, and load successfully. The only exception is `usa-autotransport.com`, which is missing a mobile viewport meta tag.

### 2. AI Discoverability (Average: 59%)
This is the most critical area for improvement. While 10 sites have schema markup, only a few use the specific `MovingCompany` or `FAQPage` schemas that AI engines prefer. 
- **9 sites** are missing an `llms.txt` file.
- **Most sites** have a `robots.txt` file that is ambiguous regarding AI crawlers (neither explicitly allowing nor blocking them).

### 3. Content Quality (Average: 69%)
AI engines look for factual density and clear answers. 
- **7 sites** are completely missing dedicated FAQ sections.
- **6 sites** are missing meta descriptions on their homepages, which AI engines sometimes use for quick summaries.

### 4. Trust & Authority (Average: 59%)
AI engines prioritize trustworthy sources. While almost all sites display customer reviews, **6 sites** lack a proper "About Us" or "Team" page with bios, which hurts the "Entity Authority" signal.

### 5. Local SEO (Average: 79%)
Most sites have dedicated service area pages, which is excellent. However, **13 out of 14 sites** fail to link directly to their Google Business Profile or Google Maps listing from the homepage, breaking a critical entity connection.

---

## Feature-by-Feature Heatmap

The heatmap below illustrates exactly which features are missing (red), partially implemented (orange), or fully implemented (green) across the portfolio.

![Feature Heatmap](/home/ubuntu/scorecard_heatmap.png)

---

## Prioritized Action Plan

To defend the 14-domain moat and start capturing AI search traffic, we recommend executing the following fixes in order of priority:

### Priority 1: The "Quick Wins" (Week 1)
These changes take minutes per site but have a massive impact on AI crawlability.
1. **Add `llms.txt` files:** Create and upload a standard `llms.txt` file to the root directory of the 9 missing sites.
2. **Update `robots.txt`:** Explicitly allow `GPTBot`, `ClaudeBot`, and `PerplexityBot` across all 14 domains.
3. **Link Google Business Profiles:** Add a clear link to the respective Google Maps/GBP listing in the footer of all 13 missing sites.