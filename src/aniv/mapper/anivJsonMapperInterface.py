from abc import ABC, abstractmethod
from typing import Any

from ..models.whichAnivUser import WhichAnivUser


class AnivJsonMapperInterface(ABC):

    @abstractmethod
    def parseWhichAnivUser(
        self,
        string: str | Any | None
    ) -> WhichAnivUser | None:
        pass

    @abstractmethod
    def requireWhichAnivUser(
        self,
        string: str | Any | None
    ) -> WhichAnivUser:
        pass
