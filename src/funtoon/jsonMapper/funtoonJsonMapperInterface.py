from abc import ABC, abstractmethod
from typing import Any

from ..funtoonPkmnCatchType import FuntoonPkmnCatchType
from ..funtoonTriviaQuestion import FuntoonTriviaQuestion


class FuntoonJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> FuntoonTriviaQuestion | None:
        pass

    @abstractmethod
    async def serializePkmnCatchType(
        self,
        pkmnCatchType: FuntoonPkmnCatchType,
    ) -> str:
        pass
