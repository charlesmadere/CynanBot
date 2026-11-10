from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozendict import frozendict

from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemType import ChatterItemType
from ..models.requestWatchStreakRewardAction import RequestWatchStreakRewardAction


class RequestWatchStreakRewardUseCaseInterface(ABC):

    class AbsResult(ABC):
        pass

    @dataclass(frozen = True, slots = True)
    class NoRewardResult(AbsResult):
        pass

    @dataclass(frozen = True, slots = True)
    class NotEnabledResult(AbsResult):
        pass

    @dataclass(frozen = True, slots = True)
    class RewardedResult(AbsResult):
        chatterInventory: ChatterInventoryData
        rewardedItems: frozendict[ChatterItemType, int]
        hypeEmote: str

    @abstractmethod
    async def invoke(
        self,
        action: RequestWatchStreakRewardAction,
    ) -> AbsResult:
        pass
