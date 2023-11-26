from abc import ABC, abstractmethod
from typing import List, Optional

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
        twitchChannel: str
    ) -> List[RecurringAction]:
        pass

    @abstractmethod
    async def getSuperTriviaRecurringAction(
        self,
        twitchChannel: str
    ) -> Optional[SuperTriviaRecurringAction]:
        pass

    @abstractmethod
    async def getWeatherRecurringAction(
        self,
        twitchChannel: str
    ) -> Optional[WeatherRecurringAction]:
        pass

    @abstractmethod
    async def getWordOfTheDayRecurringAction(
        self,
        twitchChannel: str
    ) -> Optional[WordOfTheDayRecurringAction]:
        pass

    @abstractmethod
    async def setRecurringAction(self, action: RecurringAction):
        pass
