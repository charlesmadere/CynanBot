from abc import ABC, abstractmethod
from typing import Any

from .jishoAttribution import JishoAttribution
from .jishoData import JishoData
from .jishoJapaneseWord import JishoJapaneseWord
from .jishoJlptLevel import JishoJlptLevel
from .jishoMeta import JishoMeta
from .jishoResponse import JishoResponse
from .jishoSense import JishoSense


class JishoJsonMapperInterface(ABC):

    @abstractmethod
    async def parseAttribution(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> JishoAttribution | None:
        pass

    @abstractmethod
    async def parseData(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> JishoData | None:
        pass

    @abstractmethod
    async def parseJapaneseWord(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> JishoJapaneseWord | None:
        pass

    @abstractmethod
    async def parseJlptLevel(
        self,
        jsonString: str | Any | None,
    ) -> JishoJlptLevel | None:
        pass

    @abstractmethod
    async def parseMeta(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> JishoMeta | None:
        pass

    @abstractmethod
    async def parseResponse(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> JishoResponse | None:
        pass

    @abstractmethod
    async def parseSense(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> JishoSense | None:
        pass
