from datetime import timezone, tzinfo

import pytz

from .timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils


# A listing of pytz timezones can be found here:
# https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
class TimeZoneRepository(TimeZoneRepositoryInterface):

    def __init__(self, defaultTimeZone: tzinfo = timezone.utc):
        if not isinstance(defaultTimeZone, tzinfo):
            raise TypeError(f'defaultTimeZone argument is malformed: \"{defaultTimeZone}\"')

        self.__defaultTimeZone: tzinfo = defaultTimeZone
        self.__timeZones: dict[str, tzinfo] = dict()

    def getDefault(self) -> tzinfo:
        return self.__defaultTimeZone

    def getTimeZone(self, timeZoneStr: str) -> tzinfo:
        if not utils.isValidStr(timeZoneStr):
            raise TypeError(f'timeZoneStr argument is malformed: \"{timeZoneStr}\"')

        if timeZoneStr in self.__timeZones:
            return self.__timeZones[timeZoneStr]

        newTimeZone: tzinfo = pytz.timezone(timeZoneStr)
        self.__timeZones[timeZoneStr] = newTimeZone
        return newTimeZone

    def getTimeZones(self, timeZoneStrs: list[str]) -> list[tzinfo]:
        if not isinstance(timeZoneStrs, list):
            raise TypeError(f'timeZoneStrs argument is malformed: \"{timeZoneStrs}\"')

        timeZones: list[tzinfo] = list()

        for timeZoneStr in timeZoneStrs:
            if not utils.isValidStr(timeZoneStr):
                raise ValueError(f'malformed timeZoneStr \"{timeZoneStr}\" within given timeZoneStrs: \"{timeZoneStrs}\"')

            newTimeZone = self.getTimeZone(timeZoneStr)
            timeZones.append(newTimeZone)

        return timeZones
