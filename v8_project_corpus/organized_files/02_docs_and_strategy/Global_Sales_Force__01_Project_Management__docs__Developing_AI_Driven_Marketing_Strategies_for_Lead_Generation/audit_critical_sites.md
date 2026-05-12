# Live Audit Findings - March 21, 2026

## 1. kerbmoving.com
- **Status:** PARKED DOMAIN. Redirects to searchhounds.com (a generic content aggregator). Not a functional moving company website.
- **robots.txt:** Exists. Has `User-agent: *` Allow: / and `LLM-Policy: /llms.txt`
- **llms.txt:** Exists but contains `Disallow-Training: /` — explicitly blocks AI training
- **HTTP response:** 405 Method Not Allowed on HEAD request (parked domain behavior)
- **Schema:** None
- **Content:** Zero moving-related content. Displays generic articles about streaming in Germany.
- **Severity:** CRITICAL — This domain is completely non-functional as a moving company website.

## 2. ldmovers.com
- **Status:** REDIRECTS to longdistanceusamovers.com (301 redirect works in browser)
- **ldmovers.com robots.txt:** MISSING (returns empty/405)
- **ldmovers.com llms.txt:** MISSING (returns empty/405)
- **longdistanceusamovers.com robots.txt:** Exists but has NO AI crawler directives. Only generic WP disallows.
- **longdistanceusamovers.com llms.txt:** MISSING (returns 404)
- **Internal links status:**
  - About Us: 200 OK (works)
  - Blog: 404 NOT FOUND (broken)
  - Cities Served: 200 OK (works)
- **Schema on longdistanceusamovers.com:** WebPage, BreadcrumbList, WebSite, Organization (NO MovingCompany schema)
- **Meta description:** Missing on homepage
- **FAQ:** None
- **GBP link:** None
- **Severity:** HIGH — Blog is broken, no llms.txt, no AI crawler directives, missing schema types.

## 3. usa-autotransport.com
- **Status:** LIVE and functional. HTTP 200. Hosted on WP Engine.
- **robots.txt:** Exists but has NO AI crawler directives. Standard WP disallows.
- **llms.txt:** MISSING (returns 404)
- **Viewport meta tag:** MISSING (confirmed via BeautifulSoup — returns None)
- **Meta description:** Present in HTML source per curl grep, but BeautifulSoup returns None (may be dynamically injected via JS)
- **Schema:** Has MovingCompany, AggregateRating, ContactPoint, OpeningHoursSpecification — GOOD
- **FAQ:** YES — Has a dedicated FAQ section on homepage
- **About page:** YES — Has founder bios
- **Cities served:** YES — Extensive city pages
- **GBP link:** MISSING
- **Mobile rendering:** Site appears to render OK in desktop browser but missing viewport meta tag means mobile devices won't scale properly
- **Severity:** MEDIUM — Functional site with good content, but missing viewport tag, llms.txt, AI crawler directives, and GBP link.
