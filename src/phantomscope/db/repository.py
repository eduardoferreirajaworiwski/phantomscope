from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from phantomscope.models.schemas import AnalysisResult


class AnalysisRepository:
    def __init__(self, database_url: str) -> None:
        self.path = _resolve_sqlite_path(database_url)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS analysis_runs (
                    analysis_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    target TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def save(self, result: AnalysisResult) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO analysis_runs (analysis_id, created_at, target, payload_json)
                VALUES (?, ?, ?, ?)
                """,
                (
                    result.analysis_id,
                    result.created_at.isoformat(),
                    result.target_profile.normalized_target,
                    json.dumps(result.model_dump(mode="json")),
                ),
            )
            connection.commit()

    def get(self, analysis_id: str) -> AnalysisResult | None:
        with sqlite3.connect(self.path) as connection:
            row = connection.execute(
                "SELECT payload_json FROM analysis_runs WHERE analysis_id = ?",
                (analysis_id,),
            ).fetchone()
        if not row:
            return None
        return AnalysisResult.model_validate_json(row[0])


def _resolve_sqlite_path(database_url: str) -> Path:
    if database_url.startswith("sqlite:///"):
        return Path(database_url.replace("sqlite:///", "", 1)).resolve()
    raise ValueError("Only sqlite URLs are supported in the MVP.")

