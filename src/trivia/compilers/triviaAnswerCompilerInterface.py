from abc import ABC, abstractmethod
from typing import Collection


class TriviaAnswerCompilerInterface(ABC):

    @abstractmethod
    async def compileBoolAnswer(self, answer: str | None) -> bool:
        pass

    @abstractmethod
    async def compileMultipleChoiceAnswer(self, answer: str | None) -> int:
        pass

    @abstractmethod
    async def compileTextAnswer(self, answer: str | None) -> str:
        pass

    @abstractmethod
    async def compileTextAnswersList(
        self,
        answers: Collection[str | None] | None,
        allWords: frozenset[str] | None = None,
        expandParentheses: bool = True,
    ) -> list[str]:
        pass

    @abstractmethod
    async def expandNumerals(self, answer: str) -> list[str]:
        pass
