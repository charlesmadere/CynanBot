from abc import ABC, abstractmethod

from .openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from .openWeatherReport import OpenWeatherReport
from ..location.location import Location


class OpenWeatherApiServiceInterface(ABC):

    @abstractmethod
    async def fetchAirPollutionReport(self, location: Location) -> OpenWeatherAirPollutionReport:
        pass

    @abstractmethod
    async def fetchWeatherReport(self, location: Location) -> OpenWeatherReport:
        pass
