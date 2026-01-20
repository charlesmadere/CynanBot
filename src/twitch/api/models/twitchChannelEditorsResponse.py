from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchChannelEditor import TwitchChannelEditor


# This class intends to directly correspond to Twitch's "Get Channel Editors" API:
# https://dev.twitch.tv/docs/api/reference#get-channel-editors
@dataclass(frozen = True, slots = True)
class TwitchChannelEditorsResponse:
    editors: FrozenList[TwitchChannelEditor]
