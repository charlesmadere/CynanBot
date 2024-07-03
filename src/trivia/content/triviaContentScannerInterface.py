from abc import ABC, abstractmethod

from .triviaContentCode import TriviaContentCode
from ..questions.absTriviaQuestion import AbsTriviaQuestion


class TriviaContentScannerInterface(ABC):

    @abstractmethod
    async def verify(self, question: AbsTriviaQuestion | None) -> TriviaContentCode:
        pass
