from dataclasses import dataclass
from datetime import datetime

from .twitchApiScope import TwitchApiScope


@dataclass(frozen = True)
class TwitchValidationResponse:
    expiresAt: datetime
    scopes: frozenset[TwitchApiScope]
    expiresInSeconds: int
    clientId: str
    login: str
    userId: str
