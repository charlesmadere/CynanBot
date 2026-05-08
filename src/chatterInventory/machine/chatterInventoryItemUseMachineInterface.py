from abc import ABC, abstractmethod

from ..models.absChatterItemAction import AbsChatterItemAction
from ...misc.startable import Startable


class ChatterInventoryItemUseMachineInterface(Startable, ABC):

    @abstractmethod
    def submitAction(self, action: AbsChatterItemAction):
        pass
