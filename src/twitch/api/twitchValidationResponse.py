from dataclasses import dataclass
from datetime import datetime

from .twitchApiScope import TwitchApiScope


@dataclass(frozen = True)
class TwitchValidationResponse():
    expiresAt: datetime
    expiresInSeconds: int
    scopes: set[TwitchApiScope]
    clientId: str
    login: str
    userId: str
