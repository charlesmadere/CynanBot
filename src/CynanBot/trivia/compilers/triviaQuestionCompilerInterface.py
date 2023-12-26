from abc import ABC, abstractmethod
from typing import Collection, List, Optional


class TriviaQuestionCompilerInterface(ABC):

    @abstractmethod
    async def compileCategory(
        self,
        category: str,
        htmlUnescape: bool = False
    ) -> str:
        pass

    @abstractmethod
    async def compileQuestion(
        self,
        question: str,
        htmlUnescape: bool = False
    ) -> str:
        pass

    @abstractmethod
    async def compileResponse(
        self,
        response: str,
        htmlUnescape: bool = False
    ) -> str:
        pass

    @abstractmethod
    async def compileResponses(
        self,
        responses: Optional[Collection[Optional[str]]],
        htmlUnescape: bool = False
    ) -> List[str]:
        pass
