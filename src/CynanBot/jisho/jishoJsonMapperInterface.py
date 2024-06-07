from abc import ABC, abstractmethod
from typing import Any

from CynanBot.jisho.jishoAttribution import JishoAttribution
from CynanBot.jisho.jishoData import JishoData
from CynanBot.jisho.jishoJapaneseWord import JishoJapaneseWord
from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel
from CynanBot.jisho.jishoMeta import JishoMeta
from CynanBot.jisho.jishoResponse import JishoResponse
from CynanBot.jisho.jishoSense import JishoSense


class JishoJsonMapperInterface(ABC):

    @abstractmethod
    async def parseAttribution(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoAttribution | None:
        pass

    @abstractmethod
    async def parseData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoData | None:
        pass

    @abstractmethod
    async def parseJapaneseWord(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoJapaneseWord | None:
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

    @abstractmethod
    async def parseSense(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoSense | None:
        pass
