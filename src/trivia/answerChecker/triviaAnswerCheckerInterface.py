from abc import ABC, abstractmethod
from typing import Any

from .triviaAnswerCheckResult import TriviaAnswerCheckResult
from ..questions.absTriviaQuestion import AbsTriviaQuestion


class TriviaAnswerCheckerInterface(ABC):

    @abstractmethod
    async def checkAnswer(
        self,
        answer: str | None,
        triviaQuestion: AbsTriviaQuestion,
        extras: dict[str, Any] | None = None,
    ) -> TriviaAnswerCheckResult:
        pass
