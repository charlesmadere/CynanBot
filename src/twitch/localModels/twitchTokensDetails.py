from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class TwitchTokensDetails:
    expirationTime: datetime
    accessToken: str
    refreshToken: str
