from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchModeratorUser import TwitchModeratorUser
from .twitchPaginationResponse import TwitchPaginationResponse


# This class intends to directly correspond to Twitch's "Get Moderators" API:
# https://dev.twitch.tv/docs/api/reference/#get-moderators
@dataclass(frozen = True)
class TwitchModeratorsResponse:
    data: FrozenList[TwitchModeratorUser]
    pagination: TwitchPaginationResponse | None
