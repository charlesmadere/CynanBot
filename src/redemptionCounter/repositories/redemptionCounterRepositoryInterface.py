from abc import ABC, abstractmethod

from ..models.redemptionCount import RedemptionCount
from ...misc.clearable import Clearable


class RedemptionCounterRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str,
    ) -> RedemptionCount:
        pass

    @abstractmethod
    async def increment(
        self,
        incrementAmount: int,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str,
    ) -> RedemptionCount:
        pass
