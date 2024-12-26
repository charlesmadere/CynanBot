from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchChannelEditor import TwitchChannelEditor


@dataclass(frozen = True)
class TwitchChannelEditorsResponse:
    editors: FrozenList[TwitchChannelEditor]
