from abc import ABC, abstractmethod

from .cutenessHistoryResult import CutenessHistoryResult
from .cutenessLeaderboardHistoryResult import CutenessLeaderboardHistoryResult


class CutenessUtilsInterface(ABC):

    @abstractmethod
    def getCutenessHistory(
        self,
        result: CutenessHistoryResult,
        chatterUserName: str,
        delimiter: str = ', ',
    ) -> str:
        pass

    @abstractmethod
    async def getCutenessLeaderboardHistory(
        self,
        result: CutenessLeaderboardHistoryResult,
        entryDelimiter: str = ', ',
        leaderboardDelimiter: str = ' — ',
    ) -> str:
        pass
