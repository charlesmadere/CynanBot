from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchFollower import TwitchFollower
from .twitchPaginationResponse import TwitchPaginationResponse


@dataclass(frozen = True)
class TwitchFollowersResponse:
    followers: FrozenList[TwitchFollower]
    total: int
    pagination: TwitchPaginationResponse | None
