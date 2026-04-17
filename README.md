# PhantomScope

PhantomScope is a defensive threat-intelligence and external attack-surface analysis project focused on one concrete business problem: identifying suspicious domains and supporting infrastructure that may be used for phishing, typosquatting, brand impersonation, and abusive external asset exposure.

It is intentionally designed as an analyst-oriented internal security product rather than a generic security dashboard. The project demonstrates how to turn a recognizable cyber defense workflow into a modular, explainable, portfolio-grade application with clear architectural boundaries and interview-ready storytelling.

## Business Problem

Security teams responsible for digital risk, brand protection, and phishing response face a recurring operational challenge:

- suspicious lookalike domains appear before incidents are fully confirmed
- infrastructure context is scattered across multiple external sources
- prioritization is often manual, inconsistent, or opaque
- executive stakeholders want concise summaries, while analysts need evidence and rationale

PhantomScope addresses that gap by taking a target brand or domain and producing a ranked, explainable triage view of suspicious external assets.

## What PhantomScope Does

- accepts a target brand or domain
- generates typosquatting and phishing-lure domain candidates
- queries Certificate Transparency activity through `crt.sh`
- enriches findings with DNS, RDAP, IP, ASN, registrar, and related context when available
- calculates a deterministic, explainable risk score
- produces an analyst summary with optional AI assistance grounded on structured findings
- exposes results through a FastAPI backend and a Streamlit dashboard
- exports findings as JSON and Markdown reports

## Why This Project Matters

This repository is meant to communicate senior-level engineering judgment in a security context:

- clear architectural separation between generation, collection, enrichment, scoring, summarization, and reporting
- deterministic security logic separated from AI-assisted narrative generation
- explicit handling of provider failure, retries, timeouts, and offline demo continuity
- realistic analyst workflow instead of a generic “SOC dashboard”
- defensive-only posture suitable for public portfolio review

## Architecture

PhantomScope is organized by domain responsibility so the analysis flow remains easy to audit and evolve:

- `api`: FastAPI application, routing, and service wiring
- `services`: end-to-end orchestration of the analysis workflow
- `models`: Pydantic schemas for requests, evidence, findings, summaries, and exports
- `discovery`: target normalization and suspicious domain generation
- `collectors`: evidence collection abstractions such as CT collection
- `enrichment`: orchestration of infrastructure enrichment
- `providers`: external adapters, HTTP client behavior, and offline fixture-backed providers
- `scoring`: deterministic risk signals and score rationale generation
- `ai`: AI-assisted summary generation with deterministic fallback
- `reporting`: Markdown and JSON export
- `db`: SQLite persistence for stored analysis runs
- `app`: Streamlit analyst dashboard

### Architectural Principles

- deterministic, reviewable risk logic
- explicit provenance of evidence as `live`, `mock`, or `fallback`
- provider isolation with bounded failure behavior
- thin API routes, business logic in services
- portfolio-safe, defensive-only behavior

## Data Pipeline

```text
Target Input
  -> Target Normalization
  -> Domain Candidate Generation
  -> CT Collection
  -> Infrastructure Enrichment
  -> Deterministic Risk Scoring
  -> AI-Assisted Analyst Summary
  -> Report Export
  -> API Response / Streamlit Dashboard / Persistence
```

### Pipeline Stages

1. A target brand or domain is normalized into a `TargetProfile`.
2. Candidate domains are generated using lookalike and lure-oriented patterns.
3. CT evidence is collected through a provider-backed collector.
4. Infrastructure context is enriched through DNS resolution and RDAP-derived metadata when available.
5. Rule-based scoring emits named `RiskSignal` entries with weights, reasons, and evidence.
6. AI optionally summarizes the structured output without modifying the risk score.
7. Findings are rendered in the dashboard and exported to Markdown and JSON.

## Stack

- Backend: FastAPI
- Frontend: Streamlit
- Validation and schemas: Pydantic v2
- HTTP client: `httpx`
- Persistence: SQLite
- Packaging: `pyproject.toml`
- Linting: `ruff`
- Tests: `pytest`
- Containerization: Docker

