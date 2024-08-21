from abc import ABC, abstractmethod
from typing import Any

from frozenlist import FrozenList

from .willFryTriviaQuestion import WillFryTriviaQuestion
from .willFryTriviaQuestionText import WillFryTriviaQuestionText
from .willFryTriviaQuestionType import WillFryTriviaQuestionType


class WillFryTriviaJsonParserInterface(ABC):

    @abstractmethod
    async def parseQuestionText(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> WillFryTriviaQuestionText | None:
        pass

    @abstractmethod
    async def parseQuestionType(
        self,
        questionType: str | Any | None
    ) -> WillFryTriviaQuestionType | None:
        pass

    @abstractmethod
    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> WillFryTriviaQuestion | None:
        pass

    @abstractmethod
    async def parseTriviaQuestions(
        self,
        jsonContents: list[dict[str, Any] | Any | None] | None
    ) -> FrozenList[WillFryTriviaQuestion] | None:
        pass
