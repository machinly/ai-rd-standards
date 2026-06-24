# Change: Define RAG Retrieval Source Standard

## Why

Existing standards cover AI prompt/eval, datasets, memory/context, tool runtime, async jobs, observability, trust claims, and audit evidence. They do not yet define one focused standard for RAG source admission, ingestion, chunking, embedding, retrieval filters, citation/grounding, poisoning controls, deletion/reindex, and RAG-specific eval review.

Without this standard, a RAG feature can quietly become a production data boundary: unauthorized documents are indexed, stale chunks answer user questions, tenant filters are applied after retrieval, citations are invented, malicious retrieved text acts like instructions, and deletion requests fail to reach embeddings or hosted vector stores.

## What

- Add a stage 36 standard for AI RAG, knowledge sources, retrieval, citation, and grounding governance.
- Define five minimal artifacts under `rag/`.
- Require source registry, ingestion pipeline, retrieval policy, citation/grounding rules, and RAG eval review for production RAG capabilities.
- Define human checkpoints for new external/private sources, sensitive/customer data indexing, cross-tenant sharing, unclear content rights, low-confidence answers, embedding/vector-store changes, deletion/reindex exceptions, and high-impact RAG output.
- Create `rag-retrieval-source-guard` skill and verifier.

## Impact

- Go/Kratos/sqlc/gRPC systems get a clear source/chunk/index/retrieval/citation data model.
- Vite knowledge-source and answer surfaces get explicit source status, citations, low-confidence states, and deletion/reindex actions.
- AI workflows treat retrieved context as untrusted data and require citation or fallback for fact claims.
- The solo founder reviews only high-risk source, rights, sensitivity, cross-tenant, deletion, and high-impact choices; artifact shape, required controls, headings, and sensitive-content screening are automated.
