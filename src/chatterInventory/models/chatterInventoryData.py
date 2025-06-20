from dataclasses import dataclass

from frozendict import frozendict

from .chatterItemType import ChatterItemType


@dataclass(frozen = True)
class ChatterInventoryData:
    inventory: frozendict[ChatterItemType, int]
    chatterUserId: str
    twitchChannelId: str
