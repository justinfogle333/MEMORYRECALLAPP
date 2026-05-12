# Agent Onboarding: Global Sales Force Project

**IMPORTANT:** Read this entire document before doing anything. This is the complete context transfer from a prior Manus session. You are continuing an active, multi-phase AI strategy project for a moving company conglomerate.

---

## 1. Who You're Working For

### Justin Fogel (a.k.a. "HaVoK")
- **Your direct user.** Everything you build goes through him.
- **Role:** Sales + AI/Tech Lead at Global Sales Force
- **Responsibilities:** Selling moving services AND building/deploying AI tools for the company
- **Compensation:** Flat fee for AI work on top of sales commission
- **Technical skill level:** Can code (Python, APIs), but prefers the most efficient/cost-effective approach
- **Access:** Being added to Claude for Business, dev group chat, and Asana workflow

### Alex (a.k.a. "Sasha")
- **Justin's boss.** The owner of ALL the companies.
- **Role:** CEO / Owner of the entire conglomerate
- **Style:** Action-oriented. Direct quote: *"Talking about it and brainstorming is one thing. Executing is something else."*
- **Priorities (in his own words, from meeting March 25, 2026):**
  1. Automated Review Solicitation Agent (get Google reviews across ~100 GBP locations)
  2. Social Media Automation (daily posting across all brands)
  3. AI Sales Assist (instant lead responses — leads currently going to voicemail)
  4. GEO Strategy (already hired an Israeli company + Serbian dev for this)

### Dev Team Structure
- **Canada-based supervisor** → Reviews tasks → Creates Asana tickets → 2 developers (Serbia) execute
- **Israeli GEO company** → Building AI agents that search AI platforms, find where results are pulled from, and auto-create pages on the websites. Started working ~March 24, 2026.
- **Serbian developer** → Setting up a WordPress AI plugin for automated daily content/page generation across all sites. All sites run WordPress.

---

## 2. The Company: Global Sales Force

Global Sales Force is the **sales team** for a moving company conglomerate owned by Alex. The conglomerate operates **19 brands** across two divisions:

### Domestic Division (14 Brands)

| # | Domain | Email | Category |
|---|--------|-------|----------|
| 1 | ultimatemovers.net | justin@ultimatemovers.net | Moving |
| 2 | california-seattleexpress.com | Justin@california-seattleexpress.com | Moving |
| 3 | crosscountrymovers.com | Justin@crosscountrymovers.com | Moving |
| 4 | crosscountrymovingcompany.net | Justin@crosscountrymovingcompany.net | Moving |
| 5 | eastcoastwestcoastmovers.com | Justin@eastcoastwestcoastmovers.com | Moving |
| 6 | flatpriceautotransport.com | Justin@flatpriceautotransport.com | Auto Transport |
| 7 | kerbmoving.com | Justin@kerbmoving.com | Moving (CRITICAL: parked domain) |
| 8 | ldmovers.com | Justin@ldmovers.com | Moving (redirects to longdistanceusamovers.com) |
| 9 | longdistancemovers.com | justin@longdistancemovers.com | Moving |
| 10 | longdistancemovingexperts.com | justin@longdistancemovingexperts.com | Moving |
| 11 | longdistanceusamovers.com | Justin@longdistanceusamovers.com | Moving |
| 12 | state2statemovers.com | Justin@state2statemovers.com | Moving |
| 13 | tricolongdistancemovers.com | Justin@tricolongdistancemovers.com | Moving |
| 14 | usa-autotransport.com | justin@usa-autotransport.com | Auto Transport |

### International Division (5 Brands)

| # | Domain | Brand Name | Type |
|---|--------|-----------|------|
| 1 | myinternationalmovers.com | My International Movers | International + Domestic + Auto |
| 2 | ilovemoving.com | I Love International Moving | International Moving |
| 3 | shepherdmovers.com | Shepherd International Movers | International (CRITICAL: 15/100 score) |
| 4 | sunsetmoving.com | Sunset International Shipping | International Moving |
| 5 | schmidtmovers.com | Schmidt International Relocations | International |

### CRM System
- **URL:** https://app.ultimatemoving.us/
- **Type:** Proprietary system, no public API
- **Workaround:** CSV export for now; browser automation planned for Phase 2
- **Key feature:** Already sends satisfaction text messages to customers and tracks happy/unhappy

### Competitor Intel
- **International Van Lines:** 1.5 stars on Yelp (1,600 reviews), but recommended by Forbes and Grok through paid manipulation and aggressive GEO tactics. This is who we're competing against.

---

## 3. What We've Already Done (Complete History)

