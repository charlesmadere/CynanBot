from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .cutenessBoosterPack import CutenessBoosterPack


class CutenessBoosterPackJsonParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> CutenessBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, CutenessBoosterPack] | None:
        pass
