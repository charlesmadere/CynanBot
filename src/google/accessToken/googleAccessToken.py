from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class GoogleAccessToken:
    expireTime: datetime
    accessToken: str
