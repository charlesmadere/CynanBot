from abc import ABC, abstractmethod

from .recurringActionEventListener import RecurringActionEventListener
from ..misc.startable import Startable


class RecurringActionsMachineInterface(Startable, ABC):

    @abstractmethod
    def setEventListener(self, listener: RecurringActionEventListener | None):
        pass
