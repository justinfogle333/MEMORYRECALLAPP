# 90-Day GEO Implementation Sprint Plan (v2.0)
**Global Sales Force AI Lead Generation Strategy (19-Brand Portfolio)**

**Date:** March 22, 2026  
**Prepared for:** Alex & Justin, Global Sales Force  
**Prepared by:** Manus AI  

---

## Executive Summary

This 90-day sprint plan is designed to transition Global Sales Force's entire 19-brand portfolio (14 domestic + 5 international) from traditional SEO to Generative Engine Optimization (GEO). The goal is to dominate AI search recommendations (ChatGPT, Perplexity, Google AI Overviews) when users ask for "best movers" or "best international movers." 

Based on our comprehensive audits, the domestic portfolio scores an average of **68/100**, while the international portfolio lags significantly at **50/100**. The international sites suffer from a near-zero AI Discoverability score (28%), meaning AI engines literally cannot find or read them. 

This sprint plan bridges that gap through a phased, 12-week execution strategy that integrates technical fixes, content upgrades, and the authentic Reddit community engagement strategy originally proposed by Alex—executed safely within FTC guidelines.

---

## Phase 1: Technical Foundation (Weeks 1-2)
**Goal:** Ensure all 19 domains are fully readable, crawlable, and understood by AI engines.

The audit revealed that 18 of 19 sites are missing `llms.txt` files, and 19 of 19 lack explicit AI crawler directives in their `robots.txt`. These are quick, high-impact fixes.

### Week 1: The "Quick Wins"
* **Task 1.1: Implement `llms.txt` Files.** Create and upload a standard `llms.txt` file to the root directory of all 19 sites to explicitly guide AI crawlers to the most important content.
* **Task 1.2: Update `robots.txt`.** Explicitly allow `GPTBot`, `ClaudeBot`, and `PerplexityBot` across all 19 domains.
* **Task 1.3: Link Google Business Profiles.** Add a clear, visible link to the respective Google Maps/GBP listing in the footer of the 16 sites currently missing them (13 domestic, 3 international).
* **Task 1.4: Fix Critical Domains.** 
  * Un-park `kerbmoving.com` (currently blocking AI training).
  * Resolve the redirect loop and broken blog link on `ldmovers.com`.
  * Investigate and fix the client-side crashing issues on `shepherdmovers.com`.
  * Fix the malformed HTML on `sunsetmoving.com`.

### Week 2: Advanced Schema & Structure
* **Task 2.1: Deploy Schema Markup.** Implement `MovingCompany` and `Organization` JSON-LD schema across the 7 sites missing it (4 domestic, 3 international).
* **Task 2.2: Mobile Optimization.** Fix the missing mobile viewport meta tag on `usa-autotransport.com`.
* **Task 2.3: Meta Descriptions.** Write and deploy factual, keyword-rich meta descriptions for the 7 sites currently missing them (including `shepherdmovers.com`).

**Phase 1 KPIs:** 100% technical compliance on the GEO Scorecard; successful crawls by GPTBot across all 19 domains.  
**Responsibility:** Web Development / Technical SEO Team.

---

## Phase 2: Content Foundation & Entity Authority (Weeks 3-4)
**Goal:** Provide the factual density and structured answers that AI engines rely on to generate recommendations.

AI engines prefer claim-based content and structured Q&A formats. Currently, 11 of the 19 sites lack dedicated FAQ sections.

### Week 3: The FAQ Build-Out
* **Task 3.1: FAQ Generation.** Write comprehensive, factual FAQ pages for all 19 brands. Focus on pricing, logistics, insurance, and specific routes (especially international customs/shipping for the 5 international brands).
* **Task 3.2: FAQ Schema.** Implement `FAQPage` schema on all newly created FAQ pages so AI engines can extract the answers directly.
* **Task 3.3: Claim-Based Formatting.** Audit homepage content and reformat key selling points into verifiable claims (e.g., "According to our 2025 data, our average cross-country delivery time is 4.2 days").

### Week 4: Entity Authority & Trust Signals
* **Task 4.1: "About Us" Upgrades.** Build out detailed "Team" or "About Us" pages with employee bios for the 10 sites missing them (6 domestic, 4 international). AI engines prioritize trustworthy sources with real people.
* **Task 4.2: Directory Consistency.** Audit Name, Address, and Phone (NAP) consistency across major directories for all 19 brands.
* **Task 4.3: Review Aggregation.** Ensure customer reviews are prominently displayed and marked up with `Review` schema on all sites.

**Phase 2 KPIs:** 19 fully optimized FAQ pages live; 100% completion of "About Us" pages; improved Entity Authority scores.  
**Responsibility:** Content Team / SEO Team.

---

