from abc import abstractmethod

from .languageEntry import LanguageEntry
from .wordOfTheDayResponse import WordOfTheDayResponse
from ..misc.clearable import Clearable


class WordOfTheDayRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        pass
