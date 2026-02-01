from abc import ABC, abstractmethod

from .cutenessChampionsResult import CutenessChampionsResult
from .cutenessHistoryResult import CutenessHistoryResult
from .cutenessLeaderboardHistoryResult import CutenessLeaderboardHistoryResult
from .cutenessLeaderboardResult import CutenessLeaderboardResult
from .cutenessResult import CutenessResult
from .incrementedCutenessResult import IncrementedCutenessResult


class CutenessRepositoryInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ) -> CutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessChampions(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> CutenessChampionsResult:
        pass

    @abstractmethod
    async def fetchCutenessHistory(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ) -> CutenessHistoryResult:
        pass

    @abstractmethod
    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ) -> IncrementedCutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        specificLookupUserId: str | None = None,
        specificLookupUserName: str | None = None,
    ) -> CutenessLeaderboardResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboardHistory(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> CutenessLeaderboardHistoryResult:
        pass
