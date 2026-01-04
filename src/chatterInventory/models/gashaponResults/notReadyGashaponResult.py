from dataclasses import dataclass
from datetime import datetime

from .absGashaponResult import AbsGashaponResult


@dataclass(frozen = True)
class NotReadyGashaponResult(AbsGashaponResult):
    mostRecentGashapon: datetime
    chatterUserId: str
    twitchChannelId: str
