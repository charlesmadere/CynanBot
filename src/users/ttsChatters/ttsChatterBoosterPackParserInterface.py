from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from ...tts.ttsProvider import TtsProvider
from .ttsChatterBoosterPack import TtsChatterBoosterPack


class TtsChatterBoosterPackParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        defaultTtsProvider: TtsProvider,
        jsonContents: dict[str, Any]
    ) -> TtsChatterBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        defaultTtsProvider: TtsProvider,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, TtsChatterBoosterPack] | None:
        pass
