from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .pkmnCatchBoosterPack import PkmnCatchBoosterPack
from .pkmnCatchType import PkmnCatchType


class PkmnJsonParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> PkmnCatchBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, PkmnCatchBoosterPack] | None:
        pass

    @abstractmethod
    def parseCatchType(
        self,
        catchType: str | Any | None
    ) -> PkmnCatchType | None:
        pass
