from abc import ABC, abstractmethod

from .wordOfTheDayResponse import WordOfTheDayResponse


class WordOfTheDayPresenterInterface(ABC):

    @abstractmethod
    async def toString(
        self,
        includeRomaji: bool,
        wordOfTheDay: WordOfTheDayResponse,
    ) -> str:
        pass
