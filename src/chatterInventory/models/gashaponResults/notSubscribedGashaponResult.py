from dataclasses import dataclass

from .absGashaponResult import AbsGashaponResult


@dataclass(frozen = True, slots = True)
class NotSubscribedGashaponResult(AbsGashaponResult):
    chatterUserId: str
    twitchChannelId: str
