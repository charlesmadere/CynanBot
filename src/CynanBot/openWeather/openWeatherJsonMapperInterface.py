from abc import ABC, abstractmethod
from typing import Any

from CynanBot.openWeather.openWeatherMomentReport import OpenWeatherMomentReport
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport


class OpenWeatherJsonMapperInterface(ABC):

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
