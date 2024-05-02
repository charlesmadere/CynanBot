from abc import ABC, abstractmethod

from CynanBot.openWeather.openWeatherReport import OpenWeatherReport


class OpenWeatherApiServiceInterface(ABC):

    @abstractmethod
    async def fetchWeatherReport(
        self,
        latitude: float,
        longitude: float
    ) -> OpenWeatherReport:
        pass
