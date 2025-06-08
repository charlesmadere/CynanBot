from abc import ABC, abstractmethod

from ..models.preparedRedemptionCount import PreparedRedemptionCount


class RedemptionCounterHelperInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str
    ) -> PreparedRedemptionCount:
        pass

    @abstractmethod
    async def increment(
        self,
        incrementAmount: int,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str
    ) -> PreparedRedemptionCount:
        pass
