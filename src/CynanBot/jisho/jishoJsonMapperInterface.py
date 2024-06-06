from abc import ABC, abstractmethod
from typing import Any

from CynanBot.jisho.jishoData import JishoData
from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel
from CynanBot.jisho.jishoMeta import JishoMeta
from CynanBot.jisho.jishoResponse import JishoResponse


class JishoJsonMapperInterface(ABC):

    @abstractmethod
    async def parseData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoData | None:
        pass

    @abstractmethod
    async def parseJlptLevel(
        self,
        jsonString: str | Any | None
    ) -> JishoJlptLevel | None:
        pass

    @abstractmethod
    async def parseMeta(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoMeta | None:
        pass

    @abstractmethod
    async def parseResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoResponse | None:
        pass
