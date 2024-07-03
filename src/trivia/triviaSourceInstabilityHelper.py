from collections import defaultdict
from datetime import datetime, timedelta

from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..timber.timberInterface import TimberInterface
from .questions.triviaSource import TriviaSource


class TriviaSourceInstabilityHelper():

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        fallOffTimeDelta: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(fallOffTimeDelta, timedelta):
            raise TypeError(f'fallOffTimeDelta argument is malformed: \"{fallOffTimeDelta}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__fallOffTimeDelta: timedelta = fallOffTimeDelta

        self.__times: dict[TriviaSource, datetime | None] = dict()
        self.__values: dict[TriviaSource, int] = defaultdict(lambda: 0)

    def __getitem__(self, key: TriviaSource) -> int:
        if not isinstance(key, TriviaSource):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        lastErrorTime = self.__times.get(key, None)

        if lastErrorTime is not None and now - lastErrorTime <= self.__fallOffTimeDelta:
            return self.__values[key]

        self.__values[key] = 0
        return 0

    def incrementErrorCount(self, key: TriviaSource) -> int:
        if not isinstance(key, TriviaSource):
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

        self.__timber.log('TriviaSourceInstabilityHelper', f'Incremented error count ({key=}) ({newErrorCount=})')
        return newErrorCount
