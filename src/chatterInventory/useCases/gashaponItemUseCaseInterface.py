from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozendict import frozendict

from ..models.chatterItemType import ChatterItemType
from ..models.gashaponTier import GashaponTier
from ..models.useChatterItemAction import UseChatterItemAction


class GashaponItemUseCaseInterface(ABC):

    class AbsResult:
        pass

    @dataclass(frozen = True, slots = True)
    class GashaponDisabledResult(AbsResult):
        pass

    @dataclass(frozen = True, slots = True)
    class ItemsReceivedResult(AbsResult):
        awardedItems: frozendict[ChatterItemType, int]
        gashaponTier: GashaponTier

    @dataclass(frozen = True, slots = True)
    class NoItemsReceivedResult(AbsResult):
        pass

    @abstractmethod
    async def invoke(
        self,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> AbsResult:
        pass
