from datetime import datetime, timedelta, timezone, tzinfo
from typing import Dict, Generic, Optional, TypeVar

import CynanBot.misc.utils as utils

T = TypeVar('T')

class TimedDict(Generic[T]):

    def __init__(
        self,
        cacheTimeToLive: timedelta,
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(cacheTimeToLive, timedelta):
            raise TypeError(f'cacheTimeToLive argument is malformed: \"{cacheTimeToLive}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__cacheTimeToLive: timedelta = cacheTimeToLive
        self.__timeZone: tzinfo = timeZone

        self.__times: Dict[str, Optional[datetime]] = dict()
        self.__values: Dict[str, Optional[T]] = dict()

    def clear(self):
        self.__times.clear()
        self.__values.clear()

    def __delitem__(self, key: str):
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        self.__times.pop(key, None)
        self.__values.pop(key, None)

    def __getitem__(self, key: str) -> Optional[T]:
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        cachedTime = self.__times.get(key, None)
        cachedValue = self.__values.get(key, None)

        if cachedTime is None:
            return None

        nowDateTime = datetime.now(self.__timeZone)

        if nowDateTime > cachedTime:
            return None

        return cachedValue

    def isReady(self, key: str) -> bool:
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        return self[key] is None

    def isReadyAndUpdate(self, key: str) -> bool:
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        if self.isReady(key):
            self.update(key)
            return True
        else:
            return False

    def __setitem__(self, key: str, value: Optional[T]):
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        self.__times[key] = datetime.now(self.__timeZone) + self.__cacheTimeToLive
        self.__values[key] = value

    def update(self, key: str):
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        self.__times[key] = datetime.now(self.__timeZone) + self.__cacheTimeToLive
