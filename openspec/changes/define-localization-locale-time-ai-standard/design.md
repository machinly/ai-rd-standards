# Design: localization, locale, time, and AI language standard

## Decision

Add a narrow localization governance layer under:

```text
localization/
  locale-policy/<target>.json
  message-catalog/<target>.json
  time-currency-rules/<target>.md
  ai-locale-eval/<target>.json
  localization-review/<target>.md
```

This layer records which locales are genuinely supported, how fallback works, how time and currency are stored/displayed, and how AI multilingual behavior is verified. It does not manage full translation operations.

## Artifact Shape

- `locale-policy`: default locale, supported locales, BCP 47 tags, text direction, fallback, timezone, currency, routing/persistence, linked artifacts, and checkpoints.
- `message-catalog`: stable message ids, namespaces, default messages, descriptions, variables, plural/format policy, fallback, pseudo-localization, and high-risk copy checkpoints.
- `time-currency-rules`: human-readable UTC/IANA/ISO 4217 rules, database semantics, frontend formatting, scheduling/cutoff behavior, testing, and checkpoints.
- `ai-locale-eval`: multilingual eval cases with expected output locale, time zone, currency, scenario, assertions, failure modes, telemetry, and checkpoints.
- `localization-review`: recent changes, coverage, translation quality, time/currency findings, AI locale findings, direction/accessibility, feedback, open risks, and one next change.

## Human-Attention Defaults

The human decides official supported locales, RTL, paid countries/regions, high-risk translated copy, timezone/currency semantic changes, and external translation/LLM data boundaries. Codex can draft artifacts and run structural checks.

## Verifier

The skill verifier checks:

- required artifact presence;
- JSON required keys and markdown headings;
- BCP 47-like locale tags, `ltr`/`rtl`, IANA-looking timezone names, and ISO 4217-like currency codes;
- message ids, variable metadata, risk classes, fallback policy, pseudo-localization/test policy;
- time/currency rule sections are non-empty;
- AI eval cases cover at least one non-default locale and one formatting/timezone/currency assertion;
- high-risk locales/copy/AI cases have human checkpoints;
- artifacts do not contain secrets, raw prompts/responses, full user content, payment data, or unredacted personal data.

## Alternatives Considered

- Put localization into the Vite frontend standard: too frontend-only; backend time, database semantics, notifications, billing, and AI output language would remain scattered.
- Use only a translation vendor/platform: too heavy before real locale demand and still misses timezone/currency/AI behavior.
- Let the LLM translate on demand without artifacts: fast but unreviewable, hard to test, and unsafe for billing, security, legal, incident, and policy copy.

## Stack Notes

- Go/Kratos: parse and match locales with `golang.org/x/text/language`; keep message keys stable.
- sqlc/PostgreSQL: store instants as UTC semantics and store IANA zone names when local business meaning matters.
- gRPC: carry explicit `locale`, `time_zone`, `currency`, `message_key`, and user-safe error metadata.
- Vite: use `Intl` or a mature i18n library, set `lang`/`dir`, and test long/pseudo-localized strings.
- AI: prompts and evals must specify output locale and formatting expectations.
