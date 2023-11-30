from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.recurringActions.recurringActionEventListener import \
    RecurringActionEventListener


class RecurringActionsMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: Optional[RecurringActionEventListener]):
        pass

    @abstractmethod
    def startMachine(self):
        pass
