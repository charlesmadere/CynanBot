import locale
from typing import Final

from .cutenessEntry import CutenessEntry
from ..misc import utils as utils


class CutenessLeaderboardEntry(CutenessEntry):

    def __init__(
        self,
        cuteness: int,
        rank: int,
        userId: str,
        userName: str,
    ):
        super().__init__(
            cuteness = cuteness,
            userId = userId,
            userName = userName,
        )

        if not utils.isValidInt(rank):
            raise TypeError(f'rank argument is malformed: \"{rank}\"')
        elif rank < 1 or rank > utils.getIntMaxSafeSize():
            raise ValueError(f'rank argument is out of bounds: {rank}')

        self.__rank: Final[int] = rank

    @property
    def rank(self) -> int:
        return self.__rank

    @property
    def rankStr(self) -> str:
        return locale.format_string("%d", self.__rank, grouping = True)
