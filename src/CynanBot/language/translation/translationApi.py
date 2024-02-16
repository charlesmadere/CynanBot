from abc import ABC, abstractmethod

from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.translationApiSource import TranslationApiSource
from CynanBot.language.translationResponse import TranslationResponse


class TranslationApi(ABC):

    @abstractmethod
    def getTranslationApiSource(self) -> TranslationApiSource:
        pass

    @abstractmethod
    async def isAvailable(self) -> bool:
        pass

    @abstractmethod
    async def translate(self, text: str, targetLanguage: LanguageEntry) -> TranslationResponse:
        pass
