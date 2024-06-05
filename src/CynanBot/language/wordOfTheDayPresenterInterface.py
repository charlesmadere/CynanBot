from abc import ABC, abstractmethod

from CynanBot.language.wordOfTheDayResponse import WordOfTheDayResponse


class WordOfTheDayPresenterInterface(ABC):

    @abstractmethod
    async def toString(
        self,
        wordOfTheDayResponse: WordOfTheDayResponse
    ) -> str:
        pass
