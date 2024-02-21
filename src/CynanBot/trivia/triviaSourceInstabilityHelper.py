from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.questions.triviaSource import TriviaSource


class TriviaSourceInstabilityHelper():

    def __init__(
        self,
        timber: TimberInterface,
        fallOffTimeDelta: timedelta = timedelta(minutes = 20),
        timeZone: timezone = timezone.utc
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(fallOffTimeDelta, timedelta), f"malformed {fallOffTimeDelta=}"
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__timber: TimberInterface = timber
        self.__fallOffTimeDelta: timedelta = fallOffTimeDelta
        self.__timeZone: timezone = timeZone

        self.__times: Dict[TriviaSource, Optional[datetime]] = dict()
        self.__values: Dict[TriviaSource, int] = defaultdict(lambda: 0)

    def __getitem__(self, key: TriviaSource) -> int:
        assert isinstance(key, TriviaSource), f"malformed {key=}"

        now = datetime.now(self.__timeZone)
        lastErrorTime = self.__times.get(key, None)

        if lastErrorTime is not None and now - lastErrorTime <= self.__fallOffTimeDelta:
            return self.__values[key]

        self.__values[key] = 0
        return 0

    def incrementErrorCount(self, key: TriviaSource) -> int:
        assert isinstance(key, TriviaSource), f"malformed {key=}"

        now = datetime.now(self.__timeZone)
        lastErrorTime = self.__times.get(key, None)
        self.__times[key] = now
        newErrorCount: int = 0

        if lastErrorTime is not None and now - lastErrorTime <= self.__fallOffTimeDelta:
            newErrorCount = self.__values[key] + 1
            self.__values[key] = newErrorCount
        else:
            newErrorCount = 1
            self.__values[key] = newErrorCount

        self.__timber.log('TriviaSourceInstabilityHelper', f'Incremented error count for {key} to {newErrorCount}')
        return newErrorCount
