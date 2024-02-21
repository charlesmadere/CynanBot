from CynanBot.cuteness.cutenessDate import CutenessDate
from CynanBot.cuteness.cutenessEntry import CutenessEntry


class CutenessHistoryEntry(CutenessEntry):

    def __init__(
        self,
        cutenessDate: CutenessDate,
        cuteness: int,
        userId: str,
        userName: str
    ):
        super().__init__(
            cuteness = cuteness,
            userId = userId,
            userName = userName
        )

        assert isinstance(cutenessDate, CutenessDate), f"malformed {cutenessDate=}"

        self.__cutenessDate: CutenessDate = cutenessDate

    def getCutenessDate(self) -> CutenessDate:
        return self.__cutenessDate
