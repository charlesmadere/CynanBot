from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchGame import TwitchGame


@dataclass(frozen = True, slots = True)
class TwitchGamesResponse:
    data: FrozenList[TwitchGame]
