from abc import ABC, abstractmethod
from typing import Any

from CynanBot.openWeather.openWeatherAirPollutionIndex import \
    OpenWeatherAirPollutionIndex
from CynanBot.openWeather.openWeatherAirPollutionReport import \
    OpenWeatherAirPollutionReport
from CynanBot.openWeather.openWeatherAlert import OpenWeatherAlert
from CynanBot.openWeather.openWeatherDay import OpenWeatherDay
from CynanBot.openWeather.openWeatherFeelsLike import OpenWeatherFeelsLike
from CynanBot.openWeather.openWeatherMoment import OpenWeatherMoment
from CynanBot.openWeather.openWeatherMomentDescription import \
    OpenWeatherMomentDescription
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport
from CynanBot.openWeather.openWeatherTemperature import OpenWeatherTemperature


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
    async def parseDay(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherDay | None:
        pass

    @abstractmethod
    async def parseFeelsLike(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherFeelsLike | None:
        pass

    @abstractmethod
    async def parseMoment(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMoment | None:
        pass

    @abstractmethod
    async def parseMomentDescription(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMomentDescription | None:
        pass

    @abstractmethod
    async def parseTemperature(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherTemperature | None:
        pass

    @abstractmethod
    async def parseWeatherReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherReport | None:
        pass
