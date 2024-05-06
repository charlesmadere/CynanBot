from abc import ABC, abstractmethod

from CynanBot.weather.weatherReport import WeatherReport


class WeatherReportPresenterInterface(ABC):

    @abstractmethod
    async def toString(self, weather: WeatherReport) -> str:
        pass
