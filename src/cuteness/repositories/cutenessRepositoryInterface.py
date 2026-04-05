from abc import ABC, abstractmethod

from ..models.cutenessChampionsResult import CutenessChampionsResult
from ..models.cutenessHistoryResult import CutenessHistoryResult
from ..models.cutenessResult import CutenessResult


class CutenessRepositoryInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> CutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessChampions(
        self,
        twitchChannelId: str,
    ) -> CutenessChampionsResult:
        pass

    @abstractmethod
    async def fetchCutenessHistory(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> CutenessHistoryResult:
        pass
