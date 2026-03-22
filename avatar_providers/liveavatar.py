"""
LiveAvatar provider.

Creates sessions via the LiveAvatar REST API. The frontend then uses
the @heygen/liveavatar-web-sdk to connect via LiveKit.

No framework dependencies — config is passed via constructor.
"""

from __future__ import annotations

import logging

import requests

from .base import AvatarProvider, SessionResult

logger = logging.getLogger(__name__)

LIVEAVATAR_API_URL = "https://api.liveavatar.com"


class LiveAvatarProvider(AvatarProvider):
    name = "liveavatar"

    def __init__(self, api_key: str, avatar_id: str = ""):
        if not api_key:
            raise ValueError("LiveAvatarProvider requires an api_key")
        self.api_key = api_key
        self.avatar_id = avatar_id

    def create_session(self) -> SessionResult:
        payload: dict = {
            "mode": "FULL",
            "avatar_persona": {"language": "en"},
        }
        if self.avatar_id:
            payload["avatar_id"] = self.avatar_id

        resp = requests.post(
            f"{LIVEAVATAR_API_URL}/v1/sessions/token",
            headers={
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
            timeout=15,
        )

        if not resp.ok:
            logger.error(
                "LiveAvatar token request failed: %s %s — %s",
                resp.status_code,
                resp.reason,
                resp.text,
            )
            raise RuntimeError(
                f"LiveAvatar API error ({resp.status_code}): {resp.text}"
            )

        resp_json = resp.json()
        data = resp_json.get("data", resp_json)

        return SessionResult(
            provider="liveavatar",
            session_id=data.get("session_id", ""),
            session_token=data.get("session_token", ""),
        )

