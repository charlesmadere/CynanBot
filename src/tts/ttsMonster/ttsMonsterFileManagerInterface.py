from abc import ABC, abstractmethod
from typing import Collection

from frozenlist import FrozenList


class TtsMonsterFileManagerInterface(ABC):

    @abstractmethod
    async def saveTtsUrlToNewFile(self, ttsUrl: str) -> str | None:
        pass

    @abstractmethod
    async def saveTtsUrlsToNewFiles(self, ttsUrls: Collection[str]) -> FrozenList[str] | None:
        pass
