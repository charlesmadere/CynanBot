from abc import ABC, abstractmethod

from ..listener.timeoutEventListener import TimeoutEventListener
from ..models.absTimeoutAction import AbsTimeoutAction


class TimeoutActionMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: TimeoutEventListener | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitAction(self, action: AbsTimeoutAction):
        pass
