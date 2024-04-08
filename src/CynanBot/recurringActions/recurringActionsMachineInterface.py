from abc import ABC, abstractmethod

from CynanBot.recurringActions.recurringActionEventListener import \
    RecurringActionEventListener


class RecurringActionsMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: RecurringActionEventListener | None):
        pass

    @abstractmethod
    def startMachine(self):
        pass
