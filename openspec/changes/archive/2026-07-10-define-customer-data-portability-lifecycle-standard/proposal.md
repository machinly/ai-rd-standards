# Proposal: Define Customer Data Portability Lifecycle Standard

## Intent

Add stage 40: a one-person-company standard for customer data import, export, synchronization, data rights requests, and deletion propagation across application data, derived stores, AI stores, third parties, and backups.

## Scope

- Define required `customer-data/` artifacts for each production target that imports, exports, syncs, or deletes customer data.
- Cover data maps, transfer contracts, sync runbooks, rights/deletion policies, and lifecycle reviews.
- Connect Go/Kratos/sqlc/gRPC jobs, Vite data UX, AI memory/RAG/vector deletion, audit evidence, and privacy records.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Replacing database migration, webhook integration, backup recovery, audit evidence, RAG, or AI memory standards.
- Providing legal advice or formal GDPR/CCPA compliance certification.
- Building a data catalog, MDM platform, ETL platform, or enterprise privacy request portal.
- Performing actual production data deletion or export.

## Sources

- The Mythical Man-Month, small project management, Designing Data-Intensive Applications, Database Reliability Engineering.
- GDPR data subject rights, NIST Privacy Framework, NIST SP 800-88 Rev. 2, FTC personal information guidance.
- OWASP File Upload and CSV Injection, RFC 4180, Google SRE Data Processing Pipelines, PostgreSQL COPY.
- OpenAI data controls for AI application state and retention boundaries.

## Human Attention

Keep human judgment only for:

- new customer data categories, processors, sync targets, cross-product flows, or cross-border transfers;
- sensitive, restricted, customer-confidential, payment, identity, health, legal, financial, minor, or high-impact data import/export;
- irreversible deletion, bulk deletion, tenant deletion, account merge, bidirectional sync, or production restore overwrite;
- deletion exceptions such as billing/tax, security/audit, fraud, legal hold, contract obligations, backup retention, or supplier inability;
- sending customer files, raw prompts/responses, support data, or import samples to AI/model providers;
- sharing export packages, migration packages, audit packages, recipient lists, or deletion proof externally.
