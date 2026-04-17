from __future__ import annotations

import json

import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000/api/v1/analyses"

st.set_page_config(page_title="PhantomScope", layout="wide")
st.title("PhantomScope")
st.caption("Threat intelligence triage for phishing infrastructure, typosquatting, and brand impersonation.")

with st.sidebar:
    st.subheader("Analysis Input")
    target = st.text_input("Target brand or domain", value="acme")
    target_type = st.selectbox("Target type", options=["brand", "domain"])
    max_variants = st.slider("Max generated variants", min_value=5, max_value=25, value=10)
    offline_mode = st.toggle("Offline demo mode", value=True)
    run = st.button("Run Analysis", type="primary")

if run:
    payload = {
        "target": target,
        "target_type": target_type,
        "offline_mode": offline_mode,
        "max_variants": max_variants,
    }
    with st.spinner("Running analysis..."):
        try:
            response = httpx.post(API_URL, json=payload, timeout=30.0)
            response.raise_for_status()
            result = response.json()
        except httpx.HTTPError as exc:
            st.error(f"API request failed: {exc}")
        else:
            st.success(f"Analysis complete: {result['analysis_id']}")

            summary = result["summary"]
            st.subheader(summary["headline"])
            st.write(summary["executive_summary"])

            metrics = st.columns(3)
            metrics[0].metric("Assets", len(result["assets"]))
            metrics[1].metric(
                "High Priority",
                sum(1 for asset in result["assets"] if asset["priority"] == "high"),
            )
            metrics[2].metric("Offline Mode", str(result["metadata"]["offline_mode"]))

            st.subheader("Ranked Findings")
            for asset in result["assets"]:
                with st.expander(f"{asset['domain']} | {asset['score']}/100 | {asset['priority']}"):
                    st.write(f"Technique: `{asset['technique']}`")
                    st.write("Signals:")
                    for signal in asset["risk_signals"]:
                        st.write(f"- `{signal['code']}`: {signal['reason']}")
                    st.write("Infrastructure:")
                    st.json(asset["infrastructure"])

            st.subheader("Analyst Notes")
            for note in summary["analyst_notes"]:
                st.write(f"- {note}")

            st.subheader("Export")
            st.download_button(
                "Download Markdown Report",
                data=result["report_markdown"],
                file_name=f"phantomscope-{result['analysis_id']}.md",
            )
            st.download_button(
                "Download JSON Report",
                data=json.dumps(result, indent=2),
                file_name=f"phantomscope-{result['analysis_id']}.json",
            )
