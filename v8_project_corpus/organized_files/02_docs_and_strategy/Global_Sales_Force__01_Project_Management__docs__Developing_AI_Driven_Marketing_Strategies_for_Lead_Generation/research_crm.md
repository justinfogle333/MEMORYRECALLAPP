# CRM Research Notes

## Ultimate Moving CRM
- URL: app.ultimatemoving.us
- Title on login page: "Long Distance Moving Software"
- Branded as "UM - Ultimate Moving"
- This appears to be a custom/proprietary CRM built specifically for the conglomerate, NOT a widely known off-the-shelf product
- No public API documentation found
- No public webhook documentation found

## Integration Strategy
Since this is a proprietary CRM with no public API docs, we have two approaches:
1. **Database-level integration:** If Justin has access to the database, we can set up a cron job to poll for completed moves.
2. **Manual/CSV export approach:** Export completed moves periodically and feed into the automation.
3. **Browser automation:** Use a script to scrape completed move data from the CRM dashboard.
4. **Ask the dev team:** The Serbian developer or the CRM vendor may be able to add a webhook.

## Most Cost-Effective Stack (Token/Cost Optimized)
- **No LLM needed for this agent** — it's a rules-based workflow, not an AI conversation
- **Python script + cron job** = cheapest option (zero monthly platform fees)
- **Twilio SMS** = ~$0.0079 per message (cheapest communication channel)
- **Tremendous API** = free to use, only pay for the gift cards themselves
- **SQLite** = free local database for tracking
- Total recurring cost: Twilio SMS only (~$0.016 per customer for 2 messages)
