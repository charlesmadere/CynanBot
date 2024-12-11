from abc import ABC, abstractmethod
from datetime import tzinfo
from typing import Any

from ..models.openWeatherAirPollutionIndex import OpenWeatherAirPollutionIndex
from ..models.openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from ..models.openWeatherAlert import OpenWeatherAlert
from ..models.openWeatherDay import OpenWeatherDay
from ..models.openWeatherFeelsLike import OpenWeatherFeelsLike
from ..models.openWeatherMoment import OpenWeatherMoment
from ..models.openWeatherMomentDescription import OpenWeatherMomentDescription
from ..models.openWeatherReport import OpenWeatherReport
from ..models.openWeatherTemperature import OpenWeatherTemperature


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
