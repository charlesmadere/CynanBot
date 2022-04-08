from cuteness.cutenessDate import CutenessDate
from cuteness.cutenessEntry import CutenessEntry


class CutenessHistoryEntry():

    def __init__(self, cutenessDate: CutenessDate, cutenessEntry: CutenessEntry):
        if cutenessDate is None:
            raise ValueError(f'cutenessDate argument is malformed: \"{cutenessDate}\"')
        elif cutenessEntry is None:
            raise ValueError(f'cutenessResult argument is malformed: \"{cutenessEntry}\"')

        self.__cutenessDate: CutenessDate = cutenessDate
        self.__cutenessEntry: CutenessEntry = cutenessEntry

    def getCutenessDate(self) -> CutenessDate:
        return self.__cutenessDate

    def getCutenessEntry(self) -> CutenessEntry:
        return self.__cutenessEntry
