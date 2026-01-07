from abc import ABC, abstractmethod
from typing import Any

from ..questions.triviaQuestionType import TriviaQuestionType


class TriviaQuestionTypeParserInterface(ABC):

    @abstractmethod
    async def parse(
        self,
        triviaQuestionType: str | Any | None,
    ) -> TriviaQuestionType:
        pass

    @abstractmethod
    async def serialize(
        self,
        triviaQuestionType: TriviaQuestionType,
    ) -> str:
        pass
