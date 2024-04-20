from abc import ABC, abstractmethod
from datetime import tzinfo
from typing import List


# A listing of pytz timezones can be found here:
# https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
class TimeZoneRepositoryInterface(ABC):

    @abstractmethod
    def getTimeZone(self, timeZoneStr: str) -> tzinfo:
        pass

    @abstractmethod
    def getTimeZones(self, timeZoneStrs: List[str]) -> List[tzinfo]:
        pass
