from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class AnivCopyMessageTimeoutScore():
    mostRecentDodge: datetime | None
    mostRecentTimeout: datetime | None
    dodgeScore: int
    timeoutScore: int
    chatterUserId: str
    chatterUserName: str
    twitchChannel: str
    twitchChannelId: str
