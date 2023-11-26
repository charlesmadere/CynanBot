from abc import ABC, abstractmethod
from typing import Optional


class TriviaIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateActionId(self) -> str:
        pass

    @abstractmethod
    async def generateEventId(self) -> str:
        pass

    @abstractmethod
    async def generateQuestionId(
        self,
        question: str,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> str:
        pass