### Phase 1: Strategic Analysis
- Analyzed Alex's original idea (post on Reddit to influence AI search results)
- Validated the core concept but identified FTC risks ($53,088 per violation for astroturfing)
- Pivoted to a legitimate GEO (Generative Engine Optimization) strategy
- **Deliverable:** `Strategic_Analysis_AI_Lead_Gen.md`

### Phase 2: GEO Readiness Audits
- Audited all 14 domestic websites for AI readiness → **Portfolio average: 68/100**
- Audited all 5 international websites → **Portfolio average: 50/100**
- Top performers: crosscountrymovers.com (90), state2statemovers.com (87)
- Critical failures: shepherdmovers.com (15), kerbmoving.com (25)
- **Deliverables:** `GEO_Readiness_Audit_Report.md`, `GEO_Readiness_Audit_Report_International.md`, CSV data, scorecard visualizations

### Phase 3: Technical Foundation Guide
- Created code templates for `llms.txt`, `robots.txt`, and `MovingCompany` JSON-LD schema
- Site-by-site checklist for all 19 domains
- **Deliverable:** `Technical_Foundation_Guide.md`

### Phase 4: Critical Domains Remediation
- Live audited kerbmoving.com (parked, redirects to spam), ldmovers.com (broken blog, redirect issues), usa-autotransport.com (missing viewport)
- Created step-by-step fix plans for each
- **Deliverable:** `Critical_Domains_Remediation_Plan.md`

### Phase 5: Community Engagement Playbook
- Identified target Reddit communities (r/moving 54K members, r/SameGrassButGreener, city-specific subs)
- Built the 90/10 posting strategy (90% helpful, 10% subtle promotion with FTC disclosure)
- Multi-brand coordination rules so 19 brands don't overlap
- 4-week account warm-up plan
- **Deliverable:** `Community_Engagement_Playbook.md`

### Phase 6: 90-Day Sprint Plan
- 12-week execution plan covering all 19 brands
- Phase 1 (Weeks 1-2): Technical Foundation
- Phase 2 (Weeks 3-4): Content Foundation & Entity Authority
- Phase 3 (Weeks 5-8): Authentic Community Engagement
- Phase 4 (Weeks 9-12): Measurement & Scaling
- Budget: $7,650 - $12,300 total hard costs
- **Deliverable:** `90_Day_GEO_Sprint_Plan_v2.md`

### Phase 7: Platform Policy Deep Dive
- Read the fine print of Google, Yelp, Facebook, BBB, Reddit, WordPress, and FTC policies
- Discovered the "Two-Step Decoupled" workaround: incentivize a survey (legal), then separately ask for a review (no incentive attached)
- Google bans incentivized reviews; Yelp bans even asking; FTC bans gating (routing happy to public, unhappy to private)
- **Deliverable:** `research_platform_policies.md`

### Phase 8: Review Agent (BUILT)
- Complete Python application — zero LLM token usage, entirely rules-based
- Tech stack: Python + SQLite + Twilio SMS + Tremendous gift card API
- Cost per customer: ~$15.02 (gift card + SMS)
- All 19 unit tests passed
- 5-day deployment plan created
- **Deliverables:** `review_agent/` (full code), `Review_Agent_Dev_Handoff.md`, `Justin_Review_Agent_Implementation_Guide.md`, `SAVED_TASK_5_Day_Review_Agent_Build.md`

### Presentations Created (4 total)
1. **Dominating AI Search: Lead Gen Strategy** — `manus-slides://cMJbxorsOjEUjLjFZ9dAoU`
2. **GEO Readiness Audit: Complete 19-Brand Portfolio** — `manus-slides://l7bASl757R6SXAaXaO1cHV`
3. **90-Day GEO Sprint Plan** — `manus-slides://1eNcAae9XgSLGuf3XAzOrt`
4. **The Automated Review Agent** — `manus-slides://p0uBEhicJrjn5qJhspXV3P`

---

## 4. What Still Needs to Be Done (Master Task List)

### Priority #1: Deploy the Review Agent
**Status:** Code built, 5-day deployment plan saved. Justin needs to:
- Set up Twilio + Tremendous accounts
- Create Google Form survey
- Map all 19 GBP review links
- Test with 5 real customers
- Go live with cron job

### Priority #2: Social Media Automation Pipeline
**Status:** Planning phase — NOT started yet
- Audit which brands have social accounts
- Create accounts for all missing brands
- Design 4-agent pipeline: Script Writer → Video Creator → Description Writer → Auto-Poster
- Build and deploy

