from collections import defaultdict
from datetime import datetime, timedelta
from typing import Final

from .twitchWebsocketInstabilityHelperInterface import TwitchWebsocketInstabilityHelperInterface
from ..twitchWebsocketUser import TwitchWebsocketUser
from ....location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ....timber.timberInterface import TimberInterface


class TwitchWebsocketInstabilityHelper(TwitchWebsocketInstabilityHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        fallOffTimeDelta: timedelta = timedelta(minutes = 3),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(fallOffTimeDelta, timedelta):
            raise TypeError(f'fallOffTimeDelta argument is malformed: \"{fallOffTimeDelta}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__fallOffTimeDelta: Final[timedelta] = fallOffTimeDelta

        self.__times: Final[dict[TwitchWebsocketUser, datetime | None]] = dict()
        self.__values: Final[dict[TwitchWebsocketUser, int]] = defaultdict(lambda: 0)

    def __getitem__(self, key: TwitchWebsocketUser) -> int:
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        lastErrorTime = self.__times.get(key, None)

        if lastErrorTime is not None and now - lastErrorTime <= self.__fallOffTimeDelta:
            return self.__values[key]

        self.__values[key] = 0
        return 0

    def incrementErrorCount(self, key: TwitchWebsocketUser) -> int:
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        lastErrorTime = self.__times.get(key, None)
        self.__times[key] = now
        newErrorCount = 0

        if lastErrorTime is not None and now - lastErrorTime <= self.__fallOffTimeDelta:
            newErrorCount = self.__values[key] + 1
            self.__values[key] = newErrorCount
        else:
            newErrorCount = 1
            self.__values[key] = newErrorCount

        self.__timber.log('TwitchWebsocketInstabilityHelper', f'Incremented error count ({key=}) ({newErrorCount=})')
        return newErrorCount

    def resetToDefault(self, key: TwitchWebsocketUser):
        if not isinstance(key, TwitchWebsocketUser):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        oldErrorCount = self[key]
        self.__times.pop(key, None)
        self.__values[key] = 0
        self.__timber.log('TwitchWebsocketInstabilityHelper', f'Reset error count ({key=}) ({oldErrorCount=})')
