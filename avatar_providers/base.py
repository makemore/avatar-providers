"""
Abstract base for avatar providers.

Framework-agnostic — no Django, Flask, or Firebase imports.
Each provider accepts its config via constructor args.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionResult:
    """Provider-agnostic session response."""

    provider: str  # "heygen" or "tavus"
    session_id: str
    session_token: str  # auth token for the frontend SDK / embed
    metadata: dict[str, Any] = field(default_factory=dict)


class AvatarProvider(abc.ABC):
    """Interface every avatar provider must implement."""

    name: str  # e.g. "heygen", "tavus"

    @abc.abstractmethod
    def create_session(self) -> SessionResult:
        """Create a new avatar session and return credentials."""
        ...

