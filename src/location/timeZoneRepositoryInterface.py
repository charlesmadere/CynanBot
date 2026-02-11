from abc import ABC, abstractmethod
from datetime import datetime, tzinfo
from typing import Collection

from frozenlist import FrozenList


# A listing of pytz timezones can be found here:
# https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
class TimeZoneRepositoryInterface(ABC):

    @abstractmethod
    def getDefault(self) -> tzinfo:
        pass

    @abstractmethod
    def getNow(self) -> datetime:
        pass

    @abstractmethod
    def getTimeZone(self, timeZoneStr: str) -> tzinfo:
        pass

    @abstractmethod
    def getTimeZones(self, timeZoneStrs: Collection[str]) -> FrozenList[tzinfo]:
        pass
