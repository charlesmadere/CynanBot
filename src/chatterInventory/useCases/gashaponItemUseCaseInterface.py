from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozendict import frozendict

from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemType import ChatterItemType
from ..models.gashaponTier import GashaponTier
from ..models.useChatterItemAction import UseChatterItemAction


class GashaponItemUseCaseInterface(ABC):

    class AbsResult:
        pass

    @dataclass(frozen = True, slots = True)
    class GashaponItemDisabledResult(AbsResult):
        pass

    @dataclass(frozen = True, slots = True)
    class ItemsReceivedResult(AbsResult):
        updatedInventory: ChatterInventoryData
        awardedItems: frozendict[ChatterItemType, int]
        gashaponTier: GashaponTier
        hypeEmote: str

    @dataclass(frozen = True, slots = True)
    class NoItemsReceivedResult(AbsResult):
        ripBozoEmote: str

    @abstractmethod
    async def invoke(
        self,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> AbsResult:
        pass
