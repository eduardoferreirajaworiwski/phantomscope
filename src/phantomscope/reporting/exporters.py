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
        "",
        "## Executive Summary",
        "",
        result.summary.executive_summary,
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
                f"- Signals: {', '.join(signal.code for signal in asset.risk_signals) or 'none'}",
                "",
            ]
        )

    lines.extend(
        [
            "## Recommended Actions",
            "",
            *[f"- {action}" for action in result.summary.recommended_actions],
            "",
        ]
    )
    return "\n".join(lines)


def build_json_report(result: AnalysisResult) -> str:
    return json.dumps(result.model_dump(mode="json"), indent=2)

