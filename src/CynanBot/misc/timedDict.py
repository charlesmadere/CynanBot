from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils


class TimedDict():

    def __init__(
        self,
        cacheTimeToLive: timedelta,
        timeZone: tzinfo = timezone.utc
    ):
        assert isinstance(cacheTimeToLive, timedelta), f"malformed {cacheTimeToLive=}"
        assert isinstance(timeZone, tzinfo), f"malformed {timeZone=}"

        self.__cacheTimeToLive: timedelta = cacheTimeToLive
        self.__timeZone: tzinfo = timeZone

        self.__times: Dict[str, Optional[datetime]] = dict()
        self.__values: Dict[str, Optional[Any]] = dict()

    def clear(self):
        self.__times.clear()
        self.__values.clear()

    def __delitem__(self, key: str):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        self.__times.pop(key, None)
        self.__values.pop(key, None)

    def __getitem__(self, key: str) -> Optional[Any]:
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        cachedTime = self.__times.get(key, None)
        cachedValue = self.__values.get(key, None)

        if cachedTime is None or cachedValue is None:
            return None

        nowDateTime = datetime.now(self.__timeZone)

        if nowDateTime > cachedTime:
            return None

        return cachedValue

    def isReady(self, key: str) -> bool:
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        return self[key] is None

    def isReadyAndUpdate(self, key: str) -> bool:
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        if self.isReady(key):
            self.update(key)
            return True
        else:
            return False

    def __setitem__(self, key: str, value):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        self.__times[key] = datetime.now(self.__timeZone) + self.__cacheTimeToLive
        self.__values[key] = value

    def update(self, key: str):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        newCachedTime = datetime.now(self.__timeZone) + self.__cacheTimeToLive
        self.__times[key] = newCachedTime
        self.__values[key] = newCachedTime
