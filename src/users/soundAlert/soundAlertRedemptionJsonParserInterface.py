from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .soundAlertRedemption import SoundAlertRedemption


class SoundAlertRedemptionJsonParserInterface(ABC):

    @abstractmethod
    def parseRedemption(
        self,
        jsonContents: dict[str, Any]
    ) -> SoundAlertRedemption:
        pass

    @abstractmethod
    def parseRedemptions(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, SoundAlertRedemption] | None:
        pass
