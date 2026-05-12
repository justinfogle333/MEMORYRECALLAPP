# LIFE-RECALLAPP / MEMORYRECALLAPP V8 Master Plan

**Author:** Manus AI  
**Version:** V8  
**Repository:** `justinfogle333/MEMORYRECALLAPP`  
**Prepared:** 2026-05-09 UTC

## Executive Direction

The V8 direction is to evolve **MEMORYRECALLAPP** into a recall-oriented, automation-capable, multi-tenant operating system for Global Sales Force. The extracted corpus shows that the project is not merely a personal memory app; it is a convergence point for **lead quoting**, **move-intelligence intake**, **review workflow automation**, **GEO/AI search readiness**, **multi-brand operations**, and **LLM-routed agent work**. The highest-leverage framework is therefore a modular app that separates **source-of-truth project knowledge**, **stateful memory**, **retrieval-augmented search**, and **workflow execution**.

The key architectural decision is to treat **RAG and memory as separate layers**. Current AI architecture research distinguishes RAG as a stateless retrieval pipeline and AI memory as a stateful write/read layer that persists across sessions.[1] This distinction is central to V8 because the app must recall project documents, but it must also remember decisions, tenant preferences, brand constraints, workflow history, and recurring operational state without poisoning the knowledge base.

## Top-Down Corpus Findings

Eight ZIP archives were found in the accessible project/Drive surface and opened. The extraction pass processed **471 archive members**, retained **265 unique files**, removed **206 duplicates**, excluded **8 sensitive/private candidates**, and removed remaining nested ZIP files after confirming their contents were already expanded through matching top-level archives. The recall tree is now placed under `v8_project_corpus/`, with extracted source files, knowledge packs, manifests, LLM cross-check outputs, and research notes arranged for direct retrieval without re-opening compressed archives.

| Evidence Source | V8 Interpretation | Action Taken |
|---|---|---|
| Automated Review Solicitation Agent | Provides reusable workflow-state patterns: customer table, SMS log, gift-card log, webhook intake, scheduled worker, and compliance-sensitive review flow. | Preserve architecture as a workflow module pattern, but require strict FTC guardrails and tenant-aware audit logs. |
| GEO readiness audits and strategy exports | Provides a repeatable audit model for AI search discoverability: schema, crawler access, `llms.txt`, FAQ density, and entity authority. | Incorporate a GEO auditor service into V8, not as the core product but as an automation module. |
| Bot A Lead Quoting Engine v2/v3 | Provides LLM email parsing, pricing heuristics, route scoring, operator overrides, and multi-model fallback logic. | Convert from local daemon/CSV into database-backed workflow execution with human-review thresholds. |
| Move Intelligence Full Suite | Provides the strongest frontend pattern: React, Tailwind, shadcn/ui, multi-step intake, dynamic scoring, and brand-neutral placeholders. | Make this the reference UI pattern for V8 interactive workflows. |
| Multi-LLM and external research cross-check | Confirms hybrid RAG + stateful memory, model routing, and tenant isolation as the strongest framework. | Use model roles instead of a single default model; persist routing policy in documentation and app config. |

## Recommended V8 Framework

The primary V8 implementation should be a **multi-tenant web application with server-side agent APIs**, not a purely local script collection. The fastest path that preserves project momentum is a TypeScript-first web stack with a Python-compatible worker lane for legacy automation modules.

| Layer | Recommended Choice | Reason |
|---|---|---|
| User application | **React + TypeScript + Tailwind + shadcn/ui** | Matches the extracted Move Intelligence UI pattern and supports polished, reusable workflow screens. |
| Server/API | **Next.js App Router or Vite/React with a typed API backend** | The AI SDK reference shows how streaming AI routes, provider abstraction, schema-validated tools, and React chat hooks fit well in a TypeScript app.[2] |
| Data store | **Postgres-compatible relational database with row-level tenant isolation** | Supports tenants, users, brands, workflow state, audit logs, corpus manifests, and future vector search. |
| Memory and retrieval | **Hybrid memory + RAG** | RAG indexes extracted project knowledge, while memory persists decisions and user/project state across sessions.[1] |
| Offline/mobile option | **Expo local-first module after web MVP** | Supabase/Legend-State patterns show local persistence, retryable sync, generated IDs, timestamps, and soft deletes for offline-capable apps.[3] |
| Workflow execution | **Event-driven worker layer** | Converts cron scripts, local daemons, webhooks, review flows, and quoting workflows into observable jobs. |
| LLM gateway | **Provider router with fallback policy** | Extracted Bot A already validated a Gemini-first, OpenAI/other-provider fallback concept; V8 should formalize this as a routing service. |