### Priority #3: AI Sales Assist (Speed-to-Lead)
**Status:** Planning phase — NOT started yet
- Instant email response when lead enters CRM
- Immediate callback system
- 5-minute SLA implementation
- Industry data: leads contacted within 5 minutes are 21x more likely to book

### Priority #4: GEO Strategy Coordination
**Status:** Needs handoff package
- Share audit data with Israeli company + Serbian dev
- Ensure their work aligns with our findings

### Priorities #5-8: 90-Day Sprint Phases 1-4
- Technical Foundation fixes (llms.txt, robots.txt, schema, critical domains)
- Content Foundation (FAQs, About pages, claim-based formatting)
- Community Engagement (Reddit — playbook written, pending execution)
- Measurement & Scaling (AI visibility tracking, original research)

---

## 5. Rules and Guidelines

### FTC Compliance (Non-Negotiable)
- **NEVER** suggest fake reviews, fake Reddit posts, or astroturfing
- **NEVER** suggest review gating (routing happy customers to public sites, unhappy to private)
- Employees CAN post on Reddit but MUST disclose employment ("I work for [Brand Name]")
- Incentivized reviews are allowed ONLY if: (a) you don't require positive sentiment, (b) you send to ALL customers not just happy ones, (c) the incentive is disclosed
- Penalty for violations: $53,088 per incident
- The "Two-Step Decoupled" method is our approved approach: gift card for survey, separate non-incentivized review ask

### Google Review Policy
- No incentivized reviews (even if you don't ask for positive)
- No review gating
- Direct review links are allowed
- Asking for reviews is allowed (just no incentive)

### Yelp Policy
- Do NOT solicit Yelp reviews at all — even asking is against their policy

### Reddit Rules
- 90/10 rule: 90% helpful content, 10% self-promotion
- No coordinated inauthentic behavior
- Build karma before mentioning brands (100+ karma minimum)
- Never have two brand reps in the same thread

### Cost Efficiency
- Justin prefers the most token-efficient approach
- Avoid LLM-based solutions when rules-based logic works
- The Review Agent uses zero LLM tokens by design

### Communication Style
- Alex wants action, not brainstorming
- Justin is hands-on and will build things himself
- Present options with clear recommendations
- Always update the knowledge base after completing work

---

## 6. Key Research Findings

### Lead Generation for Moving Companies
- Industry average close rate: 39%
- Only 38% of movers respond to leads within 5 minutes
- Leads contacted within 5 minutes are 21x more likely to book
- SEO leads convert at 14.6% vs. 1.7% for traditional marketing
- 70% of people pick their mover from Google Maps

### GEO (Generative Engine Optimization)
- AI-powered search handles 40%+ of all queries globally
- Real-world case study: GEO implementation drove 100% increase in AI referrals and 315% surge in Google AI Overviews
- AI traffic converts at 3x the rate of traditional search
- Core tactics: structured data (JSON-LD), entity authority, claim-based content, FAQ optimization, llms.txt standard
- Free tools: HubSpot AEO Grader, Semrush AI Visibility Checker

### Portfolio GEO Scores
- **Domestic average:** 68/100
- **International average:** 50/100
- **Biggest gaps:** AI Discoverability (59% domestic, 28% international), Trust & Authority (59% domestic, 45% international)
- **Critical domains:** kerbmoving.com (25/100), shepherdmovers.com (15/100)

---

## 7. File Directory

All files are organized in the `Global_Sales_Force/` folder structure:

```
Global_Sales_Force/
├── README.md                          ← Master index
├── 01_Review_Agent/                   ← Code + docs for the review agent
├── 02_Social_Media_Automation/        ← (pending)
├── 03_AI_Sales_Assist/                ← (pending)
├── 04_GEO_Strategy_Coordination/      ← Strategy + Sprint Plan
├── 05_Technical_Foundation/           ← Audits + tech guides
├── 06_Content_Foundation/             ← (pending)
├── 07_Community_Engagement/           ← Reddit playbook
├── 08_Measurement_and_Scaling/        ← (pending)
└── _Master/                           ← Knowledge base, meeting notes, task lists
```

Additionally, all original files are included at the root level for direct access.

---

## 8. How to Continue This Project

When starting a new task on the work Manus account:

1. Upload this zip file
2. Say: *"Read AGENT_ONBOARDING.md first. This is a continuation of the Global Sales Force AI strategy project. All context, files, research, and code are in this zip. Read the Master_Task_List.md to see what needs to be done next."*
3. The new agent will have full context to continue from where we left off.

---

*Document created: March 26, 2026*
*Last session agent: Manus AI*
