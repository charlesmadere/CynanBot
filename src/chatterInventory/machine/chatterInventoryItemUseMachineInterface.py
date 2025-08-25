from abc import ABC, abstractmethod

from ..listeners.useChatterItemEventListener import UseChatterItemEventListener
from ..models.useChatterItemAction import UseChatterItemAction


class ChatterInventoryItemUseMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: UseChatterItemEventListener | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitAction(self, action: UseChatterItemAction):
        pass
