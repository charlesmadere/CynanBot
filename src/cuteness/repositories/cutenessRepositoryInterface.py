from abc import ABC, abstractmethod

from ..models.cutenessChampionsResult import CutenessChampionsResult
from ..models.cutenessHistoryResult import CutenessHistoryResult
from ..models.cutenessLeaderboardHistoryResult import CutenessLeaderboardHistoryResult
from ..models.cutenessLeaderboardResult import CutenessLeaderboardResult
from ..models.cutenessResult import CutenessResult
from ..models.incrementedCutenessResult import IncrementedCutenessResult


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

    @abstractmethod
    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> IncrementedCutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboard(
        self,
        twitchChannelId: str,
        specificLookupUserId: str | None = None,
    ) -> CutenessLeaderboardResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboardHistory(
        self,
        twitchChannelId: str,
    ) -> CutenessLeaderboardHistoryResult:
        pass
