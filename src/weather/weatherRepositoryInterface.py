from abc import ABC, abstractmethod

from .weatherReport import WeatherReport
from ..location.location import Location
from ..misc.clearable import Clearable


class WeatherRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def fetchWeather(self, location: Location) -> WeatherReport:
        pass
