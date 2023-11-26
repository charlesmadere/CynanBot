from abc import abstractmethod

from language.languageEntry import LanguageEntry
from language.wordOfTheDayResponse import WordOfTheDayResponse
from misc.clearable import Clearable


class WordOfTheDayRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        pass
