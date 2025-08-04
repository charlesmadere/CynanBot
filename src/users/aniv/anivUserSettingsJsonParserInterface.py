from abc import ABC, abstractmethod
from typing import Any

from ...aniv.models.whichAnivUser import WhichAnivUser


class AnivUserSettingsJsonParserInterface(ABC):

    @abstractmethod
    def parseWhichAnivUser(
        self,
        whichAnivUser: str | Any | None,
    ) -> WhichAnivUser | None:
        pass

    @abstractmethod
    def requireWhichAnivUser(
        self,
        whichAnivUser: str | Any | None,
    ) -> WhichAnivUser:
        pass
