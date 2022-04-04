from datetime import datetime, timezone
from typing import Optional


class CutenessDate():

    def __init__(
        self,
        utcYearAndMonthStr: Optional[str] = None
    ):
        if utcYearAndMonthStr is None:
            now = datetime.now(timezone.utc)
            self.__str: str = now.strftime('%Y-%m')
            self.__datetime: datetime = now
        else:
            self.__str: str = utcYearAndMonthStr
            self.__datetime: datetime = datetime.strptime(utcYearAndMonthStr, '%Y-%m')

    def getDateTime(self) -> datetime:
        return self.__datetime

    def getStr(self) -> str:
        return self.__str

    def toStr(self) -> str:
        return self.__datetime.strftime('%b %Y')
