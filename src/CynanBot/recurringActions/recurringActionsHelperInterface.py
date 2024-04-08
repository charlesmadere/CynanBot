from abc import ABC, abstractmethod

from CynanBot.recurringActions.recurringAction import RecurringAction


class RecurringActionsHelperInterface(ABC):

    @abstractmethod
    async def disableRecurringAction(self, recurringAction: RecurringAction | None) -> bool:
        pass
