# Developer Handoff Specification: Automated Review Solicitation Agent

**Project:** Global Sales Force AI Lead Generation
**Component:** Automated Review Solicitation Agent
**Target:** 19 Brands, 100+ Google Business Profile (GBP) Locations
**Objective:** Automate the generation of authentic, FTC-compliant Google reviews using a "Two-Step Decoupled" incentive model.

---

## 1. System Architecture & Tech Stack

The system requires four primary components to function autonomously:

| Component | Tool / Platform | Purpose |
| :--- | :--- | :--- |
| **Trigger Source** | Existing CRM / Dispatch System | Triggers the workflow when a move is marked as "Completed." |
| **Orchestration** | Zapier or Make.com | The central brain that routes data, applies logic, and triggers actions. |
| **Communication** | Twilio (SMS) & SendGrid (Email) | Delivers the survey links and follow-up review requests to the customer. |
| **Incentive API** | Tremendous or Tango Card | Automatically issues the $15 Amazon Gift Card upon survey completion. |

---

## 2. The "Two-Step Decoupled" Logic Flow

To remain strictly compliant with Google's prohibition on incentivized reviews and the FTC's prohibition on review gating, the logic flow must decouple the financial incentive from the public review request.

### Step 1: The Incentive (Day 0)
**Trigger:** Move status changes to "Completed" in the CRM.
**Action:** The orchestration tool waits 2 hours, then sends an SMS/Email via Twilio/SendGrid.
**Offer:** The customer is offered a $15 Amazon Gift Card in exchange for completing an internal, private 3-question Quality Assurance survey.
**Compliance Check:** This is entirely legal. We are paying for private feedback, not a public review.

### Step 2: The Fulfillment (Day 0 - Immediate)
**Trigger:** Customer submits the survey via a web form (e.g., Typeform or native WordPress form).
**Action:** The orchestration tool receives the webhook from the form, calls the Tremendous/Tango API, and instantly emails the $15 Amazon Gift Card to the customer.

### Step 3: The Ask (Day 1)
**Trigger:** 24 hours after the survey is submitted.
**Action:** The orchestration tool sends a second SMS/Email.
**Offer:** The customer is asked to share their experience on Google. **Crucially, no incentive is mentioned or offered in this step.**
**Compliance Check:** Because the incentive was already paid for the survey, and this request is sent to *all* survey respondents regardless of their sentiment, this complies with both Google and FTC policies.

---

## 3. Copywriting Templates

The following templates must be used exactly as written to maintain compliance and maximize conversion rates.

### Template 1: The Survey Request (SMS)
> "Hi [Customer Name], thank you for moving with [Brand Name]! We want to ensure everything went perfectly. Please take our 60-second Quality Assurance survey and we'll instantly send you a $15 Amazon Gift Card for your time. Tap here: [Survey Link]"

### Template 2: The Gift Card Delivery (Email)
> **Subject:** Your $15 Amazon Gift Card from [Brand Name]
> 
> "Hi [Customer Name], 
> 
> Thank you for completing our Quality Assurance survey. Your feedback helps us improve our service for future families. 
> 
> As promised, here is your $15 Amazon Gift Card: [Gift Card Link/Code]
> 
> Thank you again for choosing [Brand Name]!"

### Template 3: The Google Review Ask (SMS - 24 Hours Later)
> "Hi [Customer Name], it's [Brand Name] again. We're so glad we could help with your move. If you have a spare minute, it would mean the world to our crew if you shared your experience on Google. You can leave a review here: [Direct GBP Link]"

---

## 4. Asana Task Breakdown for Development Team

This section is formatted for direct import into the Canada-based supervisor's Asana workflow.

### Phase 1: Infrastructure Setup
- **Task 1.1:** Create Twilio sub-accounts for all 19 brands to ensure local area codes match the brand's primary operating region.
- **Task 1.2:** Set up a Tremendous or Tango Card API account and fund the initial escrow balance.
- **Task 1.3:** Map all 100+ Google Business Profile direct review links to their corresponding internal location IDs in a master database.

### Phase 2: Form & Landing Page Creation
- **Task 2.1:** Build a standardized, mobile-optimized 3-question survey form.
- **Task 2.2:** Deploy the survey form to a hidden URL on all 19 brand WordPress sites (e.g., `brand.com/quality-assurance`).
- **Task 2.3:** Configure form webhooks to send submission data (Name, Email, Phone, Location ID) to the orchestration tool.

### Phase 3: Orchestration Logic (Zapier/Make)
- **Task 3.1:** Build Zap 1: Catch "Move Completed" webhook from CRM -> Delay 2 hours -> Send SMS Template 1 via Twilio.
- **Task 3.2:** Build Zap 2: Catch "Survey Submitted" webhook -> Call Tremendous API -> Send Email Template 2.
- **Task 3.3:** Build Zap 3: Catch "Survey Submitted" webhook -> Delay 24 hours -> Lookup GBP Link by Location ID -> Send SMS Template 3 via Twilio.

### Phase 4: Testing & QA
- **Task 4.1:** Run end-to-end dummy data through all 19 brand pipelines to verify correct brand naming, correct Twilio numbers, and correct GBP link routing.
- **Task 4.2:** Verify that the 24-hour delay in Zap 3 functions correctly and does not mention the gift card.
