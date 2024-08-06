from abc import ABC, abstractmethod
from typing import Any

from ..triviaDifficulty import TriviaDifficulty


class TriviaDifficultyParserInterface(ABC):

    @abstractmethod
    async def parse(
        self,
        triviaDifficulty: Any | None
    ) -> TriviaDifficulty:
        pass
