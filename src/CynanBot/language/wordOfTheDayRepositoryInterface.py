from abc import abstractmethod

from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.wordOfTheDayResponse import WordOfTheDayResponse
from CynanBot.misc.clearable import Clearable


class WordOfTheDayRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        pass
