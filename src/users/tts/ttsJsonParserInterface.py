from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .ttsBoosterPack import TtsBoosterPack
from ...tts.ttsProvider import TtsProvider


class TtsJsonParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> TtsBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, TtsBoosterPack] | None:
        pass

    @abstractmethod
    def parseTtsProvider(
        self,
        ttsProvider: str
    ) -> TtsProvider:
        pass
