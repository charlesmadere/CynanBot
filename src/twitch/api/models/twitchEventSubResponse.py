from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchEventSubDetails import TwitchEventSubDetails


@dataclass(frozen = True)
class TwitchEventSubResponse:
    data: FrozenList[TwitchEventSubDetails]
    maxTotalCost: int
    total: int
    totalCost: int
