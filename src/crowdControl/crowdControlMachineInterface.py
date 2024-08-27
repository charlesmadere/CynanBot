from abc import ABC, abstractmethod

from .crowdControlInput import CrowdControlInput
from .crowdControlInputHandler import CrowdControlInputHandler


class CrowdControlMachineInterface(ABC):

    @abstractmethod
    def setInputHandler(self, inputHandler: CrowdControlInputHandler | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitInput(self, input: CrowdControlInput):
        pass
