from abc import ABC, abstractmethod
from typing import Any

from CynanBot.openWeather.openWeatherAirPollutionIndex import \
    OpenWeatherAirPollutionIndex
from CynanBot.openWeather.openWeatherAirPollutionReport import \
    OpenWeatherAirPollutionReport
from CynanBot.openWeather.openWeatherAlert import OpenWeatherAlert
from CynanBot.openWeather.openWeatherMoment import OpenWeatherMoment
from CynanBot.openWeather.openWeatherMomentDescription import \
    OpenWeatherMomentDescription
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport


class OpenWeatherJsonMapperInterface(ABC):

    @abstractmethod
    async def parseAirPollutionIndex(
        self,
        index: int | None
    ) -> OpenWeatherAirPollutionIndex | None:
        pass

    @abstractmethod
    async def parseAirPollutionReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherAirPollutionReport | None:
        pass

    @abstractmethod
    async def parseAlert(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherAlert | None:
        pass

    @abstractmethod
    async def parseMomentDescription(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMomentDescription | None:
        pass

    @abstractmethod
    async def parseMoment(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMoment | None:
        pass

    @abstractmethod
    async def parseWeatherReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherReport | None:
        pass
