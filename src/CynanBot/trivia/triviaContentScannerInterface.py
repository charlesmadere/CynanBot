from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaContentCode import TriviaContentCode


class TriviaContentScannerInterface(ABC):

    @abstractmethod
    async def verify(self, question: Optional[AbsTriviaQuestion]) -> TriviaContentCode:
        pass
