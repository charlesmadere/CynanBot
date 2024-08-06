from abc import ABC, abstractmethod
from typing import Any

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseSessionToken import OpenTriviaDatabaseSessionToken


class OpenTriviaDatabaseJsonParserInterface(ABC):

    @abstractmethod
    async def parseSessionToken(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenTriviaDatabaseSessionToken | None:
        pass

    @abstractmethod
    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenTriviaDatabaseQuestion | None:
        pass
