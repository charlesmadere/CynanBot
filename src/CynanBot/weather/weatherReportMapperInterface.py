from abc import ABC, abstractmethod

from CynanBot.openWeather.openWeatherReport import OpenWeatherReport
from CynanBot.weather.weatherReport import WeatherReport


class WeatherReportMapperInterface(ABC):

    @abstractmethod
    async def fromOpenWeatherReport(
        self,
        report: OpenWeatherReport
    ) -> WeatherReport:
        pass
