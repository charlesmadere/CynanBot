from abc import ABC, abstractmethod

from .languageEntry import LanguageEntry
from .translationResponse import TranslationResponse


class TranslationHelperInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        text: str,
        targetLanguage: LanguageEntry | None = None,
    ) -> TranslationResponse:
        pass
