from dataclasses import dataclass
from datetime import datetime

from .absGashaponResult import AbsGashaponResult


@dataclass(frozen = True, slots = True)
class NotReadyGashaponResult(AbsGashaponResult):
    mostRecentGashapon: datetime
    nextGashaponAvailability: datetime
    daysBetweenGashaponRewards: int
    chatterUserId: str
    twitchChannelId: str
