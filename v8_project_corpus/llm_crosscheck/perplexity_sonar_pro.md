# perplexity_sonar_pro Cross-Check

Status: `ok`

# 1. Core Architecture Recommendation
**Next.js App Router + Supabase + Vercel AI SDK stack** grounded in external references [3][2][4].  
- **Frontend**: React 19 + Tailwind 4 + shadcn/ui (reuse from Move Intelligence [5]); dynamic brand theming via URL params for 19-brand multi-tenancy.  
- **Backend**: Supabase for Postgres (tenant-isolated schemas, RLS, realtime subscriptions); Vercel AI SDK for streaming routes and Zod-validated tools.  
- **Agent Layer**: HMLR memory [1] for stateful agent memory + RAG (Atlan [ref]); separate corpus retrieval (GEO audits, pricing CSVs) from tenant memory.  
- **Deployment**: Local-first Expo pattern [2] for offline quoting bots; multi-tenant guardrails [4] (OAuth, encryption, audit logs).  
Reuses: SQLite→Supabase migration for review flows ; IMAP→Supabase Edge Functions for lead quoting [3][6]; Zapier webhooks [5].  

# 2. Data and Memory Model
**Hybrid RAG + Stateful Memory (Atlan distinction)**:  
- **RAG Corpus**: Global extracts (GEO audits [1][2][7], pricing CSVs [3][6], logistics schemas [4]) in Supabase pgvector; Zod-validated ingestion with CSV importer .  
- **Stateful Memory**: HMLR [1] per-tenant (multi-hop/temporal reasoning); Supabase tables with `tenant_id`, `created/updated/deleted` (soft deletes [2]), realtime sync.  
- **Schema**:  
  ```sql
  tenants (id, name, brands[]);  -- 19 moving cos
  memories (tenant_id, type, content, metadata JSONB, vector);  -- HMLR
  workflows (tenant_id, state, config JSONB);  -- Review flows, quoting
  audits (tenant_id, domain, geo_score);  -- GEO [1][2]
  ```  
Reuses: Review SQLite→Supabase ; operator rates→JSONB [6]; difficulty scores→computed columns [4].  

# 3. Workflow/Automation Layer
**Agent swarms via Vercel AI SDK tools + cron/Edge Functions**:  
- **Swarm Patterns**:  
  | Swarm | Reused Assets | Triggers |
  |-------|---------------|----------|
  | Review Solicitation | Flask→Edge Fn , Twilio/Tremendous | Hourly cron, survey webhook |
  | Lead Quoting | IMAP monitor→subscriptions [3][6], multi-LLM | Email/realtime inbox |
  | GEO Auditor | Audit JSON→pg_cron [1][2][7] | Daily domain scans |
  | Logistics Intake | React form→Zapier [4] | Form submit |
- **Orchestration**: Supabase Edge Functions for daemon-like bots (24/7 quoting [3]); realtime state via subscriptions [2].  
- **Extensibility**: Zod tools for dynamic swarms (e.g., Golden Route detection [3]).  

# 4. Multi-LLM Routing Plan
**Fallback cascade (reuse [3][6])**: Gemini 2.0 Flash (primary, cost-efficient) → OpenAI GPT-4o-mini → Ollama (local fallback).  
- **Vercel AI SDK abstraction**: Provider routing by cost/latency/tenant prefs; FlashAttention/YOLOv12 efficiency [2] for edge deployment.  
- **Routing Logic**:  
  ```ts
  route({ tenantPrefs: { model: 'gemini' }, fallback: ['openai', 'ollama'] });
  ```  
- **Memory Integration**: HMLR state injected into all providers [1]; schema validation prevents hallucination.  

# 5. Compliance and Security Guardrails
**Multi-tenant SaaS controls [4] + corpus risks**:  
- **Isolation**: `tenant_id` RLS on all tables; brand placeholders `[Company Name]` [4].  
- **Compliance**: FTC/Google blocks in prompts (no fake reviews/gating [2][7]); audit logs for all actions.  
- **Security**: OAuth/OIDC login; Supabase encryption; no env creds (secrets manager); sanitize debug collectors [4].  
- **Risks Mitigated**:  
  | Risk | Control |
  |------|---------|
  | Review gating | Prompt guards + webhook validation  |
  | Astroturfing | No Reddit automation [2][7] |
  | CSV staleness | Realtime sync [2][3] |
  | Brand contamination | URL param theming [4] |

# 6. V8 Prompt Improvements
**Incorporate into master prompt**:  
```
MANDATORY GUARDRAILS:
- NO fake reviews/astroturfing (FTC $53k/violation [0][2])
- Tenant isolation: ALWAYS use tenant_id, [Company Name] placeholders
- Memory hygiene: Separate RAG corpus from HMLR state; validate sources before persisting (Atlan)
- Compliance: Block review gating; verify GBP links [1]

REUSABLE PATTERNS:
- Multi-LLM: Gemini→OpenAI→Ollama w/ Zod tools (Vercel AI SDK)
- Workflows: Supabase Edge + realtime (review [0], quoting [3])
- GEO: llms.txt, JSON-LD, FAQ density [1][2]

OUTPUT FORMAT: Schema-first (Zod), then code, then risks.
```
**Enhance agent reasoning**: "Use HMLR for multi-hop sales workflows; route via tenant prefs."

# 7. Fastest Safe Implementation Sequence
**4-week sprint (GEO 90-day phasing [1])**:  
1. **Week 1: Foundation (2 days)**  
   - Supabase setup (tenants, RLS, pgvector); migrate SQLite/review schema .  
   - Next.js boilerplate + Vercel AI SDK streaming chat.  
2. **Week 2: Core Ingestion (3 days)**  
   - Zod-validated CSV/JSON importers (pricing [3], audits [1][2]).  
   - HMLR memory layer [1]; multi-LLM routing.  
3. **Week 3: Workflows (4 days)**  
   - Review swarm (Twilio Edge Fn ).  
   - Quoting bot (realtime subscriptions [3][6]).  
   - Multi-tenant UI (React forms [4]).  
4. **Week 4: Polish/Deploy (2 days)**  
   - GEO auditor cron [1]; compliance tests.  
   - Vercel deploy; local-first mobile sync [2].  
**Risk**: API downtimes (Twilio ) → Fallback to manual queues. **Total: 11 dev days**.
