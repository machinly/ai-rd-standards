# Proposal: define localization, locale, time, and AI language standard

## Why

Existing standards cover Vite frontend basics, notification templates, billing, accessibility, AI evals, and support. They do not define one focused lifecycle for language tags, locale fallback, text direction, time zones, date/number/currency formatting, localized message catalogs, or AI output language verification.

For a one-person AI company, localization bugs can directly affect trust: wrong billing cutoff timezone, mixed-language AI output, unreviewed machine translation, broken RTL layout, currency precision errors, or ambiguous incident/security timestamps.

## What Changes

- Add stage 55 for internationalization, localization, time zone, currency, and multilingual AI experience.
- Add `localization-locale-time-ai-standard`.
- Define five minimal artifacts under `localization/`.
- Create `localization-locale-ai-guard` skill and verifier.
- Update README and source map.

## Scope

- Locale policy, message catalog, time/currency rules, AI locale eval, and localization review.
- Go/Kratos/sqlc/gRPC handling of BCP 47 locale tags, IANA time zones, ISO 4217 currency, UTC storage, user preferences, and user-safe message keys.
- Vite frontend handling of `Intl`, `lang`, `dir`, pseudo-localization, RTL/BiDi, long text, and locale fallback.
- AI workflow handling of output language, locale-specific formatting, multilingual RAG, translation drafts, and language mismatch evals.

## Non-Goals

- Replacing stage 38 notification messaging governance.
- Replacing stage 22 billing ledgers or tax/invoice localization.
- Replacing stage 31 accessibility and AI UX governance.
- Defining a full translation management system, localization vendor process, marketing SEO localization, or formal legal translation.
- Supporting every locale at once.

## Source Anchors

- Brooks, `The Mythical Man-Month`, and small-project management: keep the locale model small and conceptually consistent.
- W3C Internationalization and String Metadata.
- IETF BCP 47 / RFC 5646.
- Unicode CLDR / LDML and Unicode Bidirectional Algorithm.
- IANA Time Zone Database and ISO 4217 currency codes.
- ECMAScript Intl API / W3C Intl guide.
- Go `time`, `golang.org/x/text/language`, and PostgreSQL date/time docs.
- OpenAI prompt engineering and eval guidance for language-specific behavior.

## Human Attention

Only escalate:

- adding official supported locales, RTL languages, paid countries/regions, or multi-currency display;
- unreviewed machine/AI translation on high-risk copy;
- billing, quota, trial, appointment, SLA, incident, notification, or export timezone changes;
- AI multilingual output for safety, billing, legal, medical, financial, permission, incident, or external-claim content;
- sending user content to external translation/LLM providers or changing data residency/processor boundaries.
