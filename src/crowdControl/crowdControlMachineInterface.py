from abc import ABC, abstractmethod

from .actions.crowdControlAction import CrowdControlAction
from .crowdControlActionHandler import CrowdControlActionHandler
from .crowdControlMessageHandler import CrowdControlMessageHandler


class CrowdControlMachineInterface(ABC):

    @abstractmethod
    def setActionHandler(self, actionHandler: CrowdControlActionHandler | None):
        pass

    @abstractmethod
    def setMessageHandler(self, messageHander: CrowdControlMessageHandler | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitAction(self, action: CrowdControlAction):
        pass
