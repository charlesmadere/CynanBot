from abc import ABC, abstractmethod

from .recurringAction import RecurringAction
from .superTriviaRecurringAction import SuperTriviaRecurringAction
from .weatherRecurringAction import WeatherRecurringAction
from .wordOfTheDayRecurringAction import WordOfTheDayRecurringAction


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
