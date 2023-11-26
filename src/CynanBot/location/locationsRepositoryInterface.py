from abc import abstractmethod

from CynanBot.location.location import Location
from CynanBot.misc.clearable import Clearable


class LocationsRepositoryInterface(Clearable):

    @abstractmethod
    async def getLocation(self, locationId: str) -> Location:
        pass
