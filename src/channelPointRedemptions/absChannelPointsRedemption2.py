from abc import ABC, abstractmethod

from .pointsRedemptionResult import PointsRedemptionResult
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class AbsChannelPointRedemption2(ABC):

    @property
    @abstractmethod
    def pointsRedemptionName(self) -> str:
        pass

    @abstractmethod
    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        pass

    @abstractmethod
    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        pass
