from abc import ABC, abstractmethod
from typing import Any

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseQuestionsResponse import OpenTriviaDatabaseQuestionsResponse
from .openTriviaDatabaseResponseCode import OpenTriviaDatabaseResponseCode
from .openTriviaDatabaseSessionToken import OpenTriviaDatabaseSessionToken


class OpenTriviaDatabaseJsonParserInterface(ABC):

    @abstractmethod
    async def parseQuestionsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenTriviaDatabaseQuestionsResponse | None:
        pass

    @abstractmethod
    async def parseResponseCode(
        self,
        responseCode: int | Any | None
    ) -> OpenTriviaDatabaseResponseCode | None:
        pass

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

    @abstractmethod
    async def requireResponseCode(
        self,
        responseCode: int | Any | None
    ) -> OpenTriviaDatabaseResponseCode:
        pass
