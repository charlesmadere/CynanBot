from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchFollower import TwitchFollower
from .twitchPaginationResponse import TwitchPaginationResponse


# This class intends to directly correspond to Twitch's "Get Channel Followers" API:
# https://dev.twitch.tv/docs/api/reference#get-channel-followers
@dataclass(frozen = True, slots = True)
class TwitchFollowersResponse:
    data: FrozenList[TwitchFollower]
    total: int
    pagination: TwitchPaginationResponse | None
