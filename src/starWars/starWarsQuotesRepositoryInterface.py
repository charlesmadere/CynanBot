from abc import ABC, abstractmethod

from ..misc.clearable import Clearable


class StarWarsQuotesRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def fetchRandomQuote(self, trilogy: str | None = None) -> str:
        pass

    @abstractmethod
    async def searchQuote(self, query: str, input: str | None = None) -> str | None:
        pass
