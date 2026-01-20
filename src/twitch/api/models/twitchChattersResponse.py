from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchChatter import TwitchChatter
from .twitchPaginationResponse import TwitchPaginationResponse


@dataclass(frozen = True, slots = True)
class TwitchChattersResponse:
    data: FrozenList[TwitchChatter]
    total: int
    pagination: TwitchPaginationResponse | None