The app must remain **modular**. Review automation, quoting, GEO audits, logistics intake, and project memory should be separate modules that share identity, tenant, audit, memory, and workflow primitives. This prevents the prompt and product from becoming a brittle monolith.

## Data and Memory Model

V8 should implement three distinct stores. The **source corpus store** contains extracted project files and metadata. The **RAG index** contains chunked embeddings for retrieval from documents, code, CSVs, transcripts, and strategy files. The **stateful memory store** persists decisions, user preferences, tenant rules, workflow outcomes, and known facts, and it must include provenance and confidence fields.

| Table or Collection | Purpose | Key Fields |
|---|---|---|
| `tenants` | Multi-brand/company isolation | `id`, `name`, `status`, `settings_json`, `created_at` |
| `brands` | 19-brand support without code duplication | `tenant_id`, `brand_name`, `domain`, `gbp_url`, `theme_json` |
| `corpus_files` | Manifest of extracted and future project files | `sha256`, `path`, `source_archive`, `category`, `sensitivity_status` |
| `corpus_chunks` | RAG retrieval layer | `file_sha256`, `chunk_text`, `embedding`, `metadata_json` |
| `memories` | Stateful recall layer | `tenant_id`, `subject`, `memory_type`, `fact`, `source_refs`, `confidence`, `expires_at` |
| `workflows` | Automation lifecycle state | `tenant_id`, `workflow_type`, `status`, `state_json`, `next_run_at` |
| `workflow_events` | Audit and replay log | `workflow_id`, `event_type`, `input_hash`, `output_hash`, `model_used`, `created_at` |
| `llm_routes` | Model routing policy | `task_type`, `primary_model`, `fallback_models`, `max_cost`, `privacy_level` |

This structure supports fast recall without repeatedly opening ZIP archives. It also reduces token waste because future agents can first read the **V8 corpus index**, then only pull exact file packs or chunks needed for a task.

## Module Roadmap

The first production milestone should be a **V8 foundation app** that can ingest files, search project knowledge, remember decisions, and execute auditable workflows. Only after that should the app activate high-risk automation such as outbound review SMS or autonomous quoting.

| Priority | Module | Scope | Reason |
|---:|---|---|---|
| 1 | Project Knowledge Hub | Corpus import, manifest view, semantic search, source citations, memory write controls. | This is the core recall function and the basis for every later module. |
| 2 | LLM Gateway | Task classifier, model router, fallback policy, structured output validation, cost/latency logging. | Prevents provider lock-in and implements the extracted multi-LLM pattern. |
| 3 | Workflow Engine | Jobs, webhooks, scheduled tasks, human-review queue, audit logs. | Converts extracted cron/daemon scripts into a managed platform. |
| 4 | Move Intelligence Intake | Multi-step form, brand theming, difficulty scoring, document export, Zapier/CRM hook. | The most complete UI asset in the corpus and safest user-facing MVP workflow. |
| 5 | Lead Quoting Agent | Email/API ingestion, structured parsing, pricing rules, operator overrides, confidence gate. | High business value but requires validation and human oversight before automation. |
| 6 | GEO Auditor | Domain audit, schema checks, `llms.txt`, crawler directives, FAQ/entity completeness. | Supports AI search dominance using corpus-derived audit assets. |
| 7 | Review Workflow Agent | Consent-aware review requests, opt-out tracking, non-gated feedback, compliance logs. | Valuable but compliance-sensitive; must be gated behind policy controls. |

## LLM/API Task-Routing Framework

The best model is task-dependent. V8 should not hardcode one model. Instead, route by **privacy**, **complexity**, **latency**, **cost**, and **need for web-grounded evidence**.

| Task Type | Primary Choice | Fallback | Why |
|---|---|---|---|
| Large corpus synthesis and planning | Gemini / long-context model | Perplexity or DeepSeek | Strong long-context synthesis; useful for broad project plan generation. |
| Web-grounded research and citation validation | Perplexity Sonar | Browser/web extraction plus Gemini | Best fit for current-source validation and citation discovery. |
| Code generation and deterministic implementation | OpenAI-compatible coding model when quota permits | DeepSeek / local code model | Strong for structured code and refactors; fallback needed due quota/availability. |
| Safety, policy, prompt hardening | Claude-class model when allowed | Gemini + deterministic policy checklist | Best conceptual fit for safety; unavailable in this run due access restrictions. |
| High-volume parsing/classification | Gemini Flash / DeepSeek | Local Ollama where available | Cost-efficient for repeated lead parsing, category tagging, and JSON extraction. |
| Sensitive/private tenant data | Local model or redacted cloud prompt | Human review | Prevents unnecessary exposure of credentials, customer data, and internal notes. |
| Real-time user chat | AI SDK provider router | Secondary model with circuit breaker | Supports streaming, schema tools, and model abstraction.[2] |

