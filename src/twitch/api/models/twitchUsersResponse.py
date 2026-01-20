from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchUser import TwitchUser


# This class intends to directly correspond to Twitch's "Get Users" API:
# https://dev.twitch.tv/docs/api/reference#get-users
@dataclass(frozen = True, slots = True)
class TwitchUsersResponse:
    data: FrozenList[TwitchUser]
