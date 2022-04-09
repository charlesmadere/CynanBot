from cuteness.cutenessDate import CutenessDate
from cuteness.cutenessEntry import CutenessEntry


class CutenessHistoryEntry(CutenessEntry):

    def __init__(
        self,
        cutenessDate: CutenessDate,
        cuteness: int,
        userId: str,
        userName: str
    ):
        super().__init__(cuteness, userId, userName)

        if cutenessDate is None:
            raise ValueError(f'cutenessDate argument is malformed: \"{cutenessDate}\"')

        self.__cutenessDate: CutenessDate = cutenessDate

    def getCutenessDate(self) -> CutenessDate:
        return self.__cutenessDate
