from abc import ABC, abstractmethod

from ..models.gashaponRewardHistory import GashaponRewardHistory
from ...misc.clearable import Clearable


class GashaponRewardHistoryRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getHistory(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> GashaponRewardHistory | None:
        pass

    @abstractmethod
    async def noteRewardGiven(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        pass
