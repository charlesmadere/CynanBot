from abc import ABC, abstractmethod

from .location import Location
from ..misc.clearable import Clearable


class LocationsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getLocation(self, locationId: str) -> Location:
        pass
