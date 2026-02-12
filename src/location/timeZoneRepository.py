from datetime import datetime, timezone, tzinfo
from typing import Collection, Final

import pytz
from frozenlist import FrozenList

from .timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils


# A listing of pytz timezones can be found here:
# https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
class TimeZoneRepository(TimeZoneRepositoryInterface):

    def __init__(
        self,
        defaultTimeZone: tzinfo = timezone.utc,
    ):
        if not isinstance(defaultTimeZone, tzinfo):
            raise TypeError(f'defaultTimeZone argument is malformed: \"{defaultTimeZone}\"')

        self.__defaultTimeZone: Final[tzinfo] = defaultTimeZone
        self.__timeZones: Final[dict[str, tzinfo]] = dict()

    def getDefault(self) -> tzinfo:
        return self.__defaultTimeZone

    def getNow(self) -> datetime:
        timeZone = self.getDefault()
        return datetime.now(timeZone)

    def getTimeZone(self, timeZoneStr: str) -> tzinfo:
        if not utils.isValidStr(timeZoneStr):
            raise TypeError(f'timeZoneStr argument is malformed: \"{timeZoneStr}\"')

        if timeZoneStr in self.__timeZones:
            return self.__timeZones[timeZoneStr]

        newTimeZone: tzinfo = pytz.timezone(timeZoneStr)
        self.__timeZones[timeZoneStr] = newTimeZone
        return newTimeZone

    def getTimeZones(self, timeZoneStrs: Collection[str]) -> FrozenList[tzinfo]:
        if not isinstance(timeZoneStrs, Collection):
            raise TypeError(f'timeZoneStrs argument is malformed: \"{timeZoneStrs}\"')

        timeZones: FrozenList[tzinfo] = FrozenList()

        for timeZoneStr in timeZoneStrs:
            if not utils.isValidStr(timeZoneStr):
                raise ValueError(f'malformed timeZoneStr \"{timeZoneStr}\" within given timeZoneStrs: \"{timeZoneStrs}\"')

            newTimeZone = self.getTimeZone(timeZoneStr)
            timeZones.append(newTimeZone)

        timeZones.freeze()
        return timeZones
