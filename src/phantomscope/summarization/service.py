from __future__ import annotations

from phantomscope.models.schemas import AnalystSummary, ScoredAsset, TargetProfile


class AnalystSummaryService:
    def build_summary(self, target: TargetProfile, assets: list[ScoredAsset]) -> AnalystSummary:
        ranked = sorted(assets, key=lambda item: item.score, reverse=True)
        high = [item for item in ranked if item.priority == "high"]
        medium = [item for item in ranked if item.priority == "medium"]

        headline = (
            f"{len(high)} high-priority suspicious domains identified for {target.normalized_target}"
            if high
            else f"No high-priority domains identified for {target.normalized_target}"
        )

        executive_summary = (
            f"PhantomScope analyzed {len(assets)} generated assets related to {target.normalized_target}. "
            f"{len(high)} were classified as high priority and {len(medium)} as medium priority based on "
            "lookalike techniques, certificate activity, registration privacy, infrastructure resolution, "
            "and reputation hints. AI assistance is used only to accelerate analyst triage; all scoring remains rule-based."
        )

        analyst_notes = [
            f"{asset.domain} scored {asset.score}/100 with signals: {', '.join(signal.code for signal in asset.risk_signals)}."
            for asset in ranked[:3]
        ] or ["No suspicious assets were generated for review."]

        recommended_actions = [
            "Validate whether high-priority domains are externally reachable and host brand-abuse content.",
            "Escalate confirmed phishing lures to takedown or registrar-abuse workflows.",
            "Track repeated hosting and registrar patterns for clustering in future iterations.",
        ]
        grounding_notes = [
            "This legacy summarizer is deterministic and preserved for compatibility.",
            "AI-assisted narrative generation lives under phantomscope.ai.",
            "Risk score generation remains rule-based and separate from summarization.",
        ]

        return AnalystSummary(
            headline=headline,
            executive_summary=executive_summary,
            analyst_notes=analyst_notes,
            recommended_actions=recommended_actions,
            grounding_notes=grounding_notes,
            model_source="deterministic-analyst-narrative",
        )
