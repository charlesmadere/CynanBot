from dataclasses import dataclass

from frozendict import frozendict

from .absGashaponResult import AbsGashaponResult
from ..chatterInventoryData import ChatterInventoryData
from ..chatterItemType import ChatterItemType


@dataclass(frozen = True)
class GashaponRewardedGashaponResult(AbsGashaponResult):
    chatterInventory: ChatterInventoryData
    chatterUserId: str
    twitchChannelId: str

    def __getitem__(self, key: ChatterItemType) -> int:
        if not isinstance(key, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{key}\"')

        return self.chatterInventory[key]

    @property
    def inventory(self) -> frozendict[ChatterItemType, int]:
        return self.chatterInventory.inventory
