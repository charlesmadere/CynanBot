from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchBannedUser import TwitchBannedUser
from .twitchPaginationResponse import TwitchPaginationResponse


# This class intends to directly correspond to Twitch's "Get Banned Users" API:
# https://dev.twitch.tv/docs/api/reference/#get-banned-users
@dataclass(frozen = True, slots = True)
class TwitchBannedUsersResponse:
    data: FrozenList[TwitchBannedUser]
    pagination: TwitchPaginationResponse | None
