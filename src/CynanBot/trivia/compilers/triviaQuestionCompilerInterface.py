from abc import ABC, abstractmethod
from typing import Collection, List, Optional


class TriviaQuestionCompilerInterface(ABC):

    @abstractmethod
    async def compileCategory(
        self,
        category: Optional[str],
        htmlUnescape: bool = False
    ) -> str:
        pass

    @abstractmethod
    async def compileQuestion(
        self,
        question: Optional[str],
        htmlUnescape: bool = False
    ) -> str:
        pass

    @abstractmethod
    async def compileResponse(
        self,
        response: Optional[str],
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
