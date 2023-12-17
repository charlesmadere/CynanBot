from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaAnswerCheckResult import TriviaAnswerCheckResult


class TriviaAnswerCheckerInterface(ABC):

    @abstractmethod
    async def checkAnswer(
        self,
        answer: Optional[str],
        triviaQuestion: AbsTriviaQuestion,
        extras: Optional[Dict[str, Any]] = None
    ) -> TriviaAnswerCheckResult:
        pass
