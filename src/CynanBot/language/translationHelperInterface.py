from abc import ABC, abstractmethod
from typing import Optional

from language.languageEntry import LanguageEntry
from language.translationResponse import TranslationResponse


class TranslationHelperInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        text: str,
        targetLanguageEntry: Optional[LanguageEntry] = None
    ) -> TranslationResponse:
        pass
