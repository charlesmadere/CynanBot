from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .crowdControlBoosterPack import CrowdControlBoosterPack
from .crowdControlInputType import CrowdControlInputType


class CrowdControlJsonParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> CrowdControlBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, CrowdControlBoosterPack] | None:
        pass

    @abstractmethod
    def parseInputType(
        self,
        inputType: str
    ) -> CrowdControlInputType:
        pass
