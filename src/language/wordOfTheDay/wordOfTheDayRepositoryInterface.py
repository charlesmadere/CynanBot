from abc import ABC, abstractmethod

from .wordOfTheDayResponse import WordOfTheDayResponse
from ..languageEntry import LanguageEntry
from ...misc.clearable import Clearable


class WordOfTheDayRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        pass
