from dataclasses import dataclass

from frozendict import frozendict

from .absGashaponResult import AbsGashaponResult
from ..chatterInventoryData import ChatterInventoryData
from ..chatterItemType import ChatterItemType


@dataclass(frozen = True)
class GashaponRewardedGashaponResult(AbsGashaponResult):
    chatterInventory: ChatterInventoryData
    chatterUserId: str
    hypeEmote: str
    twitchChannelId: str

    @property
    def inventory(self) -> frozendict[ChatterItemType, int]:
        return self.chatterInventory.inventory
