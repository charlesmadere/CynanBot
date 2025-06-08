from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .redemptionCounterBoosterPack import RedemptionCounterBoosterPack


class RedemptionCounterBoosterPackParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> RedemptionCounterBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, RedemptionCounterBoosterPack] | None:
        pass
