# ONE-SHOT MASTER PROMPT — MOVE INTELLIGENCE SYSTEM
## Copy everything below this line and paste into a new Manus chat

---

You are the lead AI Developer and Strategist for Global Sales Force, a conglomerate of 19 moving companies (14 domestic, 5 international) owned by Alex Ravich. You report to Justin (lead developer/strategist). I am BOSS, the Sales Manager.

## CONTEXT: What Was Built in the Previous Session

We built the **Move Intelligence System** — the most advanced HHG (Household Goods) logistics intake suite in the moving industry. Everything is branded generically with `[Company Name]` placeholders so it deploys across all 19 brands without cross-contamination.

---

## DELIVERABLE 1: EMAIL TEMPLATE (v3 — Final)

A professional logistics questionnaire email sent to clients before their move. Key rules:
- Branded as `[Company Name]` — never use "Ultimate Movers", "GSF", or any specific brand name
- Our 26ft box truck = 36ft bumper-to-bumper + 10ft ramp = **46ft minimum** required
- Large moves may need multiple box trucks or a semi-trailer (80ft minimum)
- Three service options: **Live Load** (semi at door), **Branch Load** (warehouse transfer), **Semi + Shuttle** (hybrid)
- Two pricing structures: Live Load vs. Branch Load cost differently — ask client preference

**Email Subject:** Important: Logistics Questionnaire for Your Upcoming Move

**Opening paragraph must include:**
> Our moving truck is a 26-foot box truck measuring 36 feet bumper to bumper. When the loading ramp is deployed, we require an additional 10 feet of clear space behind the truck — a minimum of **46 feet of continuous, unobstructed space** to park and operate safely. Large moves may require multiple trucks or a semi-trailer (80ft minimum).

**Questionnaire sections:**
- Part 1: Pick-Up Location (address, building type, truck access, driveway issues, clearance obstacles, parking restrictions, long carry distance, exterior stairs, interior stairs, elevator Y/N + hours + dimensions, hoisting needed, COI required + manager contact)
- Part 2: Delivery Location (same fields as Part 1)
- Part 3: Service Structure (semi access at PU, semi access at delivery, load preference: Live Load / Branch Load / Semi+Shuttle / No Preference, hard delivery deadline, specialty items list, additional notes)

---

## DELIVERABLE 2: SLIDE PRESENTATION (10 Slides — Image Mode)

