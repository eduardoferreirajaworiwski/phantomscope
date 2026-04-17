from __future__ import annotations

import logging
from datetime import UTC, datetime

from phantomscope.core.config import Settings
from phantomscope.models.schemas import CertificateObservation, DataOrigin
from phantomscope.providers.http import HttpProvider
from phantomscope.providers.mock_data import mock_certificate_observations

logger = logging.getLogger(__name__)


class CrtShProvider:
    def __init__(self, settings: Settings, offline_mode: bool) -> None:
        self.settings = settings
        self.offline_mode = offline_mode
        self.http = HttpProvider(settings)

    async def fetch(self, domain: str) -> list[CertificateObservation]:
        if self.offline_mode:
            return mock_certificate_observations(domain)

        try:
            raw = await self.http.get_json(self.settings.crtsh_base_url, params={"q": domain, "output": "json"})
        except Exception as exc:
            logger.warning("ct_lookup_failed", extra={"event": "ct_lookup_failed", "domain": domain, "error": str(exc)})
            return mock_certificate_observations(domain)

        observations: list[CertificateObservation] = []
        if not isinstance(raw, list):
            return observations

        for item in raw[:5]:
            entry_ts = item.get("entry_timestamp")
            try:
                logged_at = datetime.fromisoformat(entry_ts.replace(" ", "T")).astimezone(UTC) if entry_ts else datetime.now(UTC)
            except ValueError:
                logged_at = datetime.now(UTC)
            observations.append(
                CertificateObservation(
                    logged_at=logged_at,
                    issuer_name=item.get("issuer_name", "unknown"),
                    common_name=item.get("common_name", domain),
                    matching_identities=str(item.get("name_value", domain)).split("\n"),
                    source="crt.sh",
                    origin=DataOrigin.LIVE,
                )
            )
        return observations
