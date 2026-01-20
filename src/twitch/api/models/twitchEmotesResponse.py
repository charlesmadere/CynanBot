from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchEmoteDetails import TwitchEmoteDetails


@dataclass(frozen = True, slots = True)
class TwitchEmotesResponse:
    emoteData: FrozenList[TwitchEmoteDetails]
    template: str
