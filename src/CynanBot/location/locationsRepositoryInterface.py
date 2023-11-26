from abc import abstractmethod

from location.location import Location
from misc.clearable import Clearable


class LocationsRepositoryInterface(Clearable):

    @abstractmethod
    async def getLocation(self, locationId: str) -> Location:
        pass
