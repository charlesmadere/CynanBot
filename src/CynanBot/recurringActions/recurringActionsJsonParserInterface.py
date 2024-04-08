from abc import ABC, abstractmethod

from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from CynanBot.recurringActions.weatherRecurringAction import \
    WeatherRecurringAction
from CynanBot.recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction


class RecurringActionsJsonParserInterface(ABC):

    @abstractmethod
    async def parseSuperTrivia(
        self,
        enabled: bool,
        minutesBetween: int | None,
        jsonString: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> SuperTriviaRecurringAction | None:
        pass

    @abstractmethod
    async def parseWeather(
        self,
        enabled: bool,
        minutesBetween: int | None,
        jsonString: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WeatherRecurringAction | None:
        pass

    @abstractmethod
    async def parseWordOfTheDay(
        self,
        enabled: bool,
        minutesBetween: int | None,
        jsonString: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WordOfTheDayRecurringAction | None:
        pass

    @abstractmethod
    async def toJson(self, action: RecurringAction) -> str:
        pass
