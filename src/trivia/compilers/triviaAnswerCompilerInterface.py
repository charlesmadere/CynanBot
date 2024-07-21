from abc import ABC, abstractmethod
from typing import Collection


class TriviaAnswerCompilerInterface(ABC):

    @abstractmethod
    async def findQuestionBasedAnswerAddendum(self, questionText: str) -> str | None:
        pass

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
        expandParentheses: bool = True,
        answerAddendum: str | None = None
    ) -> list[str]:
        pass

    @abstractmethod
    async def expandNumerals(self, answer: str) -> list[str]:
        pass
