from abc import ABC, abstractmethod

from CynanBot.location.location import Location
from CynanBot.openWeather.openWeatherAirPollutionReport import \
    OpenWeatherAirPollutionReport
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport


class OpenWeatherApiServiceInterface(ABC):

    @abstractmethod
    async def fetchAirPollutionReport(self, location: Location) -> OpenWeatherAirPollutionReport:
        pass

    @abstractmethod
    async def fetchWeatherReport(self, location: Location) -> OpenWeatherReport:
        pass
