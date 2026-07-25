# Change: Define Infra IaC Environment Standard

## Why

Existing standards cover release pipelines, runtime configuration, cost/capacity, security/privacy, backup/recovery, observability, and audit evidence. They do not yet define one focused standard for infrastructure-as-code source of truth, environment topology, cloud resource inventory, state backends, provisioning, manual changes, drift, and decommissioning.

Without this standard, a one-person company can lose control of production infrastructure: resources are created through cloud consoles, staging differs from production in undocumented ways, Terraform/OpenTofu state contains sensitive values, manual hotfixes never return to code, drift is invisible, and destroy/decommission actions risk data loss.

## What

- Add a stage 37 standard for infrastructure-as-code, environment topology, cloud resources, state, provisioning, and drift governance.
- Define five minimal artifacts under `infra/`.
- Require environment map, resource inventory, IaC change policy, provisioning runbook, and drift review for production targets.
- Define human checkpoints for new accounts/environments/regions/state backends, production apply/destroy, database/storage/IAM/network/public exposure changes, state operations, manual drift exceptions, backup/encryption/monitoring reductions, and high-cost platform changes.
- Create `infra-iac-environment-guard` skill and verifier.

## Impact

- Go/Kratos/sqlc/gRPC services get a clear runtime, network, secret, state, and database-resource map.
- Vite frontends get preview/staging/production environment, DNS/TLS, env boundary, rollback, and promote expectations.
- AI workflows map provider keys, vector/file stores, workers, batch jobs, tool sandboxes, and model-route dependencies into cloud resource governance.
- The solo founder reviews only high-risk infrastructure choices; artifact shape, required fields, sensitive-state screening, and fixture validation are automated.
