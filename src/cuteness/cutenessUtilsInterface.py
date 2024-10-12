from abc import ABC, abstractmethod

from .cutenessHistoryResult import CutenessHistoryResult
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessLeaderboardHistoryResult import CutenessLeaderboardHistoryResult


class CutenessUtilsInterface(ABC):

    @abstractmethod
    def getCutenessHistory(self, result: CutenessHistoryResult, delimiter: str) -> str:
        pass

    @abstractmethod
    def getCutenessLeaderboardHistory(
        self,
        result: CutenessLeaderboardHistoryResult,
        entryDelimiter: str,
        leaderboardDelimiter: str
    ) -> str:
        pass

    @abstractmethod
    def getLeaderboard(self, entries: list[CutenessLeaderboardEntry], delimiter: str) -> str:
        pass
