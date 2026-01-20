from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchStartCommercialDetails import TwitchStartCommercialDetails


@dataclass(frozen = True, slots = True)
class TwitchStartCommercialResponse:
    data: FrozenList[TwitchStartCommercialDetails]
