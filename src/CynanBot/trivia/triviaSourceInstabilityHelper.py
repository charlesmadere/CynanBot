from collections import defaultdict
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Dict, Optional

from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.questions.triviaSource import TriviaSource


class TriviaSourceInstabilityHelper():

    def __init__(
        self,
        timber: TimberInterface,
        fallOffTimeDelta: timedelta = timedelta(minutes = 20),
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(fallOffTimeDelta, timedelta):
            raise TypeError(f'fallOffTimeDelta argument is malformed: \"{fallOffTimeDelta}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__timber: TimberInterface = timber
        self.__fallOffTimeDelta: timedelta = fallOffTimeDelta
        self.__timeZone: tzinfo = timeZone

        self.__times: Dict[TriviaSource, Optional[datetime]] = dict()
        self.__values: Dict[TriviaSource, int] = defaultdict(lambda: 0)

    def __getitem__(self, key: TriviaSource) -> int:
        if not isinstance(key, TriviaSource):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        now = datetime.now(self.__timeZone)
        lastErrorTime = self.__times.get(key, None)

        if lastErrorTime is not None and now - lastErrorTime <= self.__fallOffTimeDelta:
            return self.__values[key]

        self.__values[key] = 0
        return 0

    def incrementErrorCount(self, key: TriviaSource) -> int:
        if not isinstance(key, TriviaSource):
            raise TypeError(f'key argument is malformed: \"{key}\"')

        now = datetime.now(self.__timeZone)
        lastErrorTime = self.__times.get(key, None)
        self.__times[key] = now
        newErrorCount = 0

        if lastErrorTime is not None and now - lastErrorTime <= self.__fallOffTimeDelta:
            newErrorCount = self.__values[key] + 1
            self.__values[key] = newErrorCount
        else:
            newErrorCount = 1
            self.__values[key] = newErrorCount

        self.__timber.log('TriviaSourceInstabilityHelper', f'Incremented error count for {key} to {newErrorCount}')
        return newErrorCount
