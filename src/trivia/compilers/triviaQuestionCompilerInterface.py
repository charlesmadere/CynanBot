from abc import ABC, abstractmethod
from typing import Collection


class TriviaQuestionCompilerInterface(ABC):

    @abstractmethod
    async def compileCategory(
        self,
        category: str | None,
        htmlUnescape: bool = False,
    ) -> str:
        pass

    @abstractmethod
    async def compileQuestion(
        self,
        question: str | None,
        htmlUnescape: bool = False,
    ) -> str:
        pass

    @abstractmethod
    async def compileResponse(
        self,
        response: str | None,
        htmlUnescape: bool = False,
    ) -> str:
        pass

    @abstractmethod
    async def compileResponses(
        self,
        responses: Collection[str | None] | None,
        htmlUnescape: bool = False,
    ) -> list[str]:
        pass

    @abstractmethod
    async def findAllWordsInQuestion(
        self,
        category: str | None,
        question: str,
    ) -> frozenset[str]:
        pass
