from abc import ABC, abstractmethod
from datetime import tzinfo
from typing import Any

from .openWeatherAirPollutionIndex import OpenWeatherAirPollutionIndex
from .openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from .openWeatherAlert import OpenWeatherAlert
from .openWeatherDay import OpenWeatherDay
from .openWeatherFeelsLike import OpenWeatherFeelsLike
from .openWeatherMoment import OpenWeatherMoment
from .openWeatherMomentDescription import OpenWeatherMomentDescription
from .openWeatherReport import OpenWeatherReport
from .openWeatherTemperature import OpenWeatherTemperature


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
        jsonContents: dict[str, Any] | Any | None,
        timeZone: tzinfo
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
        jsonContents: dict[str, Any] | Any | None,
        timeZone: tzinfo
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
        jsonContents: dict[str, Any] | Any | None,
        timeZone: tzinfo
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
