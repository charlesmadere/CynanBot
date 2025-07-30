from dataclasses import dataclass

from frozendict import frozendict

from .chatterInventoryData import ChatterInventoryData
from .chatterItemType import ChatterItemType


@dataclass(frozen = True)
class PreparedChatterInventoryData:
    chatterInventory: ChatterInventoryData
    chatterUserName: str
    twitchChannel: str

    @property
    def chatterUserId(self) -> str:
        return self.chatterInventory.chatterUserId

    def __getitem__(self, key: ChatterItemType) -> int:
        if not isinstance(key, ChatterItemType):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        return self.chatterInventory[key]

    @property
    def inventory(self) -> frozendict[ChatterItemType, int]:
        return self.chatterInventory.inventory

    @property
    def twitchChannelId(self) -> str:
        return self.chatterInventory.twitchChannelId
