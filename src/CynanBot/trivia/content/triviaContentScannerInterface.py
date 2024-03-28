from abc import ABC, abstractmethod

from CynanBot.trivia.content.triviaContentCode import TriviaContentCode
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion


class TriviaContentScannerInterface(ABC):

    @abstractmethod
    async def verify(self, question: AbsTriviaQuestion | None) -> TriviaContentCode:
        pass
