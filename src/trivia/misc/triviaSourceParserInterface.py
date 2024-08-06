from abc import ABC, abstractmethod
from typing import Any

from ..questions.triviaSource import TriviaSource


class TriviaSourceParserInterface(ABC):

    @abstractmethod
    async def parse(self, triviaSource: str | Any | None) -> TriviaSource:
        pass

    @abstractmethod
    async def serialize(self, triviaSource: TriviaSource) -> str:
        pass
