from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .timeoutBoosterPack import TimeoutBoosterPack
from .timeoutBoosterPackType import TimeoutBoosterPackType


class TimeoutBoosterPackJsonParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> TimeoutBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPackType(
        self,
        boosterPackType: str
    ) -> TimeoutBoosterPackType:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, TimeoutBoosterPack] | None:
        pass
