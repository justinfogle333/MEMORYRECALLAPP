# deepseek_chat Cross-Check

Status: `ok`

# V8 Architecture Guidance: Life-RecallApp / MemoryRecallApp

## Core Stack

**Primary:** Python 3.11+ with FastAPI (async), SQLite/PostgreSQL, React 19 + Tailwind CSS 4 + shadcn/ui for interactive components.

**Supporting:** Flask for lightweight webhooks, Celery/APScheduler for cron-based workflows, Twilio API for SMS, Tremendous API for incentives.

**Rationale:** The corpus demonstrates successful patterns with Python-based automation (Bot A, Review Solicitation Agent) and modern React for user-facing interfaces (Move Intelligence System). FastAPI provides async capabilities needed for concurrent LLM calls and webhook handling.

---

## Memory/RAG Model

**Architecture:** Hybrid approach combining structured SQLite/PostgreSQL for transactional data with vector embeddings (pgvector or ChromaDB) for semantic retrieval.

**Implementation:**
- **Short-term memory:** In-memory conversation buffers (last 20 exchanges) with sliding window
- **Long-term memory:** SQLite tables for customer profiles, interaction history, and preference vectors
- **RAG pipeline:** Embedding generation via `text-embedding-3-small` → vector DB → similarity search → context injection into prompts
- **Entity extraction:** Named entity recognition on incoming messages to populate structured fields (customer name, move date, origin/destination)

**Key insight from corpus:** The Review Solicitation Agent's SQLite schema (customers, sms_log, gift_card_log) provides a proven pattern for tracking stateful interactions. Extend this with vector columns for semantic search.

---

## Workflow Automation

**Pattern:** Event-driven architecture with three tiers:

1. **Triggers:** Webhooks (Twilio, survey completions), IMAP email monitoring, scheduled cron jobs
2. **Processors:** Celery workers for async tasks (quote calculation, SMS sending, document generation)
3. **Actions:** API calls (Twilio, Tremendous, SendGrid), database updates, LLM invocations

**Critical workflows from corpus:**
- **Lead ingestion:** IMAP monitoring → email parsing (LLM-assisted) → CRM entry → quote generation
- **Review solicitation:** Survey completion webhook → SMS trigger → gift card delivery → follow-up reminders
- **GEO optimization:** Automated weekly audits → schema markup validation → llms.txt generation → Google Business Profile link verification

**Implementation:** Use Apache Airflow or Prefect for complex DAGs, Celery for simple task queues. The Bot A daemon pattern (24/7 local process) should be containerized with Docker and deployed via Kubernetes for scalability.

---

## LLM Routing

**Multi-tier fallback architecture (proven in Bot A v2/v3):**

| Tier | Model | Use Case | Cost Tier |
|------|-------|----------|-----------|
| 1 | Gemini 2.0 Flash | Primary, high-volume tasks | Low |
| 2 | GPT-4o-mini | Complex reasoning, fallback | Medium |
| 3 | Ollama (local) | Offline mode, sensitive data | Free |
| 4 | GPT-4o | Edge cases, human review | High |

**Routing logic:**
- **Simple queries** (parsing, classification): Tier 1
- **Complex reasoning** (quote negotiation, complaint handling): Tier 2
- **Offline/private data**: Tier 3
- **Escalation** (human review flagged): Tier 4

**Implementation:** Abstract router class with configurable thresholds (confidence scores, latency limits, cost caps). Include circuit breaker pattern to prevent cascading failures.

---

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| FTC/GDPR violations (fake reviews, data privacy) | Critical | Strict compliance guardrails in prompts; audit logging; human-in-loop for review generation |
| LLM hallucination in quotes/pricing | High | Validate all LLM outputs against historical data; require human approval for >$500 quotes |
| Single point of failure (local daemon) | High | Containerize all services; implement health checks; auto-restart policies |
| Data leakage across brands | Medium | Tenant isolation via database schemas; generic `[Company Name]` placeholders (Move Intelligence pattern) |
| API key exposure | Medium | Secrets manager (HashiCorp Vault/AWS Secrets Manager); never in environment variables |
| IMAP/SMTP reliability | Medium | Migrate to API-based email (SendGrid, Mailgun) with retry logic |

---

## V8 Prompt Improvements

Based on corpus analysis, implement these prompt engineering patterns:

### 1. Structured Output Templates
```python
# Instead of free-form responses, enforce JSON schema
SYSTEM_PROMPT = """
You are an automated review solicitation agent. 
Respond ONLY with valid JSON matching this schema:
{
  "action": "send_sms" | "send_gift_card" | "escalate" | "wait",
  "message_template": "string",
  "reasoning": "string",
  "compliance_check": "FTC_RULE_2024_123" | "GOOGLE_POLICY_456"
}
"""
```

### 2. Compliance Guardrails (from Review Agent findings)
```
COMPLIANCE_RULES:
- Never generate fake reviews or incentivize positive reviews
- Always disclose material connections (gift cards)
- Never engage in review gating (selective solicitation)
- Include opt-out mechanism in every SMS
- Store consent records for 3 years minimum
```

### 3. Context Injection Pattern
```
CONTEXT:
- Customer history: {last_3_interactions}
- Current stage: {workflow_step}
- Brand guidelines: {brand_specific_rules}
- Regulatory jurisdiction: {customer_location}

TASK: {current_action}
```

### 4. Multi-LLM Fallback Prompt
```
# Primary prompt (Gemini optimized)
You are a concise, direct assistant. Use minimal tokens.

# Fallback prompt (GPT-4o-mini)
You are a detailed, thorough assistant. Provide reasoning.

# Escalation prompt (GPT-4o)
You are handling a complex edge case. Consider all alternatives.
```

### 5. Error Recovery Pattern
```
ERROR_DETECTION:
- If output fails JSON validation: retry with stricter constraints
- If confidence < 0.7: escalate to human review
- If API timeout: switch to local Ollama fallback
- If repeated failures: pause workflow and notify admin
```

### 6. GEO Optimization Prompt (from audit findings)
```
GEO_REQUIREMENTS:
- Generate FAQ sections with minimum 5 Q&A pairs
- Include schema markup in JSON-LD format
- Ensure llms.txt references all key pages
- Verify robots.txt allows GPTBot and ClaudeBot
- Link to Google Business Profile on every local page
```

---

## Implementation Priority

1. **Week 1-2:** Core stack setup (FastAPI + React + SQLite), implement multi-LLM router
2. **Week 3-4:** Workflow automation (Celery + webhooks), migrate from IMAP to API-based email
3. **Week 5-6:** RAG pipeline with vector embeddings, implement compliance guardrails
4. **Week 7-8:** GEO automation module, brand isolation pattern, secrets management
5. **Week 9-10:** Testing, monitoring, documentation, deployment to staging

**Total estimated effort:** 10 weeks for MVP, 16 weeks for production-ready system with all features from corpus.
