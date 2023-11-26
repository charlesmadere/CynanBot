from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.cuteness.cutenessChampionsResult import CutenessChampionsResult
from CynanBot.cuteness.cutenessHistoryResult import CutenessHistoryResult
from CynanBot.cuteness.cutenessLeaderboardHistoryResult import \
    CutenessLeaderboardHistoryResult
from CynanBot.cuteness.cutenessLeaderboardResult import \
    CutenessLeaderboardResult
from CynanBot.cuteness.cutenessResult import CutenessResult


class CutenessRepositoryInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        twitchChannel: str,
        userId: str,
        userName: str,
    ) -> CutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessChampions(self, twitchChannel: str) -> CutenessChampionsResult:
        pass

    @abstractmethod
    async def fetchCutenessHistory(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> CutenessHistoryResult:
        pass

    @abstractmethod
    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> CutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboard(
        self,
        twitchChannel: str,
        specificLookupUserId: Optional[str] = None,
        specificLookupUserName: Optional[str] = None
    ) -> CutenessLeaderboardResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboardHistory(self, twitchChannel: str) -> CutenessLeaderboardHistoryResult:
        pass
