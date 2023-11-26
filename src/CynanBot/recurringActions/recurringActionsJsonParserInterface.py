from abc import ABC, abstractmethod
from typing import Optional

from recurringActions.recurringAction import RecurringAction
from recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from recurringActions.weatherRecurringAction import WeatherRecurringAction
from recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction


class RecurringActionsJsonParserInterface(ABC):

    @abstractmethod
    async def parseSuperTrivia(
        self,
        enabled: bool,
        minutesBetween: Optional[int],
        jsonString: Optional[str],
        twitchChannel: str
    ) -> Optional[SuperTriviaRecurringAction]:
        pass

    @abstractmethod
    async def parseWeather(
        self,
        enabled: bool,
        minutesBetween: Optional[int],
        jsonString: Optional[str],
        twitchChannel: str
    ) -> Optional[WeatherRecurringAction]:
        pass

    @abstractmethod
    async def parseWordOfTheDay(
        self,
        enabled: bool,
        minutesBetween: Optional[int],
        jsonString: Optional[str],
        twitchChannel: str
    ) -> Optional[WordOfTheDayRecurringAction]:
        pass

    @abstractmethod
    async def toJson(self, action: RecurringAction) -> str:
        pass
