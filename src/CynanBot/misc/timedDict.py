from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import misc.utils as utils


class TimedDict():

    def __init__(
        self,
        timeDelta: timedelta,
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(timeDelta, timedelta):
            raise ValueError(f'timeDelta argument is malformed: \"{timeDelta}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__timeDelta: timedelta = timeDelta
        self.__timeZone: timezone = timeZone
        self.__times: Dict[str, Optional[Any]] = dict()
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

        if key not in self.__times or key not in self.__values:
            return None

        nowDateTime = datetime.now(self.__timeZone)

        if nowDateTime > self.__times[key]:
            return None

        return self.__values[key]

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

        self.__times[key] = datetime.now(self.__timeZone) + self.__timeDelta
        self.__values[key] = value

    def update(self, key: str):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        self.__times[key] = datetime.now(self.__timeZone) + self.__timeDelta
        self.__values[key] = self.__times[key]
