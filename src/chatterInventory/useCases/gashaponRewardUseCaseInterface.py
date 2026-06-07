from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from ..models.chatterInventoryData import ChatterInventoryData
from ..models.requestGashaponRewardAction import RequestGashaponRewardAction


class GashaponRewardUseCaseInterface(ABC):

    class AbsResult(ABC):
        pass

    @dataclass(frozen = True, slots = True)
    class ItemNotEnabledResult(AbsResult):
        pass

    @dataclass(frozen = True, slots = True)
    class NotFollowingResult(AbsResult):
        pass

    @dataclass(frozen = True, slots = True)
    class NotReadyResult(AbsResult):
        nextGashaponAvailability: datetime

    @dataclass(frozen = True, slots = True)
    class NotSubscribedResult(AbsResult):
        pass

    @dataclass(frozen = True, slots = True)
    class RewardedResult(AbsResult):
        chatterInventory: ChatterInventoryData
        hypeEmote: str

    @abstractmethod
    async def invoke(
        self,
        action: RequestGashaponRewardAction,
        twitchAccessToken: str,
    ) -> AbsResult:
        pass
