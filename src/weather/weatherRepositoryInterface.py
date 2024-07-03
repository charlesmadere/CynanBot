from abc import abstractmethod

from .weatherReport import WeatherReport
from ..location.location import Location
from ..misc.clearable import Clearable


class WeatherRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchWeather(self, location: Location) -> WeatherReport:
        pass

    @abstractmethod
    async def isAvailable(self) -> bool:
        pass
