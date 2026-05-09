from abc import ABC, abstractmethod

from ..models.actions.absTimeoutAction import AbsTimeoutAction
from ...misc.startable import Startable


class TimeoutActionMachineInterface(Startable, ABC):

    @abstractmethod
    def submitAction(self, action: AbsTimeoutAction):
        pass
