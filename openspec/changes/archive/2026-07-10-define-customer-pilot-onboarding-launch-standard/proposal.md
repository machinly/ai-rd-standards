# Proposal: Define Customer Pilot Onboarding Launch Standard

## Intent

Add stage 49: a one-person-company standard for customer pilots, tenant provisioning, launch readiness, customer success handoff, and exit/offboarding decisions.

## Scope

- Define required `customer-onboarding/` artifacts for design partners, private beta, pilots, paid pilots, and production customer launches.
- Cover pilot charters, tenant provisioning facts, launch readiness gates, success plans, and handoff reviews.
- Connect product discovery, auth/tenant isolation, billing, data lifecycle, AI eval/routing, support, commercial commitments, and release/SRE gates.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Replacing product discovery, tenant isolation, data lifecycle, billing, support, contracts, release, observability, or incident standards.
- Enterprise implementation playbooks, customer success platforms, professional services methodology, or full CRM workflows.
- Storing real customer names, emails, secrets, raw customer data, raw prompts/responses, payment data, or regulated content in onboarding artifacts.

## Sources

- The Mythical Man-Month and small project management.
- The Lean Startup, Customer Development, The Mom Test, and Crossing the Chasm.
- Google SRE Reliable Product Launches, Launch Checklist, and Production Readiness Review.
- Google Cloud Well-Architected operational readiness.
- AWS SaaS Lens tenant onboarding and operational excellence.
- OpenAI production, data, and safety best practices.
- Stripe go-live checklist.
- Gainsight and Intercom customer onboarding/customer success guidance.
- Kratos, sqlc, gRPC, Vite, and Vercel design references.

## Human Attention

Keep human judgment only for:

- moving a design partner/private beta to paid pilot or production;
- enabling real customer data import/sync, SSO/SCIM, live billing, production webhooks, AI on customer data, RAG, memory, tool actions, or external connectors;
- accepting failed, blocked, or accepted-risk required launch gates;
- committing custom features, roadmap, SLA, security/privacy terms, support windows, public references, or case studies;
- launching without rollback/offboarding/customer acceptance;
- using customer content in evals, demos, training, docs, or public claims.
