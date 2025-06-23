from abc import ABC, abstractmethod
from typing import Any

from frozenlist import FrozenList

from .supStreamerBoosterPack import SupStreamerBoosterPack

class SupStreamerBoosterPackJsonParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> SupStreamerBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> FrozenList[SupStreamerBoosterPack] | None:
        pass
