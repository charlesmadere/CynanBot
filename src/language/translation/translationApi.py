from abc import ABC, abstractmethod

from ..languageEntry import LanguageEntry
from ..translationApiSource import TranslationApiSource
from ..translationResponse import TranslationResponse


class TranslationApi(ABC):

    @abstractmethod
    async def isAvailable(self) -> bool:
        pass

    @abstractmethod
    async def translate(
        self,
        text: str,
        targetLanguage: LanguageEntry,
    ) -> TranslationResponse:
        pass

    @property
    @abstractmethod
    def translationApiSource(self) -> TranslationApiSource:
        pass
