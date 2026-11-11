from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozendict import frozendict

from ..models.chatterInventoryData import ChatterInventoryData
from ..models.gashaponTier import GashaponTier
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
        gashaponsRewarded: frozendict[GashaponTier, int]
        hypeEmote: str

    @abstractmethod
    async def invoke(
        self,
        action: RequestWatchStreakRewardAction,
        twitchAccessToken: str,
    ) -> AbsResult:
        pass
