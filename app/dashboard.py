from __future__ import annotations

import json

import httpx
import streamlit as st

from phantomscope.core.config import get_settings

settings = get_settings()
API_URL = settings.dashboard_api_url

st.set_page_config(page_title="PhantomScope", layout="wide")

st.markdown(
    """
    <style>
    :root {
      --bg: #06131a;
      --panel: #0c1d26;
      --panel-alt: #102733;
      --border: #1d4150;
      --text: #dbe7eb;
      --muted: #8da4ad;
      --accent: #9fe870;
      --high: #ff7b72;
      --medium: #ffd866;
      --low: #79c0ff;
    }
    .stApp {
      background:
        radial-gradient(circle at top right, rgba(159, 232, 112, 0.08), transparent 22%),
        radial-gradient(circle at top left, rgba(121, 192, 255, 0.10), transparent 28%),
        linear-gradient(180deg, #051018 0%, #07151d 100%);
      color: var(--text);
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", sans-serif;
    }
    .hero, .panel {
      border: 1px solid var(--border);
      background: linear-gradient(180deg, rgba(12, 29, 38, 0.92), rgba(9, 24, 31, 0.96));
      border-radius: 18px;
      padding: 1.2rem 1.3rem;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.22);
    }
    .hero h1, .hero h3 {
      margin: 0;
      color: var(--text);
    }
    .eyebrow {
      color: var(--accent);
      font-size: 0.82rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      margin-bottom: 0.45rem;
    }
    .muted {
      color: var(--muted);
    }
    .badge {
      display: inline-block;
      border-radius: 999px;
      padding: 0.18rem 0.65rem;
      font-size: 0.78rem;
      margin-right: 0.35rem;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.03);
    }
    .high { color: var(--high); border-color: rgba(255, 123, 114, 0.45); }
    .medium { color: var(--medium); border-color: rgba(255, 216, 102, 0.45); }
    .low { color: var(--low); border-color: rgba(121, 192, 255, 0.45); }
    .mock { color: var(--medium); }
    .live { color: var(--accent); }
    .finding {
      border: 1px solid var(--border);
      background: linear-gradient(180deg, rgba(16, 39, 51, 0.95), rgba(12, 29, 38, 0.95));
      border-radius: 16px;
      padding: 1rem;
      margin-bottom: 0.9rem;
    }
    .finding h4 {
      margin-bottom: 0.35rem;
    }
    .mono {
      font-family: "IBM Plex Mono", "SFMono-Regular", monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Defensive OSINT Portfolio Build</div>
      <h1>PhantomScope</h1>
      <p class="muted">
        Analyst-oriented triage for typosquatting, phishing lures and suspicious external infrastructure.
        The dashboard keeps deterministic evidence, score explanations and mock/live provenance visible.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Run Analysis")
    target = st.text_input("Target brand or domain", value="acme")
    target_type = st.selectbox("Target type", options=["brand", "domain"])
    max_variants = st.slider("Generated candidates", min_value=6, max_value=30, value=12)
    offline_mode = st.toggle("Offline demo mode", value=True)
    run = st.button("Analyze", type="primary", use_container_width=True)
    st.caption("Offline mode uses explicitly marked mock fixtures to keep the demo reproducible.")


def priority_class(priority: str) -> str:
    if priority == "high":
        return "high"
    if priority == "medium":
        return "medium"
    return "low"


def render_finding(asset: dict[str, object]) -> None:
    infra = asset["infrastructure"]
    origin = infra["origin"]
    badge_class = priority_class(asset["priority"])
    source_class = "live" if origin == "live" else "mock"
    st.markdown(
        f"""
        <div class="finding">
          <h4 class="mono">{asset["domain"]}</h4>
          <div>
            <span class="badge {badge_class}">{asset["priority"].upper()} · {asset["score"]}/100</span>
            <span class="badge">{asset["technique"]}</span>
            <span class="badge {source_class}">{origin.upper()}</span>
          </div>
          <p class="muted">{asset["score_rationale"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns([1.1, 1, 1])
    with cols[0]:
        st.markdown("**Signals**")
        for signal in asset["risk_signals"]:
            evidence = ", ".join(signal["evidence"]) if signal["evidence"] else "No inline evidence"
            st.write(f"`{signal['code']}` (+{signal['weight']}): {signal['reason']}")
            st.caption(evidence)
    with cols[1]:
        st.markdown("**Infrastructure**")
        st.write(f"IP: {', '.join(infra['ip_addresses']) or 'none'}")
        st.write(f"Registrar: {infra['registrar'] or 'unknown'}")
        st.write(f"Registrant: {infra['rdap_org'] or 'unknown'}")
        st.write(f"ASN: {infra['asn'] or 'unknown'} {infra['asn_org'] or ''}")
    with cols[2]:
        st.markdown("**CT Observations**")
        if asset["certificate_observations"]:
            for observation in asset["certificate_observations"]:
                st.write(f"{observation['issuer_name']} | {observation['common_name']}")
                st.caption(f"{observation['source']} · {observation['origin']}")
        else:
            st.write("No certificate observation")


if run:
    payload = {
        "target": target,
        "target_type": target_type,
        "offline_mode": offline_mode,
        "max_variants": max_variants,
    }
    with st.spinner("Collecting evidence and ranking candidate infrastructure..."):
        try:
            response = httpx.post(API_URL, json=payload, timeout=45.0)
            response.raise_for_status()
            result = response.json()
        except httpx.HTTPError as exc:
            st.error(f"API request failed: {exc}")
        else:
            summary = result["summary"]
            metadata = result["metadata"]
            ranked_assets = result["assets"]

            st.markdown(
                f"""
                <div class="panel">
                  <div class="eyebrow">Current Assessment</div>
                  <h3>{summary["headline"]}</h3>
                  <p class="muted">{summary["executive_summary"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            metrics = st.columns(5)
            metrics[0].metric("Candidates", metadata["generated_variants"])
            metrics[1].metric("Ranked Findings", metadata["scored_assets"])
            metrics[2].metric("High Priority", sum(1 for asset in ranked_assets if asset["priority"] == "high"))
            metrics[3].metric("Live Findings", metadata["live_assets"])
            metrics[4].metric("Mock Findings", metadata["mock_assets"])

            overview_tab, findings_tab, narrative_tab, exports_tab = st.tabs(
                ["Overview", "Findings", "Narrative", "Exports"]
            )

            with overview_tab:
                left, right = st.columns([1.3, 1])
                with left:
                    st.markdown("#### Recruiter Story")
                    st.write(
                        "This run demonstrates an analyst workflow: generate likely lookalikes, correlate them "
                        "with CT activity, enrich infrastructure, apply rule-based scoring, and summarize the result "
                        "without letting the model mutate the score."
                    )
                    st.markdown("#### Grounding")
                    for note in summary["grounding_notes"]:
                        st.write(f"- {note}")
                with right:
                    st.markdown("#### Target Context")
                    st.json(result["target_profile"])

            with findings_tab:
                if not ranked_assets:
                    st.info("No domains crossed the current scoring threshold.")
                for asset in ranked_assets:
                    render_finding(asset)

            with narrative_tab:
                st.markdown("#### Analyst Notes")
                for note in summary["analyst_notes"]:
                    st.write(f"- {note}")
                st.markdown("#### Recommended Actions")
                for action in summary["recommended_actions"]:
                    st.write(f"- {action}")
                st.caption(f"Summary source: {summary['model_source']}")

            with exports_tab:
                st.download_button(
                    "Download Markdown Report",
                    data=result["report_markdown"],
                    file_name=f"phantomscope-{result['analysis_id']}.md",
                    use_container_width=True,
                )
                st.download_button(
                    "Download JSON Report",
                    data=json.dumps(result, indent=2),
                    file_name=f"phantomscope-{result['analysis_id']}.json",
                    use_container_width=True,
                )
                st.markdown("#### Raw JSON")
                st.json(result)