## Dashboard and Screenshots

Place screenshots or a GIF in `docs/screenshots/` and reference them here once captured.

Suggested capture set:

1. `dashboard-overview.png`
   Show the hero section, top metrics, and analyst summary.
2. `ranked-findings.png`
   Show two or three findings with score rationale visible.
3. `finding-detail.png`
   Show CT observations, infrastructure context, and signal breakdown.
4. `export-view.png`
   Show Markdown/JSON export options.
5. `phantomscope-demo.gif`
   Show the 60-90 second flow described later in this README.

Capture guidance:

- run the project in offline mode for stable visuals
- use a consistent browser width around 1440px
- use the same example target across captures, such as `acme` or `acme.com`
- ensure at least one screenshot shows `MOCK` provenance clearly to reinforce honesty in the demo

If you want a lightweight placeholder now, keep `docs/screenshots/README.md` in the repo so visitors know where visuals will be added.

## Demo Workflow

Recommended interview workflow:

1. Launch the project in offline mode.
2. Enter a target such as `acme`.
3. Show the generated candidate count and ranked findings.
4. Open the top finding and walk through:
   the technique, the triggered risk signals, the infrastructure context, and the CT evidence.
5. Highlight that the score is deterministic and that mock evidence is explicitly labeled.
6. Show the analyst narrative and recommended actions.
7. Export the Markdown report and explain how it would feed an analyst or abuse-response workflow.

## 60-90 Second Demo Flow

Suggested short-form recording or interview flow:

1. Open the dashboard landing view with PhantomScope already running.
2. Enter `acme` as the target and keep offline mode enabled.
3. Start the analysis and let the ranked findings load.
4. Pause briefly on the top metrics and headline summary.
5. Open the top-ranked finding and highlight:
   score, technique, CT evidence, infrastructure context, and named risk signals.
6. Point out that the score is deterministic and that evidence provenance is visible as `MOCK` or `LIVE`.
7. Switch to the narrative/export area and show the Markdown download.
8. End on the message that the project turns phishing infrastructure triage into an explainable analyst workflow.

Ideal GIF shape:

- duration: 60-90 seconds
- format: silent screen capture or light voiceover
- screen width: desktop layout
- target example: `acme`
- key visual moments: search input, findings list, one finding detail, export action

## Quickstart

### Install

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

Or:

```bash
make install
```

Or with `pip` requirements files:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
```

### Configure

```bash
cp .env.example .env
```

For a stable local demo:

```bash
PHANTOMSCOPE_OFFLINE_MODE=true
```

### Start the API

```bash
make api
```

### Start the dashboard

```bash
make dashboard
```

### Run the interview demo helper

```bash
make demo-interview
```

This launches the API and Streamlit dashboard together in offline mode and prints the URLs needed for a live walkthrough.

## Render Deployment

PhantomScope is ready to deploy on Render as two web services:

- `phantomscope-api`: FastAPI backend
- `phantomscope-dashboard`: Streamlit frontend

The repository already includes the pieces Render expects:

- code in GitHub
- `requirements.txt` and `requirements-dev.txt`
- FastAPI app exposed from `phantomscope.api.main:app`
- Streamlit entrypoint at `app/dashboard.py`
- `.env.example`
- healthcheck endpoint at `/api/v1/health`
- environment-variable based configuration through `pydantic-settings`

### Recommended Render setup

Use the included [render.yaml](/home/eduardo/projects/phantomscope/render.yaml:1), or create the services manually in the Render dashboard.

### API service

- Service type: `Web Service`
- Build command: `pip install -r requirements-dev.txt && pip install -e .`
- Start command: `uvicorn phantomscope.api.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/api/v1/health`

Suggested environment variables:

- `PHANTOMSCOPE_ENV=production`
- `PHANTOMSCOPE_LOG_LEVEL=INFO`
- `PHANTOMSCOPE_OFFLINE_MODE=true`
- `PHANTOMSCOPE_DATABASE_URL=sqlite:///./phantomscope.db`

### Dashboard service

