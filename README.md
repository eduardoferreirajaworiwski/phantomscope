# PhantomScope

`PhantomScope` is a defensive threat intelligence portfolio project focused on one concrete use case: detecting suspicious domains and infrastructure that may be used for phishing, typosquatting, brand impersonation, and external attack surface abuse.

It is designed to look and behave like an analyst-facing internal tool rather than a generic dashboard. The MVP ingests a target brand or domain, generates suspicious domain variations, correlates them with certificate transparency activity, enriches assets with registration and network context, applies explainable risk scoring, and produces analyst-ready triage summaries and reports.

## Why this project exists

This project is built to demonstrate practical capability across:

- Threat Intelligence
- Digital Risk Protection
- SecOps
- Security Automation
- External Attack Surface Monitoring
- AI-assisted security workflows with explainable outputs

The emphasis is defensive and enterprise-oriented:

- no offensive actions
- no aggressive scraping
- auditable scoring logic
- provider adapters with failure isolation
- offline demo mode for interviews and portfolio walkthroughs

## Core MVP capabilities

- Brand or domain input
- Suspicious domain variation generation
- Certificate Transparency lookup
- DNS, RDAP/WHOIS-style, IP, ASN, and basic reputation enrichment
- Explainable risk scoring with explicit reasons
- AI-assisted analyst narrative with deterministic fallback
- Functional Streamlit dashboard
- Markdown and JSON report export

## Architecture

PhantomScope is split into clear modules so the analysis pipeline remains explainable and portable:

- `api`: FastAPI routes and request lifecycle
- `services`: orchestration layer for end-to-end analysis
- `discovery`: target normalization, brand extraction, suspicious variation generation, CT collection
- `enrichment`: RDAP, DNS, IP, ASN, and reputation enrichment
- `scoring`: explicit, auditable risk rules
- `summarization`: analyst-facing triage narrative and optional LLM adapter
- `reporting`: Markdown and JSON export
- `providers`: external provider adapters and offline mock data
- `db`: SQLite persistence layer designed to be replaceable later
- `app`: Streamlit frontend

## Threat model and product direction

PhantomScope is intentionally not a news aggregator and not a placeholder dashboard. It addresses a realistic analyst workflow:

1. Monitor a brand or domain.
2. Identify suspicious lookalike assets.
3. Pull surrounding infrastructure context.
4. Prioritize what deserves analyst attention.
5. Export findings into a reportable format.

## Quickstart

### 1. Install dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
```

Recommended for local demo:

```bash
PHANTOMSCOPE_OFFLINE_MODE=true
```

### 3. Start the API

```bash
uvicorn phantomscope.api.main:app --reload
```

### 4. Start the dashboard

```bash
streamlit run app/dashboard.py
```

## Example API usage

Analyze a brand in offline demo mode:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{
    "target": "Acme",
    "target_type": "brand",
    "offline_mode": true,
    "max_variants": 12
  }'
```

Analyze a domain:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{
    "target": "acme.com",
    "target_type": "domain",
    "offline_mode": true,
    "max_variants": 10
  }'
```

Fetch a previous result:

```bash
curl http://127.0.0.1:8000/api/v1/analyses/<analysis_id>
```

## Example Streamlit workflow

1. Enter a brand or domain.
2. Choose offline demo mode or live provider mode.
3. Run the analysis.
4. Review suspicious domains ranked by risk score.
5. Export the report as Markdown or JSON.

## Roadmap

### MVP

- End-to-end analysis pipeline
- Offline demo fixtures
- SQLite persistence
- FastAPI + Streamlit user flow
- Explainable scoring and analyst narrative

### V2

- Background jobs and scheduled monitoring
- Historical diffing and alerting
- Postgres migration
- More enrichment providers and passive DNS
- Entity clustering by shared infrastructure

### V3

- Case management
- Analyst feedback loop for score tuning
- Multi-tenant support
- Evidence graph and investigation timeline
- SOAR / ticketing integrations

## Directory layout

```text
phantomscope/
├── app/
│   └── dashboard.py
├── data/
│   └── mock/
├── docs/
│   └── roadmap.md
├── src/
│   └── phantomscope/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── discovery/
│       ├── enrichment/
│       ├── models/
│       ├── providers/
│       ├── reporting/
│       ├── scoring/
│       ├── services/
│       ├── summarization/
│       └── utils/
├── tests/
├── Dockerfile
└── pyproject.toml
```

## Security notes

- Secrets are injected via environment variables only.
- Network adapters use timeouts and bounded retries.
- Inputs are normalized before processing.
- The project is defensive by design and avoids active probing or abuse patterns.

## Portfolio positioning

This project is intended to communicate:

- that you understand how phishing infrastructure is identified in practice
- that you can translate security workflows into maintainable software
- that you can separate deterministic logic from AI-assisted acceleration
- that you can design systems with realistic provider abstractions and operational constraints

