from dataclasses import dataclass

from .absGashaponResult import AbsGashaponResult


@dataclass(frozen = True, slots = True)
class NotFollowingGashaponResult(AbsGashaponResult):
    chatterUserId: str
    twitchChannelId: str
