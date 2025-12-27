from abc import ABC, abstractmethod
from typing import Any

from ..funtoonTriviaQuestion import FuntoonTriviaQuestion


class FuntoonApiServiceInterface(ABC):

    @abstractmethod
    async def banTriviaQuestion(self, triviaId: str) -> bool:
        pass

    @abstractmethod
    async def customEvent(
        self,
        data: dict[str, Any] | str | None,
        event: str,
        funtoonToken: str,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> bool:
        pass

    @abstractmethod
    async def fetchTriviaQuestion(self) -> FuntoonTriviaQuestion:
        pass
