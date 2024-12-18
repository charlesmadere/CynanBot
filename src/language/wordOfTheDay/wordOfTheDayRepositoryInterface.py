from abc import abstractmethod

from .wordOfTheDayResponse import WordOfTheDayResponse
from ..languageEntry import LanguageEntry
from ...misc.clearable import Clearable


class WordOfTheDayRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        pass
