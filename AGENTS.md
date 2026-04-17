# AGENTS.md

## Mission

PhantomScope exists to demonstrate a credible, defensible, analyst-oriented cyber security product focused on phishing infrastructure, typosquatting, brand impersonation, and suspicious external assets.

The repository should evolve as if it were an internal security engineering product:

- practical
- explainable
- defensive
- auditable
- modular
- suitable for portfolio review by technical interviewers

Codex should operate as a senior product security engineer building a realistic defensive platform, not a prototype generator and not a generic dashboard builder.

## Product Direction

- Build for defensive OSINT and threat intelligence workflows.
- Prioritize analyst usefulness over visual novelty.
- Prefer realistic workflows, evidence handling, and triage quality over superficial feature breadth.
- Treat AI as an acceleration layer for summarization and prioritization, never as the source of record.
- Keep all important detection, scoring, and prioritization logic reviewable by a human analyst.

## Architecture Principles

- Keep the system modular and domain-oriented.
- Separate concerns clearly across discovery, enrichment, scoring, summarization, reporting, API, persistence, and UI.
- Prefer explicit domain models over loose dictionaries when the shape is known.
- Keep business logic in services and domain modules, not buried inside routes or UI callbacks.
- Prefer adapters for external services so providers can be swapped without rewriting core logic.
- Design storage and interfaces so SQLite can be replaced by Postgres later with minimal churn.
- Build for partial failure: external providers may timeout, rate limit, or return incomplete data.
- Prefer deterministic core workflows with bounded side effects.
- Maintain structured logging for operationally meaningful events.

## Security Rules

- Never commit secrets, tokens, API keys, or real credentials.
- Read secrets only from environment variables or approved secret-loading mechanisms.
- Sanitize and normalize all user-controlled inputs before using them.
- Apply timeouts and bounded retries to network calls.
- Fail safely when external providers are unavailable.
- Do not add active or offensive capabilities.
- Do not implement aggressive scraping, abusive collection, credential use against third-party systems, or anything that looks like unauthorized probing.
- Keep the project defensive, ethical, and safe for public portfolio presentation.
- Avoid logging secrets, raw credentials, or sensitive user-provided values unnecessarily.

## Domain Modeling Rules

- Write code that reflects the problem domain clearly: domains, observations, enrichments, risk signals, findings, summaries, and reports should be represented explicitly.
- Prefer names that match analyst language and security workflows.
- Avoid generic helper abstractions that obscure the threat intelligence use case.
- Keep logic explainable enough that a reviewer can trace why a domain was prioritized.
- Preserve a clean boundary between raw evidence, derived heuristics, and analyst narrative.

## Risk Scoring Policy

- Risk scoring must remain deterministic, rule-based, and explainable.
- Every non-trivial score contribution should map to a named signal or rule with a human-readable reason.
- Do not let LLM output directly set or override risk scores.
- If scoring evolves, preserve auditability and keep historical reasoning understandable.
- Prefer additive, transparent rules over opaque weighting schemes.

## AI Usage Policy

- AI may summarize, cluster, translate technical findings into analyst language, and help prioritize review.
- AI must never invent evidence, infrastructure, attribution, or confidence that is not supported by collected data.
- AI output must be grounded in known findings and clearly separated from deterministic facts.
- When AI is unavailable, the system must still produce a usable deterministic summary.
- If a claim cannot be supported by observed data, state uncertainty rather than filling gaps.

## External Integration Policy

- Always prefer provider adapters for CT logs, RDAP, DNS, ASN, reputation, or future enrichment sources.
- Keep external API usage encapsulated behind clear interfaces.
- Handle provider errors, schema drift, empty results, and rate limiting explicitly.
- Support offline or mock-backed execution for demos, tests, and interviews.
- Avoid tight coupling between one provider's response schema and core domain logic.

## Python Style Rules

- Target Python 3.12+ features when they improve clarity.
- Use type hints consistently on public functions, methods, and domain models.
- Prefer Pydantic models for validated request, response, and domain transfer structures.
- Keep functions focused and reasonably small.
- Prefer explicit names over abbreviations.
- Use dataclasses or Pydantic models instead of ad hoc nested dictionaries where practical.
- Raise specific errors where the caller can act on them.
- Add concise comments only when the code would otherwise be difficult to understand.
- Avoid cleverness that makes security logic harder to review.
- Favor readability over micro-optimizations unless profiling shows otherwise.

## Dependency Policy

- Prefer the existing project stack unless there is a strong reason to change it.
- Do not add heavy dependencies without a written justification in the task summary or README update.
- Prefer standard library or already-installed project dependencies when they are sufficient.
- New dependencies should be narrow, well-maintained, and aligned with defensive product needs.
- Avoid vendor lock-in in core workflows where a thin adapter can contain it.

## Testing Policy

- Always create or update tests when changing critical logic.
- Critical logic includes normalization, domain generation, enrichment mapping, scoring, reporting, persistence, and security-relevant behavior.
- Prefer focused tests that validate behavior and decision logic rather than implementation details.
- Avoid fragile mocks that simply mirror the implementation.
- Prefer stable fixtures, deterministic fake data, and contract-oriented provider tests where possible.
- Add regression tests when fixing a bug.
- If tests cannot be run in the environment, state that explicitly in the final summary.

## Documentation Policy

- Always update `README.md` when there is a relevant change to product scope, architecture, setup, usage, or roadmap.
- Keep documentation aligned with the actual behavior of the codebase.
- Write docs as if a recruiter, hiring manager, or senior security engineer may read them first.
- Prefer concise, technically credible documentation over marketing language.
- Document important architectural decisions when they affect contributor behavior.

## Implementation Preferences

- Keep routes thin.
- Keep UI code focused on presentation and orchestration, not detection logic.
- Prefer composition over hard-coded branching across providers.
- Preserve a clean path for future background jobs, scheduling, and PostgreSQL migration.
- Default to offline-safe demos when live access is unavailable.
- Use structured outputs for reports and exports.

## Completion Requirements

Before closing a task, Codex should:

- run lint if configured and feasible
- run tests relevant to the changes if feasible
- mention what was validated and what was not
- update README when the change is materially user-facing or architecturally relevant
- ensure new or changed critical logic is covered by tests

If lint or tests cannot be run, say so explicitly and explain why briefly.

