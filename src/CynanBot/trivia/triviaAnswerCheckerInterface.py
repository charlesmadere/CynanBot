from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from trivia.absTriviaQuestion import AbsTriviaQuestion
from trivia.triviaAnswerCheckResult import TriviaAnswerCheckResult


class TriviaAnswerCheckerInterface(ABC):

    @abstractmethod
    async def checkAnswer(
        self,
        answer: Optional[str],
        triviaQuestion: AbsTriviaQuestion,
        extras: Optional[Dict[str, Any]] = None
    ) -> TriviaAnswerCheckResult:
        pass
