from abc import ABC, abstractmethod
from typing import Any

from .absOpenTriviaDatabaseQuestion import AbsOpenTriviaDatabaseQuestion


class OpenTriviaDatabaseJsonParserInterface(ABC):

    @abstractmethod
    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> AbsOpenTriviaDatabaseQuestion | None:
        pass
