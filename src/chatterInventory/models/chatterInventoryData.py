from dataclasses import dataclass

from frozendict import frozendict

from .chatterItemType import ChatterItemType


@dataclass(frozen = True)
class ChatterInventoryData:
    inventory: frozendict[ChatterItemType, int]
    chatterUserId: str
    twitchChannelId: str

    def __getitem__(self, key: ChatterItemType) -> int:
        if not isinstance(key, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{key}\"')

        return self.inventory.get(key, 0)
