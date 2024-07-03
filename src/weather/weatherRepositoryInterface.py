from abc import abstractmethod

from ..location.location import Location
from ..misc.clearable import Clearable
from .weatherReport import WeatherReport


class WeatherRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchWeather(self, location: Location) -> WeatherReport:
        pass

    @abstractmethod
    async def isAvailable(self) -> bool:
        pass