In this run, Perplexity, Gemini, and DeepSeek returned usable cross-checks. Anthropic returned a permission error, Kimi returned invalid authentication, and OpenAI returned quota exhaustion. The routing layer must record provider health and fail closed rather than silently degrading output quality.

## Compliance and Security Guardrails

V8 must enforce security and compliance at the platform layer, not only in prompts. Multi-tenant SaaS guidance emphasizes tenant identifiers, data isolation, role-based access control, encryption, audit monitoring, and automated onboarding as foundational controls.[4] The FTC’s review rule prohibits fake or false reviews, buying sentiment-conditioned reviews, undisclosed insider reviews, misleading company-controlled review sites, review suppression, and fake social indicators.[5]

| Risk | Required V8 Control |
|---|---|
| Credential leakage | Never commit `.env`, connector configs, API keys, passwords, browser state, or raw secret-bearing files. Use secrets manager abstractions. |
| Brand contamination | Every record and prompt must carry `tenant_id` and `brand_id`; use `[Company Name]` placeholders in reusable templates. |
| Fake review or review gating | The app may request honest feedback but must not generate fake reviews, condition incentives on positive sentiment, or suppress negative feedback. |
| Hallucinated quotes/prices | Pricing outputs must be schema-validated, tied to source data, confidence-scored, and routed to human review when thresholds fail. |
| Memory poisoning | Memories need source references, confidence, expiration, and review status before becoming durable facts. |
| Cross-tenant data exposure | Enforce row-level policies, server-side authorization checks, and tenant-scoped retrieval filters. |
| Prompt drift | Store canonical prompts as versioned artifacts and validate generated JSON against schemas before execution. |

## Fastest Safe Implementation Sequence

The fastest safe route is an **8-week V8 foundation sprint**. A shorter sprint would risk mixing memory, retrieval, workflow execution, and compliance into a fragile prototype. V8 should prioritize durable primitives first, then activate automation modules.

| Sprint | Outcome | Deliverables |
|---|---|---|
| Week 1 | Repository and corpus foundation | Keep extracted V8 corpus, manifests, knowledge packs, and V8 docs synced; add file import pipeline and sensitivity scanner. |
| Week 2 | Tenant and identity foundation | Tenants, brands, users, RBAC, audit log, and row-level isolation model. |
| Week 3 | Memory/RAG foundation | Corpus chunking, retrieval, source citations, memory write approvals, and recall dashboard. |
| Week 4 | LLM gateway | Provider routing, fallback, model health logging, schema validation, and task-specific prompt versions. |
| Week 5 | Workflow engine | Job table, event log, webhooks, scheduler, retry/circuit breaker, and human-review queue. |
| Week 6 | Move Intelligence MVP | Multi-step intake UI, difficulty scoring, brand theming, document export, and CRM/Zapier hook. |
| Week 7 | Quoting and GEO modules | Import pricing/rates, implement confidence-gated quote draft flow, and add GEO audit checks. |
| Week 8 | Review workflow and hardening | Consent/opt-out review request workflow, compliance tests, security scan, and deployment readiness report. |

## V8 Definition of Done

V8 is done when the repository contains a clean extraction tree, no remaining ZIP dependency for recall, a versioned V8 prompt, a master plan, an LLM routing framework, and enough organized corpus material for future agents to work without re-downloading or re-opening archives. It is also done only if sensitive material remains excluded and the repository verifies cleanly after push.

## References

[1]: https://atlan.com/know/ai-memory-system-vs-rag/ "AI Memory System vs RAG: The Enterprise Architecture Decision"  
[2]: https://ai-sdk.dev/docs/getting-started/nextjs-app-router "Next.js App Router Quickstart"  
[3]: https://supabase.com/blog/local-first-expo-legend-state "Local-first Realtime Apps with Expo and Legend-State"  
[4]: https://ramamtech.com/blog/scalable-secure-multi-tenant-apps "How to Build Multi-Tenant Web Apps That Scale Safely and Securely"  
[5]: https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials "Federal Trade Commission Announces Final Rule Banning Fake Reviews and Testimonials"
