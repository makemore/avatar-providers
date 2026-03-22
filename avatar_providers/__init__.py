"""
avatar_providers — framework-agnostic avatar session management.

Supports LiveAvatar and Tavus CVI. No Django, Flask, or Firebase
dependencies — just pure Python + requests.

Usage:

    from avatar_providers import LiveAvatarProvider, TavusProvider

    # LiveAvatar
    provider = LiveAvatarProvider(api_key="...", avatar_id="...")
    result = provider.create_session()

    # Tavus
    provider = TavusProvider(api_key="...", persona_id="...", replica_id="...")
    result = provider.create_session()

    # result.provider   → "liveavatar" or "tavus"
    # result.session_id → provider's session/conversation ID
    # result.session_token → auth token for the frontend SDK
    # result.metadata   → provider-specific extras (e.g. conversation_url)
"""

from .base import AvatarProvider, SessionResult  # noqa: F401
from .liveavatar import LiveAvatarProvider  # noqa: F401
from .tavus import TavusProvider  # noqa: F401

__all__ = [
    "AvatarProvider",
    "SessionResult",
    "LiveAvatarProvider",
    "TavusProvider",
]

