from abc import ABC, abstractmethod

from .actions.crowdControlAction import CrowdControlAction
from .crowdControlActionHandler import CrowdControlActionHandler
from .message.crowdControlMessageListener import CrowdControlMessageListener


class CrowdControlMachineInterface(ABC):

    @property
    @abstractmethod
    def isPaused(self) -> bool:
        pass

    @abstractmethod
    def pause(self) -> bool:
        pass

    @abstractmethod
    def resume(self) -> bool:
        pass

    @abstractmethod
    def setActionHandler(self, actionHandler: CrowdControlActionHandler | None):
        pass

    @abstractmethod
    def setMessageListener(self, messageListener: CrowdControlMessageListener | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitAction(self, action: CrowdControlAction):
        pass
