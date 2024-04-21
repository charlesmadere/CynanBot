from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.translationResponse import TranslationResponse


class TranslationHelperInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        text: str,
        targetLanguage: Optional[LanguageEntry] = None
    ) -> TranslationResponse:
        pass
