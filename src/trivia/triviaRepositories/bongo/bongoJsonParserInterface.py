from abc import ABC, abstractmethod
from typing import Any

from frozenlist import FrozenList

from .bongoTriviaQuestion import BongoTriviaQuestion


class BongoJsonParserInterface(ABC):

    @abstractmethod
    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> BongoTriviaQuestion | None:
        pass

    @abstractmethod
    async def parseTriviaQuestions(
        self,
        jsonContents: list[dict[str, Any] | None] | Any | None
    ) -> FrozenList[BongoTriviaQuestion] | None:
        pass
