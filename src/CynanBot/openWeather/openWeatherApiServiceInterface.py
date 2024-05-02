from abc import ABC, abstractmethod

from CynanBot.openWeather.openWeatherAirQualityReport import OpenWeatherAirQualityReport
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport


class OpenWeatherApiServiceInterface(ABC):

    @abstractmethod
    async def fetchAirQuality(
        self,
        latitude: float,
        longitude: float
    ) -> OpenWeatherAirQualityReport:
        pass

    @abstractmethod
    async def fetchWeatherReport(
        self,
        latitude: float,
        longitude: float
    ) -> OpenWeatherReport:
        pass
