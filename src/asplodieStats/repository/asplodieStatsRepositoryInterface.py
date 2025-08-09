from abc import ABC, abstractmethod

from ..models.asplodieStats import AsplodieStats
from ...misc.clearable import Clearable


class AsplodieStatsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def addAsplodie(
        self,
        isSelfAsplodie: bool,
        durationAsplodiedSeconds: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AsplodieStats:
        pass

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AsplodieStats:
        pass
