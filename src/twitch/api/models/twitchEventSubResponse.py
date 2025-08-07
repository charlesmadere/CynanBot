from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchEventSubDetails import TwitchEventSubDetails
from .twitchPaginationResponse import TwitchPaginationResponse


@dataclass(frozen = True)
class TwitchEventSubResponse:
    data: FrozenList[TwitchEventSubDetails]
    maxTotalCost: int
    total: int
    totalCost: int
    pagination: TwitchPaginationResponse | None
