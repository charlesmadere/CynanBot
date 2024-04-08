from abc import ABC, abstractmethod

from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from CynanBot.recurringActions.weatherRecurringAction import \
    WeatherRecurringAction
from CynanBot.recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction


class RecurringActionsRepositoryInterface(ABC):

    @abstractmethod
    async def getAllRecurringActions(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> list[RecurringAction]:
        pass

    @abstractmethod
    async def getSuperTriviaRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> SuperTriviaRecurringAction | None:
        pass

    @abstractmethod
    async def getWeatherRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WeatherRecurringAction | None:
        pass

    @abstractmethod
    async def getWordOfTheDayRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WordOfTheDayRecurringAction | None:
        pass

    @abstractmethod
    async def setRecurringAction(self, action: RecurringAction):
        pass
