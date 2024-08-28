from abc import ABC, abstractmethod

from .actions.crowdControlAction import CrowdControlAction
from .crowdControlActionHandler import CrowdControlActionHandler


class CrowdControlMachineInterface(ABC):

    @abstractmethod
    def setActionHandler(self, actionHandler: CrowdControlActionHandler | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitAction(self, input: CrowdControlAction):
        pass
