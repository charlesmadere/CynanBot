from abc import ABC, abstractmethod

from ..listeners.chatterItemEventListener import ChatterItemEventListener
from ..models.absChatterItemAction import AbsChatterItemAction
from ...misc.startable import Startable


class ChatterInventoryItemUseMachineInterface(Startable, ABC):

    @abstractmethod
    def setEventListener(self, listener: ChatterItemEventListener | None):
        pass

    @abstractmethod
    def submitAction(self, action: AbsChatterItemAction):
        pass
