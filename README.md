# MEMORYRECALLAPP

This repository is the GitHub home for **LIFE-RECALLAPP / MEMORYRECALLAPP**.

V8 converts the project from a blank baseline into a recall-oriented, automation-capable, multi-tenant knowledge and workflow framework for Global Sales Force. The V8 sync opened the accessible ZIP archives, extracted and deduplicated their contents, arranged the corpus for efficient recall, generated knowledge packs, performed parallel corpus analysis, ran multi-LLM cross-checks, and produced the canonical V8 master plan and build prompt.

## V8 Entry Points

| Path | Purpose |
|---|---|
| `docs/v8/V8_MASTER_PLAN.md` | Full V8 architecture, roadmap, data model, module sequence, and compliance framework. |
| `docs/v8/V8_BUILD_PROMPT.md` | Canonical prompt for future V8 build agents. |
| `docs/v8/V8_LLM_ROUTING_FRAMEWORK.md` | Provider selection, fallback, health, schema-validation, and sensitive-data routing policy. |
| `docs/v8/V8_TOP_DOWN_DIG_REPORT.md` | Evidence report for ZIP discovery, extraction, deduplication, corpus organization, and cross-checking. |
| `v8_project_corpus/README.md` | Extraction summary and corpus navigation. |
| `v8_project_corpus/knowledge_extracts/v8_knowledge_extract_index.md` | Recall-optimized index of generated knowledge packs. |
| `v8_project_corpus/manifests/` | Archive, file, duplicate, exclusion, and nested-archive manifests. |
| `v8_project_corpus/organized_files/` | Deduplicated extracted project corpus; no ZIP files remain in this organized tree. |

## Security Position

The V8 sync intentionally excludes credentials, private connector configuration, `.env` files, browser state, passwords, API keys, and files flagged as sensitive/private candidates. Original ZIP files were not committed because their extracted unique contents are now organized for direct recall and committing both would create unnecessary redundancy.

## Current V8 Direction

The recommended framework is a modular multi-tenant app with a React/TypeScript UI, tenant-aware data model, hybrid RAG plus stateful memory, workflow execution layer, LLM routing gateway, and compliance-first automation controls. Future agents should start with `docs/v8/V8_BUILD_PROMPT.md` and `docs/v8/V8_MASTER_PLAN.md` before making implementation changes.
