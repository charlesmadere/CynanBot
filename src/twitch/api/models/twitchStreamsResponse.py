from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchPaginationResponse import TwitchPaginationResponse
from .twitchStream import TwitchStream


@dataclass(frozen = True, slots = True)
class TwitchStreamsResponse:
    data: FrozenList[TwitchStream]
    pagination: TwitchPaginationResponse | None
