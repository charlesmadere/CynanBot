from abc import ABC, abstractmethod

from CynanBot.openWeather.openWeatherAirPollutionReport import \
    OpenWeatherAirPollutionReport
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport


class OpenWeatherApiServiceInterface(ABC):

    @abstractmethod
    async def fetchAirPollutionReport(
        self,
        latitude: float,
        longitude: float
    ) -> OpenWeatherAirPollutionReport:
        pass

    @abstractmethod
    async def fetchWeatherReport(
        self,
        latitude: float,
        longitude: float
    ) -> OpenWeatherReport:
        pass
