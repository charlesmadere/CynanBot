from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any

from . import utils as utils


class SimpleDateTime:

    def __init__(
        self,
        now: datetime | None = None,
        timeZone: tzinfo = timezone.utc,
    ):
        if now is not None and not isinstance(now, datetime):
            raise TypeError(f'now argument is malformed: \"{now}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        if now is None:
            self.__now: datetime = datetime.now(timeZone)
        else:
            self.__now: datetime = now

    def __add__(self, other: Any):
        if isinstance(other, timedelta):
            return SimpleDateTime(self.__now + other)
        else:
            raise TypeError(f'`other` is an unsupported type: \"{other}\"')

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SimpleDateTime):
            return self.__now == other.__now
        elif isinstance(other, datetime):
            return self.__now == other
        else:
            return False

    def getDateTime(self) -> datetime:
        return self.__now

    def getDateAndTimeStr(self, includeMillis: bool = False) -> str:
        if not utils.isValidBool(includeMillis):
            raise TypeError(f'includeMillis argument is malformed: \"{includeMillis}\"')

        return f'{self.getYearMonthDayStr()} {self.getTimeStr(includeMillis)}'

    def getDayInt(self) -> int:
        return self.__now.day

    def getDayStr(self) -> str:
        return self.__now.strftime('%d')

    def getHourInt(self) -> int:
        return self.__now.hour

    def getHourStr(self) -> str:
        return self.__now.strftime('%H')

    def getIsoFormatStr(self) -> str:
        return self.__now.isoformat()

    def getMillisStr(self) -> str:
        return self.__now.strftime('%f')[:-3]

    def getMinuteInt(self) -> int:
        return self.__now.minute

    def getMinuteStr(self) -> str:
        return self.__now.strftime('%M')

    def getMonthStr(self) -> str:
        return self.__now.strftime('%m')

    def getMonthInt(self) -> int:
        return self.__now.month

    def getSecondInt(self) -> int:
        return self.__now.second

    def getSecondStr(self) -> str:
        return self.__now.strftime('%S')

    def getTimeStr(self, includeMillis: bool = False) -> str:
        if not utils.isValidBool(includeMillis):
            raise TypeError(f'includeMillis argument is malformed: \"{includeMillis}\"')

        timeStr = f'{self.getHourStr()}:{self.getMinuteStr()}:{self.getSecondStr()}'

        if includeMillis:
            timeStr = f'{timeStr}.{self.getMillisStr()}'

        return timeStr

    def getYearInt(self) -> int:
        return self.__now.year

    def getYearStr(self) -> str:
        return self.__now.strftime('%Y')

    def getYearMonthDayStr(self) -> str:
        return f'{self.getYearStr()}/{self.getMonthStr()}/{self.getDayStr()}'

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, SimpleDateTime):
            return self.__now >= other.__now
        elif isinstance(other, datetime):
            return self.__now >= other
        else:
            raise TypeError(f'`other` is an unsupported type: \"{other}\"')

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, SimpleDateTime):
            return self.__now > other.__now
        elif isinstance(other, datetime):
            return self.__now > other
        else:
            raise TypeError(f'`other` is an unsupported type: \"{other}\"')

    def __le__(self, other: Any) -> bool:
        if isinstance(other, SimpleDateTime):
            return self.__now <= other.__now
        elif isinstance(other, datetime):
            return self.__now <= other
        else:
            raise TypeError(f'`other` is an unsupported type: \"{other}\"')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, SimpleDateTime):
            return self.__now < other.__now
        elif isinstance(other, datetime):
            return self.__now < other
        else:
            raise TypeError(f'`other` is an unsupported type: \"{other}\"')

    def __repr__(self) -> str:
        return str(self.__now)

    def __sub__(self, other: Any):
        if isinstance(other, timedelta):
            return SimpleDateTime(self.__now - other)
        else:
            raise TypeError(f'`other` is an unsupported type: \"{other}\"')
