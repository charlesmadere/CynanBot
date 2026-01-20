from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchBanResponseEntry import TwitchBanResponseEntry


# This class intends to directly correspond to Twitch's "Ban User" API:
# https://dev.twitch.tv/docs/api/reference/#ban-user
@dataclass(frozen = True, slots = True)
class TwitchBanResponse:
    data: FrozenList[TwitchBanResponseEntry]
