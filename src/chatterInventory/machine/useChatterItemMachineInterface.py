from abc import ABC, abstractmethod

from ..listeners.useChatterItemEventListener import UseChatterItemEventListener
from ..models.useChatterItemAction import UseChatterItemAction


class UseChatterItemMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: UseChatterItemEventListener | None):
        pass

    @abstractmethod
    def startMachine(self):
        pass

    @abstractmethod
    def submitAction(self, action: UseChatterItemAction):
        pass
