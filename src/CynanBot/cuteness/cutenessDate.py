from datetime import datetime
from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class CutenessDate():

    def __init__(self, utcYearAndMonthStr: Optional[str] = None):
        if utils.isValidStr(utcYearAndMonthStr):
            self.__simpleDateTime: SimpleDateTime = SimpleDateTime(
                now = datetime.strptime(utcYearAndMonthStr, '%Y-%m')
            )
        else:
            self.__simpleDateTime: SimpleDateTime = SimpleDateTime()

        self.__databaseString: str = self.__simpleDateTime.getDateTime().strftime('%Y-%m')
        self.__humanString: str = self.__simpleDateTime.getDateTime().strftime('%b %Y')

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, CutenessDate):
            return self.__simpleDateTime >= other.__simpleDateTime
        else:
            return False

    def getDatabaseString(self) -> str:
        return self.__databaseString

    def getHumanString(self) -> str:
        return self.__humanString

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__simpleDateTime

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

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'databaseString': self.__databaseString,
            'humanString': self.__humanString
        }
