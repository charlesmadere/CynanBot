from abc import ABC, abstractmethod

from .mostRecentRecurringAction import MostRecentRecurringAction
from .recurringAction import RecurringAction


class MostRecentRecurringActionRepositoryInterface(ABC):

    @abstractmethod
    async def getMostRecentRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> MostRecentRecurringAction | None:
        pass

    @abstractmethod
    async def setMostRecentRecurringAction(self, action: RecurringAction):
        pass