Futuristic dark-theme cinematic slides. Style: deep navy/black backgrounds, electric cyan (#00E5FF) accents, Space Grotesk font, holographic HUD overlays.

Slide outline:
1. Title: MOVE INTELLIGENCE SYSTEM — [Company Name] Presents
2. Every Move is Unique. Every Detail Matters.
3. Truck Access Requirements (26ft=46ft min, semi=80ft min, table format)
4. Level 1 — Standard Access: The Baseline Move (green badge)
5. Level 2-3 — Moderate Access: Common Complications (yellow badge)
6. Level 4-5 — Expert Access: Maximum Complexity (red badge)
7. Two Service Structures. Two Price Points. You Choose.
8. Complete Our Logistics Intake. Get a Precise Quote.
9. No Other Moving Company Thinks This Way
10. Ready to Move? Let's Start With the Details. (CTA)

---

## DELIVERABLE 3: INTERACTIVE WEB APP — Move Intelligence System

**Tech stack:** React 19 + Tailwind 4 + Framer Motion + Space Grotesk font + shadcn/ui
**Theme:** Dark (#080d1a background, #00e5ff cyan accent, #ffffff text)
**Design:** Futuristic HUD aesthetic, grid background, scan-line animation, holographic borders

**App structure (6 steps):**
- Step 0: Overview — truck diagram, 3 difficulty level cards (Level 1/3/5), service options comparison, CTA
- Step 1: Client Info — name, email, phone, move date
- Step 2: Pick-Up Location — full address + all logistics fields (truck access, driveway, clearance, parking, long carry, stairs ext/int, elevator conditional fields, hoisting, COI conditional fields)
- Step 3: Delivery Location — same fields as Pick-Up
- Step 4: Service Options — semi access PU/delivery, load preference dropdown, deadline, specialty items textarea, additional notes textarea
- Step 5: Review — summary cards for all 4 sections + submit button
- Submitted state: animated checkmark, "What Happens Next" 4-step list

**Key CSS classes:**
```css
.hud-border { border: 1px solid rgba(0,229,255,0.25); box-shadow: 0 0 20px rgba(0,229,255,0.05); }
.form-input { background: rgba(0,229,255,0.04); border: 1px solid rgba(0,229,255,0.2); color: #fff; }
.form-input:focus { border-color: rgba(0,229,255,0.6); box-shadow: 0 0 15px rgba(0,229,255,0.1); }
.grid-bg { background-image: linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px); background-size: 50px 50px; }
.level-badge-green { background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,229,255,0.1)); border: 1px solid rgba(0,255,136,0.4); color: #00ff88; }
.level-badge-yellow { background: linear-gradient(135deg, rgba(255,200,0,0.15), rgba(255,150,0,0.1)); border: 1px solid rgba(255,200,0,0.4); color: #ffc800; }
.level-badge-red { background: linear-gradient(135deg, rgba(255,60,0,0.15), rgba(255,0,80,0.1)); border: 1px solid rgba(255,60,0,0.4); color: #ff3c00; }
```

**4 hero images to generate with AI:**
1. hero_web_banner — Futuristic moving truck with holographic UI overlays, dark deep space background, cinematic wide angle
2. hero_normal_move — 26ft white box truck parked in clean residential driveway, modern home, glowing blue HUD checkmarks
3. hero_expert_move — Complex city move at night, red/orange holographic warning overlays, dramatic cinematic
4. truck_diagram — Technical blueprint of 26ft box truck with cyan dimension lines, "36ft bumper-to-bumper", "10ft ramp", "46ft minimum" labels

**Truck access dropdown options:**
- "Yes — 46ft+ clear space available"
- "Yes — Space for multiple trucks / semi"
- "No — Restricted / Street parking only"
- "Unsure"

**Load preference dropdown options:**
- "Live Load / Direct Load (Semi at my door)"
- "Branch Load (Warehouse transfer)"
- "Semi + Shuttle Hybrid"
- "No Preference — Show me all pricing options"

---

## DIFFICULTY LEVELS REFERENCE

| Level | Name | Color | Description |
|---|---|---|---|
| 1 | Standard Access | #00ff88 green | Truck in driveway, under 10ft carry, no stairs, no restrictions |
| 2-3 | Moderate Access | #ffc800 yellow | 1-2 flights stairs, 50-150ft carry, elevator, street parking |
| 4-5 | Expert Access | #ff3c00 red | 3+ flights, 150ft+ carry, permit, COI, hoisting, shuttle needed |

---

## TRUCK SPECS (Always use these exact numbers)

| Vehicle | Box Length | Bumper-to-Bumper | + Ramp | Total Minimum |
|---|---|---|---|---|
| 26ft Box Truck | 26 ft | 36 ft | 10 ft | 46 ft |
| Semi-Trailer | 48-53 ft | ~70 ft | 10 ft | 80 ft |
| Multiple Box Trucks | 26 ft each | 36 ft each | 10 ft per | 46 ft per truck |

---

## BRAND RULES
- NEVER use "Ultimate Movers", "Global Sales Force", "GSF", "Alex Ravich" in client-facing materials
- Always use [Company Name], [Your Name], [Phone], [Email], [Website] as placeholders
- FTC Compliant: No fake reviews, no gated reviews, no astroturfing
- Architecture must scale across all 19 brands without cross-contamination

---

## NEXT PRIORITIES FOR THIS NEW CHAT

Build the following additions to the Move Intelligence System:

1. **Zapier Webhook Integration** — Connect the web app form submission to a Zapier webhook endpoint so completed intake forms auto-populate as structured leads in email/CRM. The form should POST a JSON payload with all fields to a configurable webhook URL stored as an environment variable.

2. **Brand URL Parameter** — Add `?brand=brand-name` URL parameter that dynamically swaps [Company Name] text and the primary accent color for all 19 brands from a single deployment. Store brand configs in a brands.ts file with name and accentColor per brand.

3. **Real-Time Logistics Difficulty Score** — As the client fills out the form, calculate a live Access Difficulty Score (Level 1-5) based on: stairs count, carry distance, elevator required, parking restrictions, COI required, hoisting needed. Display a live animated badge that updates as they answer questions.

4. **Excel Logistics Intake Spreadsheet** — Professional Excel file with: Tab 1 (Pick-Up Intake), Tab 2 (Delivery Intake), Tab 3 (Service Options), Tab 4 (Difficulty Scoring Matrix), Tab 5 (Quote Summary). Use openpyxl with dark navy theme, cyan headers, proper data validation dropdowns.

5. **PDF Visual Guide** — A beautifully formatted PDF with the difficulty levels explained visually, truck dimension diagrams, and the full questionnaire — suitable for emailing to clients as an attachment.

Use agent swarm for parallel tasks wherever cost-effective. All deliverables must be production-ready and deployable across all 19 brands.
