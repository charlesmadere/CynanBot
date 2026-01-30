from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class GoogleAccessToken:
    expireTime: datetime
    expiresInSeconds: int
    accessToken: str
