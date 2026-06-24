# Proposal: Define Processor Transfer Vendor Standard

## Intent

Add stage 41: a one-person-company standard for vendors that process customer data, including processor/service-provider role assessment, DPA/contract checks, subprocessor monitoring, international transfer or data residency impact, and vendor review.

## Scope

- Define required `vendor-risk/` artifacts for each production target that sends customer data, customer content, personal data, prompts, responses, logs, support data, files, RAG content, or embeddings to vendors.
- Cover processor registers, DPA/contract checklists, subprocessor watch records, transfer impact records, and recurring vendor reviews.
- Connect Go/Kratos/sqlc/gRPC vendor client boundaries, Vite trust UI, AI provider data controls, data rights workflows, audit evidence, and SRE dependency health.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Formal legal advice, contract negotiation, DPA/SCC/BAA drafting, or attorney review.
- Replacing cost/vendor lock-in, security/privacy baseline, trust policy, customer data lifecycle, or audit evidence standards.
- Full third-party risk management, procurement workflow, vendor questionnaire platform, or GRC system.
- Performing actual production vendor onboarding, data transfer, legal notice, or customer contract updates.

## Sources

- The Mythical Man-Month, small project management, Security Engineering, Software Engineering at Google dependency management.
- GDPR Articles 28, 30, 32, 33, 44, 46; EDPB controller/processor and supplementary transfer measures guidance.
- CCPA/CPRA service provider and contractor contract requirements; FTC AI privacy and confidentiality guidance.
- NIST SP 800-161 Rev. 1 Update 1, ISO/IEC 27036, OWASP LLM Top 10 supply chain risks.
- Google SRE SLO guidance for services with dependencies.
- OpenAI DPA, Data Controls, Enterprise Privacy, and Sub-processor List.

## Human Attention

Keep human judgment only for:

- sending customer content, personal data, prompts, responses, files, logs, support data, or vector/RAG data to a new vendor;
- sensitive, regulated, minor, high-impact, or contract-restricted data;
- missing or weak DPA/contract, deletion assistance, breach notice, audit/assurance, or subprocessor transparency;
- model training, feedback sharing, eval/fine-tuning sharing, human review, or longer retention;
- cross-border, region, residency, endpoint, ZDR, BAA/HIPAA, SCC, or supplementary-measure decisions;
- vendor role changes to independent controller, joint controller, advertising/analytics reuse, or data broker risk;
- critical path vendors without fallback, exit path, SLO explanation, or customer notice.
