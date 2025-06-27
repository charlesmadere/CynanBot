from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchConduitResponseEntry import TwitchConduitResponseEntry


# This class intends to directly correspond to Twitch's "Create a conduit" API:
# https://dev.twitch.tv/docs/eventsub/handling-conduit-events/#creating-a-conduit
@dataclass(frozen = True)
class TwitchConduitResponse:
    data: FrozenList[TwitchConduitResponseEntry]
