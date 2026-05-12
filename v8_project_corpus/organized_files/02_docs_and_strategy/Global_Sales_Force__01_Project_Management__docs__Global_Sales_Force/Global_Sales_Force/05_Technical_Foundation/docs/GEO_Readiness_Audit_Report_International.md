# Generative Engine Optimization (GEO) Readiness Audit
**International Portfolio**

**Date:** March 21, 2026  
**Prepared for:** Alex & Justin (Global Sales Force)  
**Prepared by:** Manus AI  

---

## 1. Executive Summary

Following the audit of the 14 domestic brands, a comprehensive Generative Engine Optimization (GEO) audit was conducted on the 5 international moving company websites owned by Global Sales Force. The goal of this audit is to determine how well these websites are optimized for AI-powered search engines (like ChatGPT, Perplexity, and Google AI Overviews).

**The International Portfolio Average Score is 50/100.** 

This is significantly lower than the domestic portfolio average (68/100). While the top performer (`myinternationalmovers.com`) is in decent shape, the bottom two sites (`sunsetmoving.com` and `shepherdmovers.com`) suffer from severe technical and content deficiencies that actively prevent AI engines from understanding or recommending them.

### The Scorecard at a Glance

| Rank | Domain | Score | Grade | Status |
|---|---|---|---|---|
| 1 | **myinternationalmovers.com** | 74/100 | B | Solid foundation, needs AI discoverability tweaks |
| 2 | **ilovemoving.com** | 64/100 | C | Good technicals, missing content depth |
| 3 | **schmidtmovers.com** | 54/100 | C | Missing FAQ, About page, and AI files |
| 4 | **sunsetmoving.com** | 43/100 | D | Malformed HTML, missing schema and meta tags |
| 5 | **shepherdmovers.com** | 15/100 | F | Critical failures, missing almost all GEO signals |

![Overall Scorecard](/home/ubuntu/intl_scorecard_overall.png)

---

## 2. Category Breakdown & Key Findings

The audit evaluated each site across 5 critical GEO categories. The heatmap below illustrates the specific strengths and weaknesses across the portfolio.

![Category Heatmap](/home/ubuntu/intl_scorecard_heatmap.png)

### A. Technical Foundation (Average: 18/20)
This is the strongest category. All 5 sites load successfully and use HTTPS. Four of the five sites have the required mobile viewport meta tag. 
* **Gap:** `sunsetmoving.com` and `shepherdmovers.com` have underlying code issues (malformed HTML and client-side errors) that make them difficult for automated crawlers to parse.

### B. AI Discoverability (Average: 7/25)
This is a critical failure point across the entire international portfolio. AI engines rely on specific files to understand how to crawl and cite a website.
* **Gap:** **Zero out of 5 sites** have an `llms.txt` file.
* **Gap:** **Zero out of 5 sites** have explicit AI crawler directives (like allowing `GPTBot`) in their `robots.txt` files.
* **Gap:** While 3 sites have some JSON-LD schema, only 2 (`myinternationalmovers.com` and `ilovemoving.com`) use the specific `MovingCompany` schema required for entity recognition.

### C. Content Quality (Average: 10/20)
AI engines pull answers directly from structured content like FAQs and service area pages.
* **Gap:** Only 1 site (`myinternationalmovers.com`) has a structured FAQ section.
* **Gap:** `shepherdmovers.com` is missing a meta description entirely.

### D. Trust & Authority (Average: 9/20)
AI models prioritize entities with verifiable real-world footprints.
* **Gap:** Only 2 sites link to a Google Business Profile.
* **Gap:** Only 1 site (`myinternationalmovers.com`) has an About page with real team information.

### E. Entity Authority (Average: 6/15)
This measures how well the site establishes itself as a distinct, authoritative business entity.
* **Gap:** `sunsetmoving.com` and `shepherdmovers.com` scored 0 in this category due to missing schema, missing team pages, and poor meta data.

---

## 3. Strategic Recommendations

To bring the international portfolio up to the standard required to dominate AI search recommendations, the following actions should be integrated into the 90-Day Sprint Plan:

### Immediate Technical Fixes (Weeks 1-2)
1. **Deploy `llms.txt`:** Create and upload an `llms.txt` file to the root directory of all 5 sites.
2. **Update `robots.txt`:** Add explicit `Allow` directives for major AI crawlers (GPTBot, ClaudeBot, PerplexityBot) to all 5 sites.
3. **Fix Schema:** Inject `MovingCompany` JSON-LD schema into `schmidtmovers.com`, `sunsetmoving.com`, and `shepherdmovers.com`.
4. **Code Audit:** Have the development team investigate the malformed HTML on `sunsetmoving.com` and the client-side crashing issues on `shepherdmovers.com`.

### Content & Authority Upgrades (Weeks 3-4)
1. **Build FAQ Pages:** Create dedicated, structured FAQ sections for the 4 sites currently missing them. This is the #1 way to feed answers directly to AI models.
2. **Connect Entities:** Add visible footer links to the respective Google Business Profiles for the 3 sites missing them.
3. **Establish Trust:** Build out proper "About Us" pages with team bios for the 4 sites lacking them.

By executing these fixes, the international portfolio can quickly close the gap and begin capturing high-converting AI referral traffic.
