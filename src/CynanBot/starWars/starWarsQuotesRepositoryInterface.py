from abc import abstractmethod
from typing import Optional

from CynanBot.misc.clearable import Clearable


class StarWarsQuotesRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchRandomQuote(self, trilogy: Optional[str] = None) -> str:
        pass

    @abstractmethod
    async def searchQuote(self, query: str, input: Optional[str] = None) -> str:
        pass
