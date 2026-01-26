from abc import ABC, abstractmethod

from .transparentResponse import TransparentResponse
from ..language.languageEntry import LanguageEntry


class TransparentApiServiceInterface(ABC):

    @abstractmethod
    async def fetchWordOfTheDay(
        self,
        targetLanguage: LanguageEntry,
    ) -> TransparentResponse:
        pass
