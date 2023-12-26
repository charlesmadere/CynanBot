from abc import ABC, abstractmethod
from typing import Collection, List, Optional


class TriviaAnswerCompilerInterface(ABC):

    @abstractmethod
    async def compileBoolAnswer(self, answer: Optional[str]) -> bool:
        pass

    @abstractmethod
    async def compileTextAnswer(self, answer: Optional[str]) -> str:
        pass

    @abstractmethod
    async def compileTextAnswersList(
        self,
        answers: Optional[Collection[Optional[str]]],
        expandParentheses: bool = True
    ) -> List[str]:
        pass

    @abstractmethod
    async def compileTextAnswerToMultipleChoiceOrdinal(self, answer: Optional[str]) -> int:
        pass

    @abstractmethod
    async def expandNumerals(self, answer: str) -> List[str]:
        pass
