from abc import ABC, abstractmethod

from ..models.gashaponResults.absGashaponResult import AbsGashaponResult


class GashaponRewardHelperInterface(ABC):

    @abstractmethod
    async def checkAndGiveRewardIfAvailable(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AbsGashaponResult:
        pass
