from typing import Final

from .cutenessDate import CutenessDate
from .cutenessEntry import CutenessEntry


class CutenessHistoryEntry(CutenessEntry):

    def __init__(
        self,
        cutenessDate: CutenessDate,
        cuteness: int,
        userId: str,
        userName: str,
    ):
        super().__init__(
            cuteness = cuteness,
            userId = userId,
            userName = userName,
        )

        if not isinstance(cutenessDate, CutenessDate):
            raise TypeError(f'cutenessDate argument is malformed: \"{cutenessDate}\"')

        self.__cutenessDate: Final[CutenessDate] = cutenessDate

    @property
    def cutenessDate(self) -> CutenessDate:
        return self.__cutenessDate
