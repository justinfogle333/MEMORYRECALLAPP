# Global Sales Force — Master Task List

**Date:** March 26, 2026
**Purpose:** A comprehensive, top-down checklist of all initiatives, projects, and tasks required to execute Alex's vision for AI integration and GEO strategy across the 19-brand portfolio.

---

## 1. Priority #1: Automated Review Solicitation Agent
*Status: Code Built, Ready for Deployment*

This is Alex's top priority to generate Google reviews across the ~100 Google Business Profile locations using the "Two-Step Decoupled" method to remain FTC and Google compliant.

- [ ] **Day 1:** Set up Twilio and Tremendous accounts, configure API keys, run test suite.
- [ ] **Day 2:** Create Google Form survey and connect the webhook to the server.
- [ ] **Day 3:** Map all 19 Google Business Profile review links in `config.py` and launch the server.
- [ ] **Day 4:** Export 5 real past customers from Ultimate Moving CRM and run a live test.
- [ ] **Day 5:** Switch Tremendous to production, set up the cron job, and go live.
- [ ] **Phase 2 (Future):** Build browser automation to extract completed moves from `app.ultimatemoving.us` automatically, eliminating the manual CSV export step.

---

## 2. Priority #2: Social Media Automation Pipeline
*Status: Planning Phase*

Alex wants automated social media posting across **every brand** (currently only Cross Country has active social media). The goal is daily posting using a 4-agent pipeline.

- [ ] **Audit:** Identify which of the 19 brands currently have social media accounts.
- [ ] **Account Creation:** Create Instagram, Facebook, and TikTok accounts for all missing brands.
- [ ] **Asset Collection:** Gather brand logos, existing move photos, and set up a shared folder for the team to drop new photos (e.g., branded t-shirt job site photos).
- [ ] **Pipeline Architecture:** Design the 4-agent workflow:
  - Agent 1: Script/Caption Writer
  - Agent 2: Video/Image Creator
  - Agent 3: Description & Hashtag Writer
  - Agent 4: Auto-Poster
- [ ] **Implementation:** Build and deploy the automation pipeline using tools like Make.com or custom Python scripts.
- [ ] **Launch:** Begin daily automated posting across all 19 brands.

---

## 3. Priority #3: AI Sales Assist (Speed-to-Lead)
*Status: Planning Phase*

Alex identified a critical gap: leads go to voicemail, and salespeople only call once or twice a day. Industry data shows leads contacted within 5 minutes are 21x more likely to book.

- [ ] **Audit:** Analyze current lead response times and identify the biggest bottlenecks.
- [ ] **Instant Email Response:** Implement an AI agent to send an immediate, personalized email response the second a lead enters the CRM.
- [ ] **Immediate Callback System:** Set up an AI voice agent or auto-dialer system to call leads immediately.
- [ ] **SLA Implementation:** Establish a strict 5-minute Speed-to-Lead SLA with automated alerts for the sales team.
- [ ] **Training:** Train the sales team on the new AI-assisted workflow.

---

## 4. GEO Strategy Coordination
*Status: Ongoing*

Alex has already hired an Israeli company for automated page creation and a Serbian developer for a WordPress AI content plugin. We need to ensure their work aligns with our audit findings.

- [ ] **Handoff Package:** Compile our GEO Readiness Audit, Technical Foundation Guide, and `llms.txt`/`robots.txt` templates.
- [ ] **Coordination:** Share the handoff package with the Israeli company and the Serbian developer via the Canada-based supervisor.
- [ ] **Alignment:** Ensure the Serbian developer's WordPress plugin generates content that follows our claim-based formatting and FAQ structure recommendations.

---

## 5. Technical Foundation Fixes (90-Day Sprint: Phase 1)
*Status: Pending Execution*

Fixing the technical plumbing so AI engines can actually read the 19 sites.

- [ ] **`llms.txt` Deployment:** Create and upload `llms.txt` files to all 19 domains.
- [ ] **`robots.txt` Update:** Explicitly allow AI crawlers (GPTBot, ClaudeBot, etc.) on all 19 domains.
- [ ] **GBP Linking:** Add Google Business Profile links to the footers of the 16 sites missing them.
- [ ] **Critical Domain Fixes:**
  - Un-park and rebuild `kerbmoving.com`.
  - Fix the redirect loop and 404 errors on `ldmovers.com`.
  - Fix the client-side crashing on `shepherdmovers.com`.
  - Fix malformed HTML on `sunsetmoving.com`.
- [ ] **Schema & Mobile:** Deploy `MovingCompany` schema where missing and fix the mobile viewport on `usa-autotransport.com`.

---

## 6. Content Foundation & Entity Authority (90-Day Sprint: Phase 2)
*Status: Pending Execution*

Building the structured content that AI engines pull answers from.

- [ ] **FAQ Build-Out:** Write and deploy comprehensive FAQ pages with `FAQPage` schema for all 19 brands.
- [ ] **"About Us" Upgrades:** Build out detailed team pages with employee bios for the 10 sites missing them.
- [ ] **Claim-Based Formatting:** Reformat homepage content into verifiable claims (e.g., "Average delivery time is 4.2 days").
- [ ] **Directory Consistency:** Audit and fix NAP (Name, Address, Phone) consistency across major directories.

---

## 7. Authentic Community Engagement (90-Day Sprint: Phase 3)
*Status: Pending Execution (Saved Task)*

Executing Alex's original vision of Reddit engagement, but legally and sustainably.

- [ ] **Playbook Elaboration:** Complete the deep-dive task to build the full Community Engagement Playbook (target subreddits, posting guidelines, compliance guardrails).
- [ ] **Account Setup:** Create Reddit accounts for 3-5 team members and begin the 4-week warm-up plan.
- [ ] **Daily Engagement:** Execute the 90/10 rule (90% helpful advice, 10% subtle promotion with FTC disclosure).
- [ ] **Multi-Brand Rotation:** Coordinate mentions so the 19 brands don't overlap or appear spammy.

---

## 8. Measurement & Scaling (90-Day Sprint: Phase 4)
*Status: Future*

- [ ] **AI Visibility Tracking:** Monitor Share of Voice on ChatGPT, Perplexity, and Google AI Overviews.
- [ ] **Original Research:** Publish a proprietary data report (e.g., "2026 State of Relocation Costs") to generate AI citations.
- [ ] **90-Day Review:** Conduct a comprehensive review with Alex to assess ROI and plan the next quarter.
