from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .ttsBoosterPack import TtsBoosterPack


class TtsBoosterPackParserInterface(ABC):

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
    ) -> frozendict[int, TtsBoosterPack] | None:
        pass
