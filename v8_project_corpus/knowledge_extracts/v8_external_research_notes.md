# V8 External Research Notes

The V8 architecture research surfaced four useful current references. Atlan’s April 2026 analysis distinguishes **RAG** as stateless retrieval from **AI memory** as stateful persistence, recommending that production agents use both with governed inputs rather than treating vector search as memory. The Supabase/Legend-State local-first reference shows an Expo-compatible pattern where offline changes are persisted locally, retried, and synced to Supabase with created/updated/deleted fields. The Vercel AI SDK Next.js App Router reference confirms that a TypeScript AI application can expose streaming route handlers, model-provider routing, schema-validated tools through Zod, and React chat UI hooks. The multi-tenant architecture reference reinforces tenant identifiers, row-level security, OAuth/OIDC, encryption, monitoring, and automated onboarding as core SaaS controls.

| Reference | V8 Takeaway |
|---|---|
| Atlan, AI Memory System vs RAG | Build separate layers for corpus retrieval and persistent user/project memory; govern the source of truth before writing memories. |
| Supabase, Local-first Realtime Apps with Expo and Legend-State | Use local persistence with retryable sync, generated IDs, updated timestamps, soft deletes, and realtime subscriptions where mobile/offline UX matters. |
| Vercel AI SDK, Next.js App Router | Use streaming model routes, provider abstraction, and schema-validated tools for agentic workflows. |
| Multi-tenant SaaS guidance | Implement tenant isolation, RBAC, encryption, onboarding automation, and audit logging from the start. |

## References

[1]: https://atlan.com/know/ai-memory-system-vs-rag/ "AI Memory System vs RAG: The Enterprise Architecture Decision"
[2]: https://supabase.com/blog/local-first-expo-legend-state "Local-first Realtime Apps with Expo and Legend-State"
[3]: https://ai-sdk.dev/docs/getting-started/nextjs-app-router "Next.js App Router Quickstart"
[4]: https://ramamtech.com/blog/scalable-secure-multi-tenant-apps "How to Build Multi-Tenant Web Apps That Scale Safely and Securely"

## Compliance Findings Added

The FTC’s official business guidance emphasizes that customer reviews and endorsements must meet FTC Act standards and the Consumer Reviews and Testimonials Rule. The FTC’s 2024 final rule specifically prohibits fake or false consumer reviews, buying positive or negative reviews where compensation is conditioned on sentiment, undisclosed insider reviews, company-controlled review sites misrepresented as independent, review suppression, and fake social media indicators.[5] These rules directly inform V8 guardrails for review solicitation: the system may request honest feedback, but it must not generate fake reviews, condition incentives on sentiment, suppress negative feedback, or automate deceptive community activity.

[5]: https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials "Federal Trade Commission Announces Final Rule Banning Fake Reviews and Testimonials"
