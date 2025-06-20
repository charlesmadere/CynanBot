from abc import ABC, abstractmethod

from ..models.chatterItemType import ChatterItemType
from ...misc.clearable import Clearable


class ChatterInventorySettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getEnabledItemTypes(self) -> frozenset[ChatterItemType]:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
