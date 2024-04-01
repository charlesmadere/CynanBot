from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class StarWarsQuotesRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchRandomQuote(self, trilogy: str | None = None) -> str:
        pass

    @abstractmethod
    async def searchQuote(self, query: str, input: str | None = None) -> str | None:
        pass
