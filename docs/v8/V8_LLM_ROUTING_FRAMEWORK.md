# V8 LLM/API Routing Framework

**Author:** Manus AI  
**Version:** V8  
**Scope:** LIFE-RECALLAPP / MEMORYRECALLAPP

## Routing Principle

V8 must route work by **task shape**, not by personal preference for one model. The extracted Bot A systems already used a practical fallback concept, and the V8 cross-check confirmed that no single provider should be assumed available. During this sync, Perplexity, Gemini, and DeepSeek returned usable analysis, while Anthropic was blocked by permission, Kimi failed authentication, and OpenAI was unavailable due quota. The app must therefore treat provider availability as a runtime health signal.

## Provider Role Matrix

| Workload | Best Primary Provider | Fallback | Required Controls |
|---|---|---|---|
| Current web research and citation validation | Perplexity Sonar | Browser extraction, Gemini synthesis | Store URLs, cite sources, avoid snippet-only decisions. |
| Broad corpus synthesis and long planning | Gemini long-context model | Perplexity, DeepSeek | Include corpus manifests and source excerpts, not raw secrets. |
| Code generation and refactoring | OpenAI-compatible coding model when quota permits | DeepSeek, local coding model | Run tests, lint, schema validation, and human review for destructive changes. |
| Safety, compliance, and prompt hardening | Claude-class model when access permits | Gemini plus deterministic checklist | Validate against FTC, tenant isolation, and outbound-action policies. |
| High-volume extraction/classification | Gemini Flash or DeepSeek | Local model | Enforce JSON schema; retry once on invalid output. |
| Sensitive tenant/customer data | Local model or redacted prompt | Human review | Do not send secrets or unnecessary personal data to cloud providers. |
| Outbound action decisioning | No fully autonomous model | Human-approved workflow | Draft first; execute only after authorization and audit logging. |

## Runtime Router Specification

Every model call should be recorded as a `workflow_event` or `llm_call` with the following fields.

| Field | Purpose |
|---|---|
| `tenant_id` | Prevents cross-tenant leakage and scopes retrieval. |
| `task_type` | Determines routing policy, schema, and model candidates. |
| `privacy_level` | Determines whether cloud models are allowed. |
| `primary_model` | First attempted model/provider. |
| `fallback_models` | Ordered failover list. |
| `input_hash` | Audit trail without storing unnecessary raw prompt content. |
| `output_hash` | Output integrity and replay support. |
| `schema_name` | Structured-output contract. |
| `validation_status` | Pass, fail, retry, or escalated. |
| `latency_ms` | Performance monitoring. |
| `estimated_cost` | Cost awareness and optimization. |
| `provider_status` | Success, quota, permission, auth failure, timeout, or validation failure. |

## Routing Pseudocode

```text
function routeTask(task):
  assert task.tenant_id exists
  assert task.task_type exists
  policy = loadRoutePolicy(task.task_type, task.privacy_level)
  context = buildTenantScopedContext(task)
  for provider in policy.providers:
    if provider.health is not healthy:
      continue
    if task.privacy_level forbids provider:
      continue
    result = callProvider(provider, context, policy.schema)
    logModelCall(result)
    if result.transport_failed:
      markProviderHealth(provider, result.error_type)
      continue
    if policy.schema and not validate(result.output, policy.schema):
      retry_result = callProvider(provider, strengthenSchemaPrompt(context), policy.schema)
      logModelCall(retry_result)
      if validate(retry_result.output, policy.schema):
        return retry_result
      continue
    return result
  return escalateToHumanReview(task)
```

## Provider Health Observed During V8 Sync

| Provider | Result | V8 Meaning |
|---|---|---|
| Perplexity Sonar Pro | Usable | Keep as research/citation primary. |
| Gemini 2.5 Flash | Partially usable | Useful for synthesis, but verify output completeness. |
| DeepSeek Chat | Usable | Good fallback for architecture and coding-oriented guidance. |
| Anthropic Claude | Permission blocked | Keep as optional safety/prompt-hardening route only when credentials allow. |
| OpenAI | Quota blocked | Keep as optional code route only when quota allows; do not make it required. |
| Kimi | Authentication failed | Do not route production work until credential is fixed. |
| ElevenLabs STT | Quota-limited for long audio | Use only for short/high-priority transcription unless quota is confirmed. |

## Default V8 Task Policies

| Task Type | Primary | Fallback | Structured Output Required |
|---|---|---|---|
| `corpus_summary` | Gemini | DeepSeek | Yes |
| `research_validation` | Perplexity | Browser extraction + Gemini | Yes |
| `code_generation` | OpenAI-compatible if healthy | DeepSeek | Yes |
| `lead_parse` | Gemini Flash | DeepSeek/local | Yes |
| `quote_draft` | DeepSeek or OpenAI-compatible | Gemini | Yes, with pricing validation |
| `review_message_draft` | Gemini | DeepSeek | Yes, with compliance checklist |
| `geo_audit` | Perplexity + deterministic scanner | Gemini | Yes |
| `memory_write` | Deterministic rules first | LLM only for summarization | Yes, with provenance |

## Safety Boundary

A model may recommend, draft, classify, or summarize. A model must not independently send SMS, email, incentives, public posts, payments, or CRM writes. High-impact actions require a workflow state that proves authorization and creates an audit event before execution.