## Phase 3: Authentic Community Engagement (Weeks 5-8)
**Goal:** Generate the "earned media" and third-party mentions that AI engines heavily weight, specifically targeting Reddit and local forums.

This phase executes Alex's original vision of Reddit engagement, but strictly adheres to the 90/10 Rule and FTC guidelines to avoid the $53,088 per violation penalty for astroturfing.

### Week 5: Account Setup & Observation
* **Task 5.1: Persona Creation.** Create individual Reddit accounts for 3-5 key team members (e.g., Justin). Do not use company names in the handles.
* **Task 5.2: Community Mapping.** Subscribe to Tier 1 (r/moving), Tier 2 (r/SameGrassButGreener), Tier 3 (city-specific), and International (r/expats, r/IWantOut) subreddits.
* **Task 5.3: Team Training.** Conduct a mandatory training session on FTC disclosure rules ("I work for [Brand Name]") and the 90/10 engagement rule.

### Week 6: Genuine Participation (The 90%)
* **Task 6.1: Daily Engagement.** Team members spend 15-30 minutes daily upvoting content and leaving thoughtful, non-promotional comments.
* **Task 6.2: Answering Questions.** Begin answering specific moving logistics questions (both domestic and international) without mentioning any of the 19 brands.
* **Task 6.3: Karma Building.** Goal is to reach 100+ comment karma per account to establish trust.

### Weeks 7-8: Subtle Promotion (The 10%)
* **Task 7.1: The First Mentions.** Begin mentioning the brands naturally when users explicitly ask for recommendations, always including the FTC disclosure.
* **Task 7.2: Host an AMA.** Coordinate an "Ask Me Anything" session in a relevant subreddit (e.g., "I manage international shipping logistics for Global Sales Force. AMA about moving overseas.").
* **Task 7.3: Multi-Brand Rotation.** Ensure different team members are rotating mentions of the 19 brands so no single brand appears to be spamming.

**Phase 3 KPIs:** 5 active, high-karma Reddit accounts; 20+ helpful comments per week; 1 successful AMA hosted; zero subreddit bans.  
**Responsibility:** Sales Team (Justin) / Marketing Team.

---

## Phase 4: Measurement, Scaling, & Content Leadership (Weeks 9-12)
**Goal:** Track AI visibility, scale what works, and publish original research to become the definitive source for AI citations.

### Weeks 9-10: Measurement & Analytics
* **Task 9.1: AI Visibility Tracking.** Run weekly prompts through ChatGPT, Perplexity, and Google AI Overviews (e.g., "Best cross country movers", "Best international movers to Europe") to track the Share of Voice for the 19 brands.
* **Task 9.2: Referral Tracking.** Monitor Google Analytics 4 for referral traffic originating from AI engines and Reddit.
* **Task 9.3: Lead Follow-Up Optimization.** Implement a strict 5-minute response SLA for all new leads generated, as industry data shows this increases booking likelihood by 21x.

### Weeks 11-12: Original Research & Scaling
* **Task 11.1: Publish Proprietary Data.** Aggregate data from the 19 brands to publish an original report (e.g., "The 2026 State of Global Relocation Costs"). AI engines love citing original statistics.
* **Task 11.2: Digital PR.** Pitch the original research to industry blogs and news outlets to generate high-authority backlinks.
* **Task 11.3: Sprint Review.** Conduct a 90-day review with Alex to assess ROI and plan the next quarter.

**Phase 4 KPIs:** Measurable increase in AI Share of Voice; publication of 1 original research report; 5-minute lead response time achieved.  
**Responsibility:** Marketing Team / Sales Team / Executive Leadership.

---

## Budget & Resource Estimates

| Resource | Estimated Cost / Time | Notes |
|----------|-----------------------|-------|
| **Technical SEO / Web Dev** | $3,500 - $5,500 | One-time cost for Phase 1 technical fixes across 19 sites. |
| **Content Creation (FAQs/Bios)** | $4,000 - $6,500 | Copywriting for 19 sites (approx. 38-50 pages of content). |
| **Community Engagement** | Internal Time | 3-5 team members dedicating 30 mins/day. No hard costs. |
| **AI Tracking Tools** | $150 - $300 / month | Subscriptions to tools like Semrush or specialized AI trackers. |
| **Total Estimated Hard Costs** | **$7,650 - $12,300** | Highly efficient given it covers 19 distinct brands. |

---

## The Bottom Line for Alex

This sprint plan takes your original instinct—that AI and Reddit are the future of lead generation—and turns it into a scalable, legal, and highly effective machine. By fixing the technical foundation first across all 19 domestic and international brands (Phase 1 & 2), we ensure that when our team engages on Reddit (Phase 3), the AI engines can actually connect those conversations back to our portfolio. This is how we build a moat that competitors with only one brand cannot cross.
