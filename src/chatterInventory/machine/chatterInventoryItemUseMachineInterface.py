from abc import ABC, abstractmethod

from ..listeners.chatterItemEventListener import ChatterItemEventListener
from ..models.absChatterItemAction import AbsChatterItemAction


class ChatterInventoryItemUseMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: ChatterItemEventListener | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitAction(self, action: AbsChatterItemAction):
        pass
