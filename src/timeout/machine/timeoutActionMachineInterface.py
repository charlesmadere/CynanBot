from abc import ABC, abstractmethod

from ..listener.timeoutEventListener import TimeoutEventListener
from ..models.actions.absTimeoutAction import AbsTimeoutAction
from ...misc.startable import Startable


class TimeoutActionMachineInterface(Startable, ABC):

    @abstractmethod
    def setEventListener(self, listener: TimeoutEventListener | None):
        pass

    @abstractmethod
    def submitAction(self, action: AbsTimeoutAction):
        pass
