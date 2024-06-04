from abc import ABC, abstractmethod

from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.transparent.transparentResponse import TransparentResponse


class TransparentApiServiceInterface(ABC):

    @abstractmethod
    async def fetchWordOfTheDay(
        self,
        targetLanguage: LanguageEntry
    ) -> TransparentResponse:
        pass
