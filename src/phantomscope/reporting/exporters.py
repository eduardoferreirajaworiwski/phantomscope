from __future__ import annotations

import json

from phantomscope.models.schemas import AnalysisResult


def build_markdown_report(result: AnalysisResult) -> str:
    lines = [
        f"# PhantomScope Report: {result.target_profile.normalized_target}",
        "",
        f"- Analysis ID: `{result.analysis_id}`",
        f"- Created At: `{result.created_at.isoformat()}`",
        f"- Assets Reviewed: `{len(result.assets)}`",
        f"- Offline Mode: `{result.metadata.get('offline_mode', False)}`",
        f"- Summary Source: `{result.summary.model_source}`",
        "",
        "## Executive Summary",
        "",
        result.summary.executive_summary,
        "",
        "## Grounding Notes",
        "",
        *[f"- {note}" for note in result.summary.grounding_notes],
        "",
        "## Priority Findings",
        "",
    ]

    if not result.assets:
        lines.append("No suspicious assets were produced in this run.")

    for asset in result.assets:
        lines.extend(
            [
                f"### {asset.domain}",
                f"- Technique: `{asset.technique}`",
                f"- Score: `{asset.score}`",
                f"- Priority: `{asset.priority}`",
                f"- Scoring rationale: `{asset.score_rationale}`",
                f"- Evidence sources: {', '.join(asset.evidence_sources) or 'none'}",
                f"- Infrastructure origin: `{asset.infrastructure.origin.value}`",
                f"- Signals: {', '.join(signal.code for signal in asset.risk_signals) or 'none'}",
                "",
                "#### Signal Breakdown",
                "",
            ]
        )
        lines.extend(
            [
                f"- `{signal.code}` (+{signal.weight}): {signal.reason}"
                for signal in asset.risk_signals
            ]
        )
        lines.append("")

    lines.extend(
        [
            "## Analyst Notes",
            "",
            *[f"- {note}" for note in result.summary.analyst_notes],
            "",
            "## Recommended Actions",
            "",
            *[f"- {action}" for action in result.summary.recommended_actions],
            "",
        ]
    )
    return "\n".join(lines)


def build_json_report(result: AnalysisResult) -> str:
    return json.dumps(result.model_dump(mode="json"), indent=2)
