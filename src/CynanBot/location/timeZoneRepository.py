from datetime import tzinfo
from typing import Dict, List

import pytz

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface


# A listing of pytz timezones can be found here:
# https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
class TimeZoneRepository(TimeZoneRepositoryInterface):

    def __init__(self):
        self.__timeZones: Dict[str, tzinfo] = dict()

    def getTimeZone(self, timeZoneStr: str) -> tzinfo:
        if not utils.isValidStr(timeZoneStr):
            raise ValueError(f'timeZoneStr argument is malformed: \"{timeZoneStr}\"')

        if timeZoneStr in self.__timeZones:
            return self.__timeZones[timeZoneStr]

        newTimeZone: tzinfo = pytz.timezone(timeZoneStr)
        self.__timeZones[timeZoneStr] = newTimeZone
        return newTimeZone

    def getTimeZones(self, timeZoneStrs: List[str]) -> List[tzinfo]:
        if not utils.hasItems(timeZoneStrs):
            raise ValueError(f'timeZoneStrs argument is malformed: \"{timeZoneStrs}\"')

        timeZones: List[tzinfo] = list()

        for timeZoneStr in timeZoneStrs:
            if not utils.isValidStr(timeZoneStr):
                raise ValueError(f'malformed timeZoneStr \"{timeZoneStr}\" within given timeZoneStrs: \"{timeZoneStrs}\"')

            newTimeZone = self.getTimeZone(timeZoneStr)
            timeZones.append(newTimeZone)

        return timeZones
