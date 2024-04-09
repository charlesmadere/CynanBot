from abc import ABC, abstractmethod

from CynanBot.deepL.deepLTranslationResponse import DeepLTranslationResponse
from CynanBot.language.languageEntry import LanguageEntry


class DeepLApiServicecInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        targetLanguage: LanguageEntry,
        text: str,
    ) -> DeepLTranslationResponse:
        pass
