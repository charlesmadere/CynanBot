from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class GashaponRewardHistory:
    mostRecentReward: datetime
    chatterUserId: str
    twitchChannelId: str
