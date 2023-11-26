from abc import ABC, abstractmethod

from recurringActions.recurringEvent import RecurringEvent


class RecurringActionEventListener(ABC):

    @abstractmethod
    async def onNewRecurringActionEvent(self, event: RecurringEvent):
        pass
