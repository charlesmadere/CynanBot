from datetime import datetime
from typing import Any, Optional

from CynanBot.misc.simpleDateTime import SimpleDateTime


class CutenessDate():

    def __init__(self, utcYearAndMonthStr: Optional[str] = None):
        if utcYearAndMonthStr is None:
            self.__simpleDateTime: SimpleDateTime = SimpleDateTime()
        else:
            self.__simpleDateTime: SimpleDateTime = SimpleDateTime(
                now = datetime.strptime(utcYearAndMonthStr, '%Y-%m')
            )

        self.__str: str = self.__simpleDateTime.getDateTime().strftime('%Y-%m')

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, CutenessDate):
            return self.__simpleDateTime >= other.__simpleDateTime
        else:
            return False

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, CutenessDate):
            return self.__simpleDateTime > other.__simpleDateTime
        else:
            return False

    def __le__(self, other: Any) -> bool:
        if isinstance(other, CutenessDate):
            return self.__simpleDateTime <= other.__simpleDateTime
        else:
            return False

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CutenessDate):
            return self.__simpleDateTime < other.__simpleDateTime
        else:
            return False

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__simpleDateTime

    def getStr(self) -> str:
        return self.__str

    def toStr(self) -> str:
        return self.__simpleDateTime.getDateTime().strftime('%b %Y')
