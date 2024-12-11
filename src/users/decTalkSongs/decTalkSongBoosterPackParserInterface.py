from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from .decTalkSongBoosterPack import DecTalkSongBoosterPack


class DecTalkSongBoosterPackParserInterface(ABC):

    @abstractmethod
    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> DecTalkSongBoosterPack:
        pass

    @abstractmethod
    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, DecTalkSongBoosterPack] | None:
        pass
