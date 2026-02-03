from abc import ABC, abstractmethod

from .actions.recurringAction import RecurringAction
from .mostRecentRecurringAction import MostRecentRecurringAction


class MostRecentRecurringActionRepositoryInterface(ABC):

    @abstractmethod
    async def getMostRecentRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> MostRecentRecurringAction | None:
        pass

    @abstractmethod
    async def setMostRecentRecurringAction(self, action: RecurringAction):
        pass
