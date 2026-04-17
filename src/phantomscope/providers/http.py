from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable

import httpx

from phantomscope.core.config import Settings


class HttpProvider:
    def __init__(self, settings: Settings) -> None:
        self._timeout = settings.http_timeout
        self._retries = settings.http_retries
        self._headers = {"User-Agent": settings.user_agent}

    async def get_json(self, url: str, params: dict[str, str] | None = None) -> list | dict:
        last_error: Exception | None = None
        for attempt in range(self._retries + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=self._timeout,
                    headers=self._headers,
                ) as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    return response.json()
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                await asyncio.sleep(0.2 * (attempt + 1))
        if last_error:
            raise last_error
        return {}

    async def post_json(
        self,
        url: str,
        json_body: dict[str, object],
        headers: dict[str, str] | None = None,
    ) -> dict[str, object]:
        request_headers = dict(self._headers)
        if headers:
            request_headers.update(headers)

        last_error: Exception | None = None
        for attempt in range(self._retries + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=self._timeout,
                    headers=request_headers,
                ) as client:
                    response = await client.post(url, json=json_body)
                    response.raise_for_status()
                    payload = response.json()
                    if not isinstance(payload, dict):
                        raise ValueError("expected dict response")
                    return payload
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                await asyncio.sleep(0.2 * (attempt + 1))
        if last_error:
            raise last_error
        return {}

    async def best_effort(self, func: Callable[[], Awaitable[dict | list]]) -> dict | list:
        try:
            return await func()
        except Exception:
            return {}
