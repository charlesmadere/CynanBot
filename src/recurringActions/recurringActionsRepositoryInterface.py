from abc import ABC, abstractmethod

from frozenlist import FrozenList

from .actions.cutenessRecurringAction import CutenessRecurringAction
from .actions.recurringAction import RecurringAction
from .actions.superTriviaRecurringAction import SuperTriviaRecurringAction
from .actions.weatherRecurringAction import WeatherRecurringAction
from .actions.wordOfTheDayRecurringAction import WordOfTheDayRecurringAction


class RecurringActionsRepositoryInterface(ABC):

    @abstractmethod
    async def getAllRecurringActions(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> FrozenList[RecurringAction]:
        pass

    @abstractmethod
    async def getCutenessRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> CutenessRecurringAction | None:
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