- Service type: `Web Service`
- Build command: `pip install -r requirements-dev.txt && pip install -e .`
- Start command: `streamlit run app/dashboard.py --server.port $PORT --server.address 0.0.0.0`

Required environment variables:

- `PHANTOMSCOPE_ENV=production`
- `PHANTOMSCOPE_LOG_LEVEL=INFO`
- `PHANTOMSCOPE_OFFLINE_MODE=true`
- `PHANTOMSCOPE_DASHBOARD_API_URL=https://<your-api-service>.onrender.com/api/v1/analyses`

### Notes

- For a stable portfolio demo, keep `PHANTOMSCOPE_OFFLINE_MODE=true`.
- SQLite is acceptable for MVP/demo deployment, but not ideal for stronger production-style persistence.
- If you enable live mode later, configure any provider-specific environment variables through the Render dashboard.

## API Example

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyses \
  -H "Content-Type: application/json" \
  -d '{
    "target": "acme",
    "target_type": "brand",
    "offline_mode": true,
    "max_variants": 12
  }'
```

Additional useful endpoints:

- `GET /api/v1/analyses` returns recent stored runs for operational review
- `GET /api/v1/analyses/{analysis_id}` returns a previous full analysis payload
- `GET /api/v1/health` returns API status, environment, version, and offline-mode state

## Security Considerations

- The project is defensive-only and avoids active or abusive collection behavior.
- Secrets are read from environment variables only.
- Inputs are sanitized before processing.
- Provider access is wrapped with timeouts and bounded retries.
- Fallback behavior is explicit rather than silent.
- AI is used for summarization only and does not set or override the risk score.
- Mock data is marked as mock to avoid presenting synthetic evidence as real intelligence.

## Validation and Testing

Current test focus includes:

- schema validation and target sanitization
- scoring behavior and rationale output
- end-to-end offline analysis flow
- API integration covering create, fetch, list, and structured validation errors

## Limitations

- The current CT workflow uses a single public source: `crt.sh`.
- DNS enrichment is intentionally conservative and avoids active probing.
- ASN and country context depend on RDAP/IP data availability.
- Offline mode is designed for reliable demos, not as a full fidelity simulation environment.
- SQLite is sufficient for a portfolio MVP but not ideal for multi-user or scheduled-monitoring production workloads.
- The Streamlit UI is suitable for demo and analyst review, but not yet optimized for larger case-management workflows.

## Future Roadmap

### Next Practical Improvements

- add provider contract tests for CT and RDAP adapters
- introduce additional CT and passive-DNS sources
- add historical diffing and scheduled monitoring
- cluster findings by registrar, nameserver, ASN, and hosting overlap
- move persistence behind a stronger repository abstraction for PostgreSQL migration
- add API integration tests and report snapshot tests

### Stronger 1.0 Direction

- background jobs and recurring analysis
- investigation history and case timeline
- analyst feedback loop for tuning rules
- alerting and webhook integration
- richer campaign/entity clustering
- stronger visual reporting assets for portfolio presentation

## Repository Structure

```text
phantomscope/
├── app/
│   └── dashboard.py
├── data/
│   └── mock/
├── docs/
│   ├── portfolio-copy.md
│   ├── roadmap.md
│   └── screenshots/
├── scripts/
│   └── demo_interview.sh
├── src/
│   └── phantomscope/
│       ├── ai/
│       ├── api/
│       ├── collectors/
│       ├── core/
│       ├── db/
│       ├── discovery/
│       ├── enrichment/
│       ├── models/
│       ├── providers/
│       ├── reporting/
│       ├── scoring/
│       ├── services/
│       └── summarization/
├── tests/
├── .env.example
├── Dockerfile
├── Makefile
└── pyproject.toml
```

## Interview Positioning

If you are presenting this project to a recruiter, hiring manager, or technical interviewer, the core message is:

PhantomScope demonstrates the ability to model a realistic security problem, design a modular analysis pipeline, preserve explainability in risk scoring, use AI responsibly, and build a portfolio-safe product that still feels operationally credible.
