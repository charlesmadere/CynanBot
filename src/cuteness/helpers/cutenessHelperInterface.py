from abc import ABC, abstractmethod

from ..models.preparedCutenessChampionsResult import PreparedCutenessChampionsResult
from ..models.preparedCutenessLeaderboardHistoryResult import PreparedCutenessLeaderboardHistoryResult
from ..models.preparedCutenessLeaderboardResult import PreparedCutenessLeaderboardResult
from ..models.preparedCutenessResult import PreparedCutenessResult
from ..models.preparedIncrementedCutenessResult import PreparedIncrementedCutenessResult


class CutenessHelperInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedCutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessChampions(
        self,
        twitchChannelId: str,
    ) -> PreparedCutenessChampionsResult:
        pass

    @abstractmethod
    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedIncrementedCutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboard(
        self,
        twitchChannelId: str,
        specificLookupUserId: str | None = None,
    ) -> PreparedCutenessLeaderboardResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboardHistory(
        self,
        twitchChannelId: str,
    ) -> PreparedCutenessLeaderboardHistoryResult:
        pass
