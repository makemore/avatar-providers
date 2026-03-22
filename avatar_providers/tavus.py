"""
Tavus CVI provider.

Creates conversations via the Tavus REST API. The frontend either
embeds the conversation_url in an iframe or uses the Daily.co SDK.

No framework dependencies — config is passed via constructor.
"""

from __future__ import annotations

import logging

import requests

from .base import AvatarProvider, SessionResult

logger = logging.getLogger(__name__)

TAVUS_API_URL = "https://tavusapi.com"


class TavusProvider(AvatarProvider):
    name = "tavus"

    def __init__(self, api_key: str, persona_id: str = "", replica_id: str = ""):
        if not api_key:
            raise ValueError("TavusProvider requires an api_key")
        self.api_key = api_key
        self.persona_id = persona_id
        self.replica_id = replica_id

    def create_session(self) -> SessionResult:
        payload: dict = {}
        if self.persona_id:
            payload["persona_id"] = self.persona_id
        if self.replica_id:
            payload["replica_id"] = self.replica_id

        resp = requests.post(
            f"{TAVUS_API_URL}/v2/conversations",
            headers={
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=15,
        )

        if not resp.ok:
            logger.error(
                "Tavus conversation request failed: %s %s — %s",
                resp.status_code,
                resp.reason,
                resp.text,
            )
            raise RuntimeError(
                f"Tavus API error ({resp.status_code}): {resp.text}"
            )

        data = resp.json()

        return SessionResult(
            provider="tavus",
            session_id=data.get("conversation_id", ""),
            session_token=data.get("meeting_token", ""),
            metadata={
                "conversation_url": data.get("conversation_url", ""),
            },
        )

