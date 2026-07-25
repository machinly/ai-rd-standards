# Design: RAG Retrieval Source Standard

## Context

RAG is a data pipeline plus an AI behavior contract. Previous stages define memory/context, eval data, async jobs, observability, AI tool runtime, security, privacy, and audit evidence, but a production RAG feature also needs source admission, ingestion, chunk metadata, retrieval filters, citations, deletion/reindex, and poisoning defenses.

The one-person-company default is deliberately small: use Postgres full-text search, pgvector, or OpenAI hosted vector stores until scale or recall requirements justify a separate vector platform. The control point is not the database choice; it is whether each retrieved chunk has provenance, scope, freshness, permissions, and a citation path.

## Decisions

- Use `rag/` as the RAG governance folder.
- Require five artifacts per production RAG capability:
  - `source-registry/<capability>.json`
  - `ingestion-pipeline/<capability>.md`
  - `retrieval-policy/<capability>.json`
  - `citation-grounding/<capability>.md`
  - `rag-eval-review/<capability>.md`
- Treat retrieved context as untrusted context, never as system/developer instructions.
- Require retrieval controls for source allowlist, tenant scope filter, access check, freshness, sensitivity, max results, max tokens, score threshold, prompt-injection scan, citation, low-confidence fallback, deletion/reindex path, and telemetry.
- Require eval coverage for answerable, unanswerable, stale, conflicting, wrong-tenant, deleted, sensitive, prompt-injected, missing-citation, low-confidence, latency, and cost cases.
- Keep human attention on source admission, sensitive data, cross-tenant sharing, rights, low-confidence behavior, embedding/vector-store changes, deletion exceptions, and high-impact output.

## Alternatives Considered

- Fold RAG into stage 29 memory/context: too broad; long-term memory and RAG source pipelines have different failure modes.
- Require a dedicated vector database: premature for one-person-company scale and operational capacity.
- Rely only on hosted File Search: convenient, but still requires source, rights, retention, deletion, and citation governance.
- Store chunks and examples directly in governance artifacts: unsafe for customer content, secrets, copyrighted material, and personal data.

## Rollout

1. Add the stage 36 standard and OpenSpec spec.
2. Create `rag-retrieval-source-guard`.
3. Add a verifier for required artifacts, JSON shape, required retrieval controls, source fields, human checkpoints, headings, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
