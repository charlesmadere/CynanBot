from abc import ABC, abstractmethod
from typing import Any

from CynanBot.openWeather.openWeatherAirQualityIndex import OpenWeatherAirQualityIndex
from CynanBot.openWeather.openWeatherAirQualityReport import OpenWeatherAirQualityReport
from CynanBot.openWeather.openWeatherMomentReport import OpenWeatherMomentReport
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport


class OpenWeatherJsonMapperInterface(ABC):

    @abstractmethod
    async def parseAirQualityIndex(
        self,
        index: int | None
    ) -> OpenWeatherAirQualityIndex | None:
        pass

    @abstractmethod
    async def parseAirQualityReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherAirQualityReport | None:
        pass

    @abstractmethod
    async def parseWeatherMomentReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMomentReport | None:
        pass

    @abstractmethod
    async def parseWeatherReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherReport | None:
        pass
