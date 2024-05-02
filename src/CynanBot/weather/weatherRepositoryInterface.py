from abc import abstractmethod

from CynanBot.location.location import Location
from CynanBot.misc.clearable import Clearable
from CynanBot.weather.weatherReport import WeatherReport


class WeatherRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchWeather(self, location: Location) -> WeatherReport:
        pass

    @abstractmethod
    async def isAvailable(self) -> bool:
        pass
