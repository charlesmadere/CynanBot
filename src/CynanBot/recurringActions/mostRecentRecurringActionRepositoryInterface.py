from abc import ABC, abstractmethod

from CynanBot.recurringActions.mostRecentRecurringAction import \
    MostRecentRecurringAction
from CynanBot.recurringActions.recurringAction import RecurringAction


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
