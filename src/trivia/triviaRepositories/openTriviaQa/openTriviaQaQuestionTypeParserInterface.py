from abc import ABC, abstractmethod
from typing import Any

from .openTriviaQaQuestionType import OpenTriviaQaQuestionType


class OpenTriviaQaQuestionTypeParserInterface(ABC):

    @abstractmethod
    async def parse(
        self,
        questionType: str | Any | None
    ) -> OpenTriviaQaQuestionType | None:
        pass

    @abstractmethod
    async def require(
        self,
        questionType: str | Any | None
    ) -> OpenTriviaQaQuestionType:
        pass
