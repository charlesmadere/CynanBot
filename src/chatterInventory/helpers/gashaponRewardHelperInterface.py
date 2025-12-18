from abc import ABC, abstractmethod

from ..models.giveGashaponRewardResult import GiveGashaponRewardResult


class GashaponRewardHelperInterface(ABC):

    @abstractmethod
    async def checkAndGiveRewardIfAvailable(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> GiveGashaponRewardResult:
        pass
